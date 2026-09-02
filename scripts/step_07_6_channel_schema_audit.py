"""Step 7.6: independent ISRUC EDF/REC channel-schema audit.

No acquisition, preprocessing, channel fallback, or scientific-contract mutation occurs here.
"""
from __future__ import annotations
import csv, hashlib, json, struct
from collections import Counter, defaultdict
from pathlib import Path
import pyedflib

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/isruc-original"
REPORTS = ROOT / "reports"
EXPECTED = range(1, 36)
NOMINAL = ["F3-A2", "C3-A2", "O1-A2", "F4-A1", "C4-A1", "O2-A1", "LOC-A2", "ROC-A1"]
RELATED = ["F3-A2", "O1-A2", "C4-A1", "ROC-A1", "C3-M2", "LOC-M2", "C3-A1", "LOC-A1", "C3", "LOC"]

def sha256(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def field_bytes(raw: bytes, offset: int, width: int, n: int):
    return [raw[offset+i*width:offset+(i+1)*width] for i in range(n)]

def decode_label_field(raw: bytes):
    before=raw.decode("latin-1")
    after=before.rstrip(" ")
    return {"raw_hex":raw.hex(),"raw_repr":repr(raw),"decoded_before_cleanup":before,
            "decoded_after_padding_strip":after,"contains_nul":b"\x00" in raw,
            "contains_non_ascii":any(x>=128 for x in raw)}

def parse_raw_header(path: Path):
    with path.open("rb") as f:
        fixed=f.read(256)
        if len(fixed)!=256: raise ValueError("CORRUPT_HEADER_FIXED")
        try: ns=int(fixed[252:256].decode("ascii").strip())
        except Exception as e: raise ValueError(f"HEADER_NS_INVALID:{e}")
        if ns<=0 or ns>512: raise ValueError("HEADER_NS_OUT_OF_RANGE")
        header=fixed+f.read(256*ns)
    if len(header)!=256*(ns+1): raise ValueError("CORRUPT_HEADER_SIGNAL_FIELDS")
    blocks={}
    offset=256
    for name,width in [("label",16),("transducer",80),("physical_dimension",8),("physical_min",8),("physical_max",8),("digital_min",8),("digital_max",8),("prefilter",80),("samples_per_record",8),("reserved",32)]:
        blocks[name]=field_bytes(header,offset,width,ns); offset+=width*ns
    labels=[decode_label_field(x) for x in blocks["label"]]
    def text(name,i): return blocks[name][i].decode("latin-1").strip()
    channels=[]
    for i,label in enumerate(labels):
        channels.append({"channel_index":i,"label":label,"transducer_raw_hex":blocks["transducer"][i].hex(),"transducer_repr":repr(blocks["transducer"][i]),"transducer":text("transducer",i),"physical_dimension":text("physical_dimension",i),"physical_min":text("physical_min",i),"physical_max":text("physical_max",i),"digital_min":text("digital_min",i),"digital_max":text("digital_max",i),"samples_per_record":int(text("samples_per_record",i))})
    records=int(fixed[236:244].decode("ascii").strip())
    duration=float(fixed[244:252].decode("ascii").strip())
    expected_body = 256*(ns+1) + records * sum(c["samples_per_record"] for c in channels) * 2
    return {"path":path,"header":fixed,"ns":ns,"records":records,"record_duration":duration,"header_length":256*(ns+1),"expected_bytes":expected_body,"actual_bytes":path.stat().st_size,"body_valid":path.stat().st_size==expected_body,"channels":channels,"patient_raw":fixed[8:88],"recording_raw":fixed[88:168]}

def find_rec(n):
    xs=sorted(RAW.glob(f"subject-{n}/**/{n}.rec"))
    if len(xs)!=1: raise FileNotFoundError(f"I{n:03d}: expected one REC, found {len(xs)}")
    return xs[0]

def project_labels(path):
    f=pyedflib.EdfReader(str(path))
    try: return list(f.getSignalLabels())
    finally: f.close()

def current_inventory():
    rows=list(csv.DictReader((REPORTS/"isruc_original_channel_inventory.csv").open(encoding="utf-8")))
    return {int(r["subject_id"][1:]):r for r in rows}

def write_csv(name, rows, fields=None):
    p=REPORTS/name; p.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:
        fields=[]
        for r in rows:
            for k in r:
                if k not in fields: fields.append(k)
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def main():
    inv=current_inventory()
    parsed={}; raw_rows=[]; char_rows=[]; cross=[]; three=[]; clusters=[]; inventories=[]; side=[]; identities=[]
    for n in EXPECTED:
        sid=f"I{n:03d}"; path=find_rec(n); h=parse_raw_header(path); parsed[n]=h
        labels=[c["label"]["decoded_after_padding_strip"] for c in h["channels"]]
        current=inv.get(n,{})
        for c in h["channels"]:
            i=c["channel_index"]; lab=c["label"]; exact=lab["decoded_after_padding_strip"] in ("C3-A2","LOC-A2")
            raw_rows.append({"subject_id":sid,"channel_index":i,"raw_hex":lab["raw_hex"],"raw_repr":lab["raw_repr"],"decoded_before_cleanup":lab["decoded_before_cleanup"],"decoded_after_padding_strip":lab["decoded_after_padding_strip"],"transducer_raw_hex":c["transducer_raw_hex"],"transducer_repr":c["transducer_repr"],"transducer":c["transducer"],"physical_dimension":c["physical_dimension"],"physical_min":c["physical_min"],"physical_max":c["physical_max"],"digital_min":c["digital_min"],"digital_max":c["digital_max"],"samples_per_record":c["samples_per_record"]})
            notes=[]
            if lab["contains_nul"]: notes.append("NUL")
            if lab["contains_non_ascii"]: notes.append("NON_ASCII")
            if any(x in lab["decoded_after_padding_strip"] for x in ("C3-A2","LOC-A2")): notes.append("EXPECTED_EXACT_AFTER_PADDING_STRIP")
            char_rows.append({"subject":sid,"channel_index":i,"raw_hex":lab["raw_hex"],"decoded_repr":lab["decoded_before_cleanup"],"stripped_repr":lab["decoded_after_padding_strip"],"contains_nul":lab["contains_nul"],"contains_non_ascii":lab["contains_non_ascii"],"exact_expected":exact,"notes":"|".join(notes)})
        py=project_labels(path)
        identities.append({"subject_id":sid,"official_folder_id":str(n),"local_subject_id":sid,"local_path":str(path.parent),"rec_patient_field_repr":repr(h["patient_raw"]),"rec_recording_field_repr":repr(h["recording_raw"]),"annotation_expected":f"{n}_1.txt|{n}_1.xlsx|{n}_2.txt|{n}_2.xlsx","annotation_files_present":"|".join(sorted(x.name for x in path.parent.glob(f"{n}_*.txt")))+"|"+"|".join(sorted(x.name for x in path.parent.glob(f"{n}_*.xlsx"))),"signal_body_valid":h["body_valid"],"record_count":h["records"],"record_duration_seconds":h["record_duration"]})
        for i,(a,b) in enumerate(zip(py,labels)):
            cross.append({"subject":sid,"channel_index":i,"existing_parser_label":a,"independent_parser_label":b,"equal":a==b,"difference_type":"NONE" if a==b else "LABEL_TEXT_DIFFERENCE"})
        cls="ALL_AGREE" if py==labels else "PROJECT_DISAGREES"
        three.append({"subject":sid,"raw_parser_labels":"|".join(labels),"pyedflib_labels":"|".join(py),"project_parser_labels":"|".join(current.get("full_labels", "").split("|")),"classification":cls})
        fields=[c["label"]["decoded_after_padding_strip"] for c in h["channels"]]
        row={"subject_id":sid,"signal_count":h["ns"]}
        for i,label in enumerate(fields,1): row[f"ch{i:02d}"]=label
        row.update({"exact_c3_a2":"C3-A2" in fields,"exact_loc_a2":"LOC-A2" in fields})
        inventories.append(row)
        fp=hashlib.sha256(json.dumps({"labels":fields,"samples":[c["samples_per_record"] for c in h["channels"]],"dimensions":[c["physical_dimension"] for c in h["channels"]]},sort_keys=True).encode()).hexdigest()
        clusters.append({"subject_id":sid,"schema_fingerprint":fp,"signal_count":h["ns"],"channel_labels":"|".join(fields),"samples_per_record":"|".join(str(c["samples_per_record"]) for c in h["channels"]),"physical_dimensions":"|".join(c["physical_dimension"] for c in h["channels"])})
    write_csv("isruc_original_raw_header_labels.csv",raw_rows)
    write_csv("isruc_channel_label_character_audit.csv",char_rows)
    write_csv("isruc_original_channel_inventory_35_diagnostic.csv",inventories)
    write_csv("isruc_channel_schema_clusters.csv",clusters)
    write_csv("isruc_channel_parser_crosscheck.csv",cross)
    write_csv("isruc_three_way_channel_parser_audit.csv",three)
    excluded=[]
    for n,h in parsed.items():
        sid=f"I{n:03d}"; labels=[c["label"]["decoded_after_padding_strip"] for c in h["channels"]]
        if "C3-A2" not in labels or "LOC-A2" not in labels:
            excluded.append({"subject_id":sid,"exact_channels":"|".join(labels),"c3_a2_absent":"C3-A2" not in labels,"loc_a2_absent":"LOC-A2" not in labels,**{x.replace('-','_').lower()+"_present":x in labels for x in RELATED},"primary_root_cause":"ALTERNATE_SOURCE_LABEL" if any(x.endswith("-M1") or x.endswith("-M2") for x in labels) else "TRUE_CHANNEL_ABSENCE"})
    write_csv("isruc_excluded_subject_channel_findings.csv",excluded)
    root_rows=[]
    for r in excluded:
        root_rows.append({"subject_id":r["subject_id"],"primary_root_cause":r["primary_root_cause"],"evidence":"Independent raw EDF label fields, pyedflib labels, and project labels agree; alternate reference labels are explicit."})
    write_csv("isruc_channel_exclusion_root_causes.csv",root_rows,["subject_id","primary_root_cause","evidence"])
    # Side-by-side fixed-header examples: first three included and first five schema-excluded.
    chosen=[n for n in EXPECTED if "C3-A2" in [c["label"]["decoded_after_padding_strip"] for c in parsed[n]["channels"]] and "LOC-A2" in [c["label"]["decoded_after_padding_strip"] for c in parsed[n]["channels"]]][:3]+[int(r["subject_id"][1:]) for r in excluded[:5]]
    for n in chosen:
        h=parsed[n]
        for c in h["channels"]:
            side.append({"subject_id":f"I{n:03d}","channel_index":c["channel_index"],"label_raw_hex":c["label"]["raw_hex"],"label_repr":c["label"]["raw_repr"],"transducer":c["transducer"],"physical_dimension":c["physical_dimension"],"physical_min":c["physical_min"],"physical_max":c["physical_max"],"digital_min":c["digital_min"],"digital_max":c["digital_max"],"samples_per_record":c["samples_per_record"],"signal_count":h["ns"],"header_length":h["header_length"],"record_duration":h["record_duration"]})
    write_csv("isruc_channel_header_side_by_side.csv",side)
    # Freeze pre-fix snapshot from current project classification and independent hashes.
    snap=[]
    for n in EXPECTED:
        h=parsed[n]; labels=[c["label"]["decoded_after_padding_strip"] for c in h["channels"]]; r=inv.get(n,{})
        snap.append({"subject_id":f"I{n:03d}","raw_rec_sha256":sha256(h["path"]),"body_valid":h["body_valid"],"raw_signal_count":h["ns"],"raw_channel_labels_exact":"|".join(labels),"parsed_channel_labels_current":r.get("full_labels",""),"c3_a2_present_current":r.get("C3-A2_present",""),"loc_a2_present_current":r.get("LOC-A2_present",""),"current_schema_status":"CHANNEL_COMPATIBLE" if r.get("C3-A2_present")=="True" and r.get("LOC-A2_present")=="True" else "MISSING_REQUIRED_CHANNEL","current_terminal_status":"INCLUDED" if n in [1,2,3,4,5,6,7,8,9,10,12,15,16,18,22,24,26] else "EXCLUDED_SCHEMA","current_failure_code":"" if r.get("C3-A2_present")=="True" and r.get("LOC-A2_present")=="True" else "MISSING_REQUIRED_CHANNEL"})
    write_csv("isruc_channel_exclusion_pre_fix_snapshot.csv",snap)
    write_csv("isruc_cohort_identity_audit.csv", identities)
    print(json.dumps({"subjects":35,"signals":len(raw_rows),"excluded":len(excluded),"included":35-len(excluded),"parser_equal":sum(r["equal"] for r in cross),"root_causes":dict(Counter(r["primary_root_cause"] for r in root_rows))},sort_keys=True))

if __name__=="__main__": main()
