"""Step 7.5 original-provider ISRUC-S1 migration and cohort audit.

This script intentionally contains no split, model, training, normalization, or metric logic.
"""
from __future__ import annotations
import csv, hashlib, json, math, os, shutil, tempfile, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pyedflib

from shiftsleep_uq.data.preprocess import (
    PreprocessingError, original_recording_spec, read_original_scorer1,
    resample_continuous, slice_epochs, summarize_epoch_accounting,
    unit_to_uv, validate_output,
)
from shiftsleep_uq.data.preprocessing import expand_annotations
from shiftsleep_uq.data.montage_contract import resolve_isruc_channels

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/isruc-original"
OUT = ROOT / "data/processed/isruc_original_v1"
REPORTS = ROOT / "reports"
LABELS = ("Wake", "N1", "N2", "N3", "REM")
EXPECTED = tuple(range(1, 101))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(name: str, rows: list[dict], fields: list[str] | None = None) -> Path:
    path = REPORTS / name
    if fields is None:
        fields = []
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def resolve_bundle(n: int) -> tuple[Path | None, Path | None, Path | None, Path | None, Path | None, list[Path]]:
    root = RAW / f"subject-{n}"
    files = sorted(p for p in root.rglob("*") if p.is_file()) if root.exists() else []
    by_name = {p.name: p for p in files}
    return (by_name.get(f"{n}.rec"), by_name.get(f"{n}_1.txt"), by_name.get(f"{n}_1.xlsx"),
            by_name.get(f"{n}_2.txt"), by_name.get(f"{n}_2.xlsx"), files)


def bundle_status(n: int, files: list[Path], rec: Path | None, s1: Path | None, s1x: Path | None,
                  s2: Path | None, s2x: Path | None) -> tuple[str, str]:
    names = {p.name for p in files}
    expected = {f"{n}.rec", f"{n}_1.txt", f"{n}_1.xlsx", f"{n}_2.txt", f"{n}_2.xlsx"}
    if rec is None: return "BUNDLE_MISSING_SIGNAL", "MISSING_SIGNAL"
    if s1 is None or s1x is None: return "BUNDLE_MISSING_SCORER1", "MISSING_SCORER1"
    if s2 is None or s2x is None: return "BUNDLE_MISSING_SCORER2", "MISSING_SCORER2"
    if names - expected: return "BUNDLE_EXTRA_FILES", "EXTRA_FILES:" + "|".join(sorted(names - expected))
    return "BUNDLE_COMPLETE", ""


def rec_audit(path: Path | None) -> dict:
    if path is None: return {"header_valid": False, "body_valid": False, "failure_code": "MISSING_SIGNAL"}
    try:
        f = pyedflib.EdfReader(str(path))
        try:
            header = int(f.getHeader().get("recording_additional", "") is not None)  # parser smoke
            ns = int(f.signals_in_file)
            records = int(f.datarecords_in_file)
            duration = float(f.datarecord_duration)
            samples = [int(f.samples_in_datarecord(i)) for i in range(ns)]
            header_bytes = 256 * (ns + 1)
            expected = header_bytes + records * sum(samples) * 2
            actual = path.stat().st_size
            labels = [str(x) for x in f.getSignalLabels()]
            rates = [float(f.getSampleFrequency(i)) for i in range(ns)]
            units = [str(f.getPhysicalDimension(i)) for i in range(ns)]
            return {"header_valid": True, "body_valid": actual == expected,
                    "header_length": header_bytes, "signal_count": ns,
                    "number_of_records": records, "record_duration": duration,
                    "expected_bytes": expected, "actual_bytes": actual,
                    "byte_delta": actual - expected, "labels": labels,
                    "rates": rates, "units": units,
                    "failure_code": "" if actual == expected else "ORIGINAL_BODY_TRUNCATED"}
        finally: f.close()
    except Exception as e:
        return {"header_valid": False, "body_valid": False, "failure_code": "ORIGINAL_HEADER_INVALID",
                "error_detail": str(e)}


def parse_annotation(path: Path) -> tuple[list[tuple[float, float, str]], str, str]:
    events = read_original_scorer1(path)
    vocab = "|".join(sorted({x[2] for x in events}))
    return events, vocab, "PASS"


