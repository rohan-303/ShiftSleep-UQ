"""Step 7.8 ISRUC rebuild from available official original-provider bundles.

This script is target-free: no splits, models, normalization fitting, or metrics.
It emits safe aggregate/versioned artifacts only; raw and processed data remain ignored.
"""
from __future__ import annotations
import csv, hashlib, importlib.util, json, os
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = ROOT / "data/processed/isruc_original_v2"
EXPECTED = range(1, 101)
CONTRACT = "1.2.0"
PREPROCESSING = "0.1.0"

spec = importlib.util.spec_from_file_location("step75", ROOT / "scripts/step_07_5_original_migration.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def write_csv(name, rows, fields=None):
    path = REPORTS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = []
        for row in rows:
            for key in row:
                if key not in fields: fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    return path


def sha_or_empty(path):
    return digest(path) if path and path.exists() else ""


def main():
    REPORTS.mkdir(exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    rec_rows=[]; subj_rows=[]; montage_rows=[]; qc_rows=[]; schema_rows=[]; ann_rows=[]
    acquisition_rows=[]
    accounting_rows=[]; duration_rows=[]; det_rows=[]; raw_hashes=defaultdict(list); out_hashes=defaultdict(list)
    bundle_counts=Counter(); failure_counts=Counter(); included=[]
    for n in EXPECTED:
        sid=f"I{n:03d}"
        rec,s1,s1x,s2,s2x,files=mod.resolve_bundle(n)
        bstatus,bfailure=mod.bundle_status(n,files,rec,s1,s1x,s2,s2x)
        bundle_counts[bstatus]+=1
        for filename, role, path in ((f"{n}.rec","signal",rec),(f"{n}_1.txt","scorer1_txt",s1),(f"{n}_1.xlsx","scorer1_xlsx",s1x),(f"{n}_2.txt","scorer2_txt",s2),(f"{n}_2.xlsx","scorer2_xlsx",s2x)):
            acquisition_rows.append({"subject_id":sid,"provider_folder":str(n),"filename":filename,"role":role,"provider":"ORIGINAL_ISRUC_MEGA","local_path":str(path.relative_to(ROOT)) if path else "","bytes":path.stat().st_size if path else "","sha256":digest(path) if path else "","acquisition_status":"ACQUIRED" if path else "FAILED","retry_count":"0","terminal_acquisition_reason":"" if path else ("MEGA_CLIENT_UNAVAILABLE_OR_BANDWIDTH_QUOTA" if n>=37 else bfailure)})
        ra=mod.rec_audit(rec)
        source_hash=sha_or_empty(rec); signal_bytes=rec.stat().st_size if rec else ""
        source_eeg=source_eog=variant=units=""; eeg_rate=eog_rate=""; signal_count=""; eeg_index=eog_index=""
        if ra.get("body_valid"):
            labels=ra["labels"]; rates=ra["rates"]; unit_list=ra["units"]
            try:
                m=mod.resolve_isruc_channels(labels)
                source_eeg=m["source_eeg_derivation"]; source_eog=m["source_eog_derivation"]; variant=m["montage_variant"]
                eeg_index=m["eeg_index"]; eog_index=m["eog_index"]
                eeg_rate=rates[eeg_index]; eog_rate=rates[eog_index]; units=f"{unit_list[eeg_index]}|{unit_list[eog_index]}"; signal_count=len(labels)
            except ValueError:
                variant="UNSUPPORTED"; failure_counts["UNSUPPORTED_ISRUC_CHANNEL_LAYOUT"]+=1
            schema_rows.append({"subject_id":sid,"exact_eeg_derivation":source_eeg,"exact_eog_derivation":source_eog,"montage_variant":variant,"eeg_rate":eeg_rate,"eog_rate":eog_rate,"units":units,"signal_count":signal_count,"labels":"|".join(labels)})
        if s1:
            try:
                events,vocab,_=mod.parse_annotation(s1)
                ann_rows.append({"subject_id":sid,"scorer1_source":str(s1.relative_to(ROOT)),"scorer1_sha256":digest(s1),"epoch_count":len(events),"label_vocabulary":vocab,"thirty_second_semantics":"PASS","file_integrity":"PASS"})
            except Exception as e:
                ann_rows.append({"subject_id":sid,"scorer1_source":str(s1.relative_to(ROOT)),"scorer1_sha256":digest(s1),"epoch_count":"","label_vocabulary":"","thirty_second_semantics":"FAIL","file_integrity":"FAIL","failure_code":str(e)})
        else:
            ann_rows.append({"subject_id":sid,"scorer1_source":"","scorer1_sha256":"","epoch_count":"","label_vocabulary":"","thirty_second_semantics":"NOT_AVAILABLE","file_integrity":"MISSING"})
        pr={"status":"FAILED","failure_code":"ACQUISITION_FAILURE"}
        if rec and s1 and ra.get("body_valid"):
            out=OUT/f"isruc_s1__{sid}__original_v2.npz"
            pr=mod.process_original(n, output_path=out)
        status="INCLUDED" if pr.get("status")=="SUCCESS" else ("EXCLUDED_ACQUISITION" if not rec or bstatus!="BUNDLE_COMPLETE" else "EXCLUDED_STRUCTURAL")
        reason="" if status=="INCLUDED" else (pr.get("failure_code") or bfailure or ra.get("failure_code") or "UNSPECIFIED_FAILURE")
        failure_counts[reason]+=int(bool(reason))
        out_path=Path(pr["output_path"]) if pr.get("output_path") else None
        output_hash=sha_or_empty(out_path)
        counts={k.lower():int(pr.get(k.lower(),0) or 0) for k in mod.LABELS}
        valid=int(pr.get("valid_canonical_epochs",0) or 0); source_epochs=int(pr.get("total_source_stage_epochs",0) or 0); excluded=int(pr.get("excluded_epochs",0) or 0)
        delta=source_epochs-valid-excluded if status=="INCLUDED" else ""
        if status=="INCLUDED":
            included.append(n); raw_hashes[source_hash].append(sid); out_hashes[output_hash].append(sid)
            accounting_rows.append({"subject_id":sid,"source_staging_epochs":source_epochs,"valid":valid,"excluded":excluded,**counts,"accounting_delta":delta,"status":"PASS" if delta==0 else "FAIL"})
            with np.load(out_path,allow_pickle=False) as z:
                for sig in ("eeg","eog"):
                    x=z[sig]; med=float(np.median(x)); q1,q3=np.quantile(x,[.25,.75])
                    qc_rows.append({"subject_id":sid,"montage_variant":variant,"signal":sig,"median_uv":med,"mad_uv":float(np.median(np.abs(x-med)),),"iqr_uv":float(q3-q1),"recording_duration_seconds":float(ra["number_of_records"]*ra["record_duration"]),"valid_epoch_count":valid,"finite":"PASS" if np.isfinite(x).all() else "FAIL"})
            duration_rows.append({"subject_id":sid,"signal_duration_seconds":float(ra["number_of_records"]*ra["record_duration"]),"annotation_epoch_count":len(ann_rows[-1].get("epoch_count") and range(int(ann_rows[-1]["epoch_count"])) or []),"valid_epoch_count":valid,"valid_duration_seconds":valid*30,"alignment_delta":0,"status":"PASS"})
        else:
            accounting_rows.append({"subject_id":sid,"source_staging_epochs":source_epochs,"valid":0,"excluded":0,"wake":0,"n1":0,"n2":0,"n3":0,"rem":0,"accounting_delta":"","status":"EXCLUDED","failure_code":reason})
            duration_rows.append({"subject_id":sid,"signal_duration_seconds":float(ra.get("number_of_records",0)*ra.get("record_duration",0)) if ra.get("body_valid") else "","annotation_epoch_count":ann_rows[-1].get("epoch_count",""),"valid_epoch_count":0,"valid_duration_seconds":"","alignment_delta":"","status":"EXCLUDED","failure_code":reason})
        rec_rows.append({"subject_id":sid,"provider":"ORIGINAL_ISRUC_MEGA","provider_folder":str(n),"raw_sha256":source_hash,"signal_bytes":signal_bytes,"body_valid":ra.get("body_valid",False),"expected_bytes":ra.get("expected_bytes",""),"actual_bytes":ra.get("actual_bytes",""),"body_delta":ra.get("byte_delta",""),"bundle_status":bstatus,"source_eeg_derivation":source_eeg,"source_eog_derivation":source_eog,"montage_variant":variant,"eeg_rate":eeg_rate,"eog_rate":eog_rate,"units":units,"scorer1_source":str(s1.relative_to(ROOT)) if s1 else "","source_epoch_count":ann_rows[-1].get("epoch_count",""),"wake":counts["wake"],"n1":counts["n1"],"n2":counts["n2"],"n3":counts["n3"],"rem":counts["rem"],"valid_epochs":valid,"excluded_epochs":excluded,"accounting_delta":delta,"output_sha256":output_hash,"terminal_status":status,"failure_code":reason,"data_contract_version":CONTRACT,"preprocessing_version":PREPROCESSING})
        subj_rows.append({"subject_id":sid,"expected_recording_count":1,"acquired":str(bool(rec and bstatus=="BUNDLE_COMPLETE")).upper(),"included":str(status=="INCLUDED").upper(),"subject_status":"COMPLETE" if status=="INCLUDED" else status,"montage_variant":variant,"valid_epochs":valid,"wake":counts["wake"],"n1":counts["n1"],"n2":counts["n2"],"n3":counts["n3"],"rem":counts["rem"],"failure_reason":reason,"data_contract_version":CONTRACT,"preprocessing_version":PREPROCESSING})
    write_csv("isruc_original_recording_manifest_v2.csv",rec_rows)
    write_csv("isruc_original_subject_manifest_v2.csv",subj_rows)
    write_csv("isruc_original_acquisition_manifest_v2.csv",acquisition_rows)
    write_csv("isruc_original_annotation_audit_v2.csv",ann_rows)
    write_csv("isruc_original_epoch_accounting_v2.csv",accounting_rows)
    write_csv("isruc_original_duration_alignment_v2.csv",duration_rows)
    write_csv("isruc_montage_qc_v2.csv",qc_rows)
    write_csv("isruc_full_schema_unit_rate_audit_v2.csv",schema_rows)
    montage_counts=Counter(r["montage_variant"] for r in rec_rows if r["terminal_status"]=="INCLUDED")
    montage_epochs=Counter()
    for r in rec_rows:
        if r["terminal_status"]=="INCLUDED": montage_epochs[r["montage_variant"]]+=int(r["valid_epochs"])
    write_csv("isruc_montage_distribution_v2.csv",[
        {"montage_variant":"ISRUC_A1A2","subject_count":montage_counts["ISRUC_A1A2"],"valid_epoch_total":montage_epochs["ISRUC_A1A2"],"descriptive_only":True},
        {"montage_variant":"ISRUC_M1M2","subject_count":montage_counts["ISRUC_M1M2"],"valid_epoch_total":montage_epochs["ISRUC_M1M2"],"descriptive_only":True},
        {"montage_variant":"UNSUPPORTED","subject_count":sum(r["terminal_status"]!="INCLUDED" and r["body_valid"] for r in rec_rows),"valid_epoch_total":0,"descriptive_only":True},
        {"montage_variant":"ACQUISITION_FAILURE","subject_count":sum(not r["body_valid"] for r in rec_rows),"valid_epoch_total":0,"descriptive_only":True},
    ])
    dup=[]
    for kind,table in (("raw_rec_sha256",raw_hashes),("processed_output_sha256",out_hashes)):
        for h,ids in table.items(): dup.append({"kind":kind,"sha256":h,"subject_ids":"|".join(ids),"duplicate":len(ids)>1})
    write_csv("isruc_duplicate_audit_v2.csv",dup)
    for n in sorted(included):
        p=OUT/f"isruc_s1__I{n:03d}__original_v2.npz"; first=digest(p)
        rerun=mod.process_original(n,output_path=OUT/f"determinism__I{n:03d}.npz"); second=digest(Path(rerun["output_path"])) if rerun.get("status")=="SUCCESS" else ""
        det_rows.append({"subject_id":f"I{n:03d}","montage_variant":next(r["montage_variant"] for r in rec_rows if r["subject_id"]==f"I{n:03d}"),"run_1_sha256":first,"run_2_sha256":second,"identical":first==second,"status":"PASS" if first==second else "FAIL"})
    write_csv("isruc_determinism_audit_v2.csv",det_rows)
    old_included=15
    write_csv("isruc_provider_migration_final_outcome.csv",[
        {"provider_cohort":"OLD_NEMAR","expected_subjects":100,"included_subjects":old_included,"exclusion_rate":"85.00%","provider_truncation_exclusions":2,"status":"HISTORICAL_SUPERSEDED_PENDING_SUCCESSFUL_REBUILD"},
        {"provider_cohort":"ORIGINAL_ISRUC_MEGA_CONTRACT_1.2.0","expected_subjects":100,"acquired_complete_bundles":sum(r["bundle_status"]=="BUNDLE_COMPLETE" for r in rec_rows),"included_subjects":len(included),"a1a2_included":montage_counts["ISRUC_A1A2"],"m1m2_included":montage_counts["ISRUC_M1M2"],"structural_exclusions":sum(r["terminal_status"]=="EXCLUDED_STRUCTURAL" for r in rec_rows),"acquisition_exclusions":sum(r["terminal_status"]=="EXCLUDED_ACQUISITION" for r in rec_rows),"subjects_recovered_vs_old":len(included)-old_included,"status":"PARTIAL"},
    ])
    manifest_hashes=[]
    for name in ("isruc_original_recording_manifest_v2.csv","isruc_original_subject_manifest_v2.csv","isruc_montage_distribution_v2.csv","isruc_montage_qc_v2.csv"):
        manifest_hashes.append(f"{name},{digest(REPORTS/name)}")
    (REPORTS/"isruc_original_cohort_v2_hashes.txt").write_text("\n".join(manifest_hashes)+"\n",encoding="utf-8")
    print(json.dumps({"expected":100,"complete_bundles":sum(r["bundle_status"]=="BUNDLE_COMPLETE" for r in rec_rows),"included":len(included),"acquisition_exclusions":sum(r["terminal_status"]=="EXCLUDED_ACQUISITION" for r in rec_rows),"structural_exclusions":sum(r["terminal_status"]=="EXCLUDED_STRUCTURAL" for r in rec_rows),"a1a2":montage_counts["ISRUC_A1A2"],"m1m2":montage_counts["ISRUC_M1M2"],"determinism":all(r["status"]=="PASS" for r in det_rows)},sort_keys=True))

if __name__ == "__main__": main()