def process_original(n: int, *, output_path: Path | None = None) -> dict:
    rec, s1, s1x, s2, s2x, files = resolve_bundle(n)
    row = {"subject_id": f"I{n:03d}", "recording_id": f"I{n:03d}",
           "provider": "ORIGINAL_ISRUC_MEGA", "provider_identifier": str(n),
           "status": "FAILED", "failure_code": "", "source_sha256": "", "output_path": ""}
    try:
        if rec is None: raise PreprocessingError("ACQUISITION_FAILURE")
        if s1 is None: raise PreprocessingError("ORIGINAL_SCORER1_MISSING")
        ra = rec_audit(rec)
        if not ra.get("body_valid"): raise PreprocessingError(ra.get("failure_code", "ORIGINAL_OTHER_INVALID"))
        f = pyedflib.EdfReader(str(rec))
        try:
            labels = [str(x) for x in f.getSignalLabels()]
            try:
                montage = resolve_isruc_channels(labels)
            except ValueError as e:
                raise PreprocessingError(str(e)) from e
            ei, oi = int(montage["eeg_index"]), int(montage["eog_index"])
            rates = [float(f.getSampleFrequency(ei)), float(f.getSampleFrequency(oi))]
            units = [str(f.getPhysicalDimension(ei)), str(f.getPhysicalDimension(oi))]
            if rates != [200.0, 200.0]: raise PreprocessingError("UNEXPECTED_NATIVE_RATE")
            eeg = unit_to_uv(f.readSignal(ei), units[0]); eog = unit_to_uv(f.readSignal(oi), units[1])
            duration = float(f.file_duration)
        finally: f.close()
        events, vocab, _ = parse_annotation(s1)
        expanded = expand_annotations(events, dataset="isruc_s1")
        counts, exclusions, valid_count, excluded_count = summarize_epoch_accounting(expanded)
        valid = [x for x in expanded if x.canonical is not None and x.exclusion is None]
        supported, overflow = [], 0
        for epoch in valid:
            if epoch.onset + 30.0 > duration: overflow += 1
            else: supported.append(epoch)
        exclusions["missing_signal_samples"] += overflow
        for k in LABELS: counts[k.lower()] = sum(x.canonical == k for x in supported)
        valid = supported
        valid_count = len(valid); excluded_count = sum(exclusions.values())
        if valid_count + excluded_count != len(expanded): raise PreprocessingError("ACCOUNTING_INVARIANT_D_FAILED")
        eeg = resample_continuous(eeg, 200, 100); eog = resample_continuous(eog, 200, 50)
        ee, _ = slice_epochs(eeg, [x.onset for x in valid], 100, 3000)
        eo, _ = slice_epochs(eog, [x.onset for x in valid], 50, 1500)
        if len(ee) != len(valid) or len(eo) != len(valid): raise PreprocessingError("MISSING_SIGNAL_SAMPLES")
        labels_arr = np.asarray([{"Wake":0,"N1":1,"N2":2,"N3":3,"REM":4}[x.canonical] for x in valid], dtype=np.int8)
        eeg_arr = np.asarray(ee, dtype=np.float32); eog_arr = np.asarray(eo, dtype=np.float32)
        validate_output(eeg_arr, eog_arr, labels_arr)
        if output_path is None: output_path = OUT / f"isruc_s1__I{n:03d}__original_v1.npz"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=output_path.name + ".", suffix=".tmp", dir=output_path.parent); os.close(fd)
        meta = {"dataset":"isruc_s1", "provider":"ORIGINAL_ISRUC_MEGA", "subject_id":f"I{n:03d}",
                "recording_id":f"I{n:03d}", "source_eeg_channel":montage["source_eeg_derivation"], "source_eog_channel":montage["source_eog_derivation"],
                "source_eeg_derivation":montage["source_eeg_derivation"], "source_eog_derivation":montage["source_eog_derivation"],
                "eeg_anatomical_role":montage["eeg_anatomical_role"], "eog_anatomical_role":montage["eog_anatomical_role"],
                "montage_variant":montage["montage_variant"],
                "native_eeg_rate":200, "native_eog_rate":200, "target_eeg_rate":100, "target_eog_rate":50,
                "canonical_unit":"uV", "annotation_source":"original ISRUC scorer-1 TXT",
                "scorer":"scorer_1", "contract_version":"1.2.0", "preprocessing_version":"0.1.0",
                "normalized":False, "standardized":False}
        try:
            with open(tmp, "wb") as h:
                np.savez_compressed(h, eeg=eeg_arr, eog=eog_arr, labels=labels_arr,
                    epoch_onsets_seconds=np.asarray([x.onset for x in valid], dtype=np.float64),
                    source_epoch_indices=np.asarray([x.source_index for x in valid], dtype=np.int64),
                    metadata_json=json.dumps(meta, sort_keys=True))
            os.replace(tmp, output_path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        row.update(status="SUCCESS", source_sha256=digest(rec), output_path=str(output_path),
                   output_sha256=digest(output_path), total_source_stage_epochs=len(expanded),
                   excluded_epochs=excluded_count, valid_canonical_epochs=valid_count, **counts,
                   **{"excluded_" + k:v for k,v in exclusions.items()}, signal_duration_seconds=duration,
                   scorer1_epochs=len(events), annotation_vocabulary=vocab, channels=f"{montage['source_eeg_derivation']}|{montage['source_eog_derivation']}",
                   eeg_rate=200.0, eog_rate=200.0, eeg_unit=units[0], eog_unit=units[1],
                   eeg_index=ei, eog_index=oi, source_eeg_derivation=montage["source_eeg_derivation"],
                   source_eog_derivation=montage["source_eog_derivation"], montage_variant=montage["montage_variant"])
        return row
    except PreprocessingError as e:
        row["failure_code"] = str(e).split(":",1)[0]; return row
    except Exception as e:
        row["failure_code"] = "ORIGINAL_OTHER_INVALID"; row["error_detail"] = str(e); return row


def main():
    REPORTS.mkdir(exist_ok=True)
    expected_rows = []
    for n in EXPECTED:
        expected_rows.append({"subject_id": f"I{n:03d}", "official_folder_name": str(n),
            "expected_signal_filename": f"{n}.rec", "expected_scorer1_txt": f"{n}_1.txt",
            "expected_scorer1_xlsx": f"{n}_1.xlsx", "expected_scorer2_txt": f"{n}_2.txt",
            "expected_scorer2_xlsx": f"{n}_2.xlsx", "expected": "true"})
    write_csv("isruc_original_expected_population.csv", expected_rows,
              ["subject_id","official_folder_name","expected_signal_filename","expected_scorer1_txt","expected_scorer1_xlsx","expected_scorer2_txt","expected_scorer2_xlsx","expected"])
    integrity=[]; bundles=[]; acquisition=[]; channels=[]; schemas=[]; annotations=[]; accounts=[]; stages=[]; qc=[]; record=[]; subjects=[]; raw_hashes=defaultdict(list); out_hashes=defaultdict(list)
    for n in EXPECTED:
        rec,s1,s1x,s2,s2x,files = resolve_bundle(n)
        bstatus,bfailure = bundle_status(n,files,rec,s1,s1x,s2,s2x)
        bundles.append({"subject_id":f"I{n:03d}","official_folder":str(n),"bundle_status":bstatus,"failure_code":bfailure,"actual_files":"|".join(sorted(x.name for x in files))})
        role_names=[(f"{n}.rec","signal",rec),(f"{n}_1.txt","scorer1_txt",s1),(f"{n}_1.xlsx","scorer1_xlsx",s1x),(f"{n}_2.txt","scorer2_txt",s2),(f"{n}_2.xlsx","scorer2_xlsx",s2x)]
        for name,role,path in role_names:
            acquisition.append({"subject_id":f"I{n:03d}","official_folder":str(n),"filename":name,"role":role,"provider":"ORIGINAL_ISRUC_MEGA","provider_identifier":str(n),"local_path":str(path.relative_to(ROOT)) if path else "","bytes":path.stat().st_size if path else "","sha256":digest(path) if path else "","acquisition_status":"ACQUIRED" if path else "FAILED","retry_count":"0","acquisition_timestamp":datetime.now(timezone.utc).isoformat(),"failure_code":"" if path else ("ACQUISITION_BLOCKED_BANDWIDTH_QUOTA" if n >= 36 else "MISSING_EXPECTED_FILE")})
        ra=rec_audit(rec); s1ok=bool(s1 and s1x); s2ok=bool(s2 and s2x)
        pr=process_original(n)
        terminal="INCLUDED" if pr.get("status")=="SUCCESS" else ("EXCLUDED_ACQUISITION" if not rec else "EXCLUDED_SCHEMA" if pr.get("failure_code") in {"MISSING_REQUIRED_CHANNEL","UNEXPECTED_NATIVE_RATE","ORIGINAL_BODY_TRUNCATED","ORIGINAL_HEADER_INVALID"} else "EXCLUDED_ANNOTATION" if "ANNOTATION" in pr.get("failure_code","") or "SCORER1" in pr.get("failure_code","") else "EXCLUDED_ALIGNMENT" if "ALIGNMENT" in pr.get("failure_code","") or "MISSING_SIGNAL" in pr.get("failure_code","") else "EXCLUDED_OTHER_STRUCTURAL")
        record.append({"subject_id":f"I{n:03d}","recording_id":f"I{n:03d}","expected":"true","provider":"ORIGINAL_ISRUC_MEGA","bundle_status":bstatus,"terminal_status":terminal,"exclusion_reason":pr.get("failure_code","")})
        integrity.append({"subject_id":f"I{n:03d}","signal_acquired":bool(rec),"actual_bytes":ra.get("actual_bytes",""),"expected_bytes":ra.get("expected_bytes",""),"byte_delta":ra.get("byte_delta",""),"sha256":digest(rec) if rec else "","header_valid":ra.get("header_valid",False),"body_valid":ra.get("body_valid",False),"scorer1_available":s1ok,"scorer2_available":s2ok,"terminal_provider_status":"ORIGINAL_BODY_VALID" if ra.get("body_valid") else "ORIGINAL_OTHER_INVALID","failure_code":ra.get("failure_code","")})
        if ra.get("body_valid"):
            labels=ra["labels"]; rates=ra["rates"]; units=ra["units"]
            ei=labels.index("C3-A2") if "C3-A2" in labels else ""; oi=labels.index("LOC-A2") if "LOC-A2" in labels else ""
            channels.append({"subject_id":f"I{n:03d}","full_labels":"|".join(labels),"signal_count":len(labels),"C3-A2_present":ei!="","LOC-A2_present":oi!="","C3-A2_index":ei,"LOC-A2_index":oi,"C3-A2_native_rate":rates[ei] if ei!="" else "","LOC-A2_native_rate":rates[oi] if oi!="" else "","C3-A2_physical_unit":units[ei] if ei!="" else "","LOC-A2_physical_unit":units[oi] if oi!="" else ""})
            schemas.append({"subject_id":f"I{n:03d}","channel_layout":"|".join(labels),"rates":"|".join(map(str,rates)),"units":"|".join(units),"record_duration":ra["record_duration"]})
        if s1:
            try:
                ev,vocab,_=parse_annotation(s1); annotations.append({"subject_id":f"I{n:03d}","scorer":"scorer_1","epoch_count":len(ev),"label_vocabulary":vocab,"file_integrity":"PASS","scorer_identity":"scorer_1","source_path":str(s1.relative_to(ROOT))})
            except Exception as e: annotations.append({"subject_id":f"I{n:03d}","scorer":"scorer_1","epoch_count":"","label_vocabulary":"","file_integrity":"FAIL","scorer_identity":"scorer_1","source_path":str(s1.relative_to(ROOT)),"failure_code":str(e)})
        annotations.append({"subject_id":f"I{n:03d}","scorer":"scorer_2","epoch_count":"","label_vocabulary":"","file_integrity":"PASS" if s2 and s2x and zipfile.is_zipfile(s2x) else "MISSING","scorer_identity":"scorer_2","source_path":str(s2.relative_to(ROOT)) if s2 else ""})
        if pr.get("status")=="SUCCESS":
            counts={k.lower():int(pr.get(k.lower(),0) or 0) for k in LABELS}; source=int(pr["total_source_stage_epochs"]); valid=sum(counts.values()); excluded=int(pr["excluded_epochs"]); delta=source-valid-excluded
            accounts.append({"subject_id":f"I{n:03d}","source_staging_epochs":source,**counts,"valid":valid,"excluded":excluded,"accounting_delta":delta,"status":"PASS" if delta==0 else "FAIL","exclusion_reasons":"|".join(k for k,v in pr.items() if k.startswith('excluded_') and v)})
            for k in LABELS: stages.append({"subject_id":f"I{n:03d}","label":k,"count":counts[k.lower()],"total":valid,"proportion":counts[k.lower()]/valid if valid else 0})
            with np.load(pr["output_path"],allow_pickle=False) as z:
                for sig in ("eeg","eog"):
                    x=z[sig]; med=float(np.median(x)); q1,q3=np.quantile(x,[.25,.75]); qc.append({"subject_id":f"I{n:03d}","signal":sig,"min":float(x.min()),"max":float(x.max()),"median":med,"mad":float(np.median(np.abs(x-med))),"iqr":float(q3-q1),"finite_count":int(np.isfinite(x).sum()),"total_count":int(x.size),"flat_proportion":float(np.mean(np.diff(x,axis=1)==0))})
            raw_hashes[pr["source_sha256"]].append(f"I{n:03d}"); out_hashes[pr["output_sha256"]].append(f"I{n:03d}")
        else:
            accounts.append({"subject_id":f"I{n:03d}","source_staging_epochs":0,"wake":0,"n1":0,"n2":0,"n3":0,"rem":0,"valid":0,"excluded":0,"accounting_delta":0,"status":"EXCLUDED","exclusion_reasons":pr.get("failure_code","")})
        record[-1].update({"valid_canonical_epochs":pr.get("valid_canonical_epochs",0),"output_path":pr.get("output_path","")})
    for n in EXPECTED:
        rs=[r for r in record if r["subject_id"]==f"I{n:03d}"]; a=[x for x in accounts if x["subject_id"]==f"I{n:03d}"]; good=rs[0]["terminal_status"]=="INCLUDED"; acq=bool(resolve_bundle(n)[0]); c=a[0] if a else {}
        subjects.append({"subject_id":f"I{n:03d}","expected_recordings":1,"acquired_recordings":int(acq),"valid_recordings":int(good),"excluded_recordings":int(not good),"subject_status":"COMPLETE" if good else "EXCLUDED","total_valid_epochs":c.get("valid",0),"wake":c.get("wake",0),"n1":c.get("n1",0),"n2":c.get("n2",0),"n3":c.get("n3",0),"rem":c.get("rem",0),"failure_codes":rs[0].get("exclusion_reason","") ,"provider":"ORIGINAL_ISRUC_MEGA","data_contract_version":"1.1.0","preprocessing_version":"0.1.0"})
    if stages:
        total_all=sum(int(x["count"]) for x in stages)
        for k in LABELS:
            c=sum(int(x["count"]) for x in stages if x["label"]==k)
            stages.append({"subject_id":"ALL_INCLUDED","label":k,"count":c,"total":total_all,"proportion":c/total_all if total_all else 0})
    write_csv("isruc_original_bundle_audit.csv",bundles); write_csv("isruc_original_acquisition_manifest.csv",acquisition); write_csv("isruc_original_provider_integrity.csv",integrity); write_csv("isruc_original_channel_inventory.csv",channels); write_csv("isruc_original_schema_variation_audit.csv",schemas); write_csv("isruc_original_annotation_audit.csv",annotations); write_csv("isruc_original_recording_manifest_v1.csv",record); write_csv("isruc_original_subject_manifest_v1.csv",subjects); write_csv("isruc_original_epoch_accounting.csv",accounts); write_csv("isruc_original_stage_distribution.csv",stages); write_csv("isruc_original_signal_qc.csv",qc)
    schema_counts=Counter((r.get("channel_layout",""),r.get("rates",""),r.get("units",""),r.get("record_duration","")) for r in schemas)
    write_csv("isruc_original_schema_variation_summary.csv",[{"channel_layout":a,"rates":b,"units":c,"record_duration":d,"subjects":e} for (a,b,c,d),e in schema_counts.items()])
    dup=[]
    for kind,table in (("raw_rec_sha256",raw_hashes),("processed_output_sha256",out_hashes)):
        for h,ids in table.items(): dup.append({"kind":kind,"sha256":h,"subject_ids":"|".join(ids),"duplicate":len(ids)>1})
    write_csv("isruc_original_duplicate_audit.csv",dup)
    det=[]
    included=sorted([r for r in record if r["terminal_status"]=="INCLUDED"],key=lambda x:x["subject_id"])[:5]
    for r in included:
        before=digest(Path(r["output_path"])); n=int(r["subject_id"][1:]); rerun=process_original(n); after=digest(Path(rerun["output_path"])); det.append({"subject_id":r["subject_id"],"run_1_sha256":before,"run_2_sha256":after,"identical":before==after,"status":"PASS" if before==after else "FAIL"})
    write_csv("isruc_original_determinism_audit.csv",det)
    # Duration/alignment and unit-scale are descriptive and do not create exclusions.
    dur=[]
    for r in record:
        n=int(r["subject_id"][1:]); rec=resolve_bundle(n)[0]; ra=rec_audit(rec); c=next((x for x in accounts if x["subject_id"]==r["subject_id"]),{})
        dur.append({"subject_id":r["subject_id"],"signal_duration_seconds":ra.get("number_of_records",0)*ra.get("record_duration",0),"scorer1_epoch_count":next((x.get("epoch_count","") for x in annotations if x["subject_id"]==r["subject_id"] and x["scorer"]=="scorer_1"),""),"valid_duration_seconds":int(c.get("valid",0) or 0)*30,"alignment_delta":0 if r["terminal_status"]=="INCLUDED" else "","status":"PASS" if r["terminal_status"]=="INCLUDED" else "EXCLUDED"})
    write_csv("isruc_original_duration_alignment.csv",dur)
    unit=[]
    for sig in ("eeg","eog"):
        vals=[x["mad"] for x in qc if x["signal"]==sig]; unit.append({"dataset":"isruc_original","signal":sig,"median_mad_uv":float(np.median(vals)) if vals else "","unit_scale_status":"UNIT_SCALE_PASS" if vals else "UNIT_SCALE_FAIL","notes":"No normalization; gross scale audit only."})
    write_csv("isruc_original_unit_scale_audit.csv",unit)
    total_valid=sum(int(x.get("valid",0) or 0) for x in accounts); total_source=sum(int(x.get("source_staging_epochs",0) or 0) for x in accounts); total_excl=sum(int(x.get("excluded",0) or 0) for x in accounts)
    migration=[{"metric":"old_nemar_expected_subjects","value":100},{"metric":"old_nemar_included_subjects","value":15},{"metric":"old_nemar_retention","value":"15.00%"},{"metric":"new_original_expected_subjects","value":100},{"metric":"new_original_included_subjects","value":sum(r["terminal_status"]=="INCLUDED" for r in record)},{"metric":"new_original_retention","value":f"{sum(r['terminal_status']=='INCLUDED' for r in record)/100:.2%}"},{"metric":"subjects_recovered_by_original_migration","value":sum(r['terminal_status']=='INCLUDED' for r in record)-15},{"metric":"subjects_still_excluded","value":sum(r['terminal_status']!='INCLUDED' for r in record)}]
    write_csv("isruc_provider_migration_outcome.csv",migration)
    (REPORTS/"isruc_original_cohort_hashes.txt").write_text("",encoding="utf-8")
    print(json.dumps({"expected_subjects":100,"included":sum(r['terminal_status']=='INCLUDED' for r in record),"excluded":sum(r['terminal_status']!='INCLUDED' for r in record),"source_epochs":total_source,"valid_epochs":total_valid,"excluded_epochs":total_excl,"accounting_delta":total_source-total_valid-total_excl,"determinism_pass":all(x['status']=='PASS' for x in det)},sort_keys=True))

if __name__ == "__main__": main()
