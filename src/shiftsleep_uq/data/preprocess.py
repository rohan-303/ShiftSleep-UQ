"""Contract-driven PSG preprocessing CLI. No models or normalization are imported."""
from __future__ import annotations
import argparse, csv, hashlib, json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pyedflib
from .preprocessing import *

VERSION = "0.1.0"
SC_LABELS = {"EEG Fpz-Cz": "eeg", "EOG horizontal": "eog"}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def read_edf(path: Path, channels: tuple[str,str]):
    try: f=pyedflib.EdfReader(str(path))
    except Exception as e: raise PreprocessingError(f"CORRUPT_EDF:{e}")
    try:
        labels=f.getSignalLabels(); idx=[]
        for c in channels:
            if c not in labels: raise PreprocessingError(("MISSING_REQUIRED_EEG" if c==channels[0] else "MISSING_REQUIRED_EOG")+":"+c)
            idx.append(labels.index(c))
        rates=[float(f.getSampleFrequency(i)) for i in idx]
        units=[f.getPhysicalDimension(i) for i in idx]
        duration=float(f.file_duration)
        arrays=[f.readSignal(i) for i in idx]
        return arrays,rates,units,duration,labels
    finally: f.close()

def read_sc_events(path: Path):
    try: f=pyedflib.EdfReader(str(path)); ons,dur,desc=f.readAnnotations(); f.close()
    except Exception as e: raise PreprocessingError(f"CORRUPT_EDF:{e}")
    return [(float(o),float(d),str(x)) for o,d,x in zip(ons,dur,desc)]

def read_isruc_events(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows=csv.DictReader(f, delimiter="\t")
        return [(float(r["onset"]),float(r["duration"]),r["trial_type"]) for r in rows]

def recording_spec(dataset: str, subject: str, raw_root: Path, annotation_root: Path):
    if dataset == "sleep_edf_sc":
        # Frozen SC identity: subject/night token is the filename stem without modality suffix.
        p=raw_root/"sleep-edfx"/"1.0.0"/"sleep-cassette"/f"{subject}-PSG.edf"
        # Official pairing retains the subject/night token and uses a source-specific
        # hypnogram suffix (C or H); accept only an exact existing official pair.
        ann_dir=annotation_root/"sleep-edfx"/"1.0.0"
        candidates=[ann_dir/(subject[:-1]+suffix+"-Hypnogram.edf") for suffix in ("C","H")] if subject.endswith("E0") else [ann_dir/(subject+"-Hypnogram.edf")]
        a=next((x for x in candidates if x.exists()), candidates[0])
        return p,a,"EEG Fpz-Cz","EOG horizontal",100,100,"SC","official Sleep-EDF"
    if dataset == "isruc_s1":
        p=raw_root/"isruc-nemar"/"v1.0.1"/f"sub-{subject}_task-sleep_eeg.edf"
        a=raw_root/"isruc-nemar"/"v1.0.1"/f"sub-{subject}_task-sleep_events.tsv"
        return p,a,"C3-A2","LOC-A2",200,200,"ISRUC-S1","NEMAR_BIDS_DERIVATIVE v1.0.1; scorer_1 primary"
    raise ValueError(dataset)

def process_one(dataset: str, subject: str, raw_root: Path, output_root: Path, annotation_root: Path, dry_run=False):
    p,a,ec,oc,er,orate,cohort,annotation_source=recording_spec(dataset,subject,raw_root,annotation_root)
    row={"dataset":dataset,"cohort":cohort,"subject_id":subject,"recording_id":subject,"source_file":str(p),"source_sha256":sha256(p) if p.exists() else "","annotation_file":str(a),"annotation_sha256":sha256(a) if a.exists() else "","source_eeg_channel":ec,"source_eog_channel":oc,"source_eeg_rate":er,"source_eog_rate":orate,"canonical_unit":"uV","target_eeg_rate":100,"target_eog_rate":50,"status":"FAILED","failure_code":"","contract_version":"1.1.0","preprocessing_version":VERSION}
    try:
        if not p.exists() or not a.exists(): raise PreprocessingError("ACQUISITION_FAILURE")
        (eeg,eog),rates,units,duration,_=read_edf(p,(ec,oc))
        if rates != [float(er),float(orate)]: raise PreprocessingError("UNEXPECTED_NATIVE_RATE")
        eeg=unit_to_uv(eeg,units[0]); eog=unit_to_uv(eog,units[1])
        events=read_sc_events(a) if dataset=="sleep_edf_sc" else read_isruc_events(a)
        expanded=expand_annotations(events)
        valid=[x for x in expanded if x.canonical is not None and x.exclusion is None]
        row["total_source_stage_epochs"]=len(expanded); row["excluded_epochs"]=len(expanded)-len(valid)
        if dry_run:
            row.update(status="DRY_RUN",valid_canonical_epochs=len(valid),output_path="")
            return row
        eeg=resample_continuous(eeg,rates[0],100); eog=resample_continuous(eog,rates[1],50)
        ee,erows=slice_epochs(eeg,[x.onset for x in valid],100,3000); eo,orows=slice_epochs(eog,[x.onset for x in valid],50,1500)
        n=min(len(ee),len(eo),len(valid))
        if n != len(valid): raise PreprocessingError("MISSING_SIGNAL_SAMPLES")
        labels=np.asarray([LABEL_TO_INT[x.canonical] for x in valid],dtype=np.int8)
        eeg_arr=np.asarray(ee,dtype=np.float32); eog_arr=np.asarray(eo,dtype=np.float32)
        validate_output(eeg_arr,eog_arr,labels)
        output_root.mkdir(parents=True,exist_ok=True); out=output_root/f"{dataset}__{subject}__core_v1.npz"; fd,tmp=tempfile.mkstemp(prefix=out.name+".",suffix=".npz.tmp",dir=output_root); os.close(fd)
        meta={"dataset":dataset,"cohort":cohort,"subject_id":subject,"recording_id":subject,"source_eeg_channel":ec,"source_eog_channel":oc,"native_eeg_rate":rates[0],"native_eog_rate":rates[1],"target_eeg_rate":100,"target_eog_rate":50,"canonical_unit":"uV","annotation_source":annotation_source,"scorer":"scorer_1" if dataset=="isruc_s1" else "official_single_stream","contract_version":"1.1.0","preprocessing_version":VERSION,"normalized":False,"standardized":False}
        with open(tmp, "wb") as handle:
            np.savez_compressed(handle,eeg=eeg_arr,eog=eog_arr,labels=labels,epoch_onsets_seconds=np.asarray([x.onset for x in valid],dtype=np.float64),source_epoch_indices=np.asarray([x.source_index for x in valid],dtype=np.int64),metadata_json=json.dumps(meta,sort_keys=True))
        os.replace(tmp,out)
        row.update(status="SUCCESS",valid_canonical_epochs=n,output_path=str(out),output_sha256=sha256(out),eeg_shape=str(eeg_arr.shape),eog_shape=str(eog_arr.shape),nan_inf="0/0")
        return row
    except PreprocessingError as e:
        row["failure_code"]=str(e).split(":",1)[0]; row.setdefault("valid_canonical_epochs",0); row.setdefault("excluded_epochs",0); row["output_path"]=""; return row
    except Exception as e:
        row["failure_code"]="CORRUPT_EDF" if "edf" in str(e).lower() else "ACQUISITION_FAILURE"; row["error_detail"]=str(e); row.setdefault("valid_canonical_epochs",0); row.setdefault("excluded_epochs",0); row["output_path"]=""; return row

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--dataset",choices=["sleep_edf_sc","isruc_s1"],required=True); ap.add_argument("--subject",required=True); ap.add_argument("--raw-root",default="data/raw"); ap.add_argument("--output-root",default="data/processed/core_v1"); ap.add_argument("--annotation-root",default="data/raw/metadata"); ap.add_argument("--contract",default="configs/data_contract_v1.yaml"); ap.add_argument("--preprocessing-config",default="configs/preprocessing_v1.yaml"); ap.add_argument("--dry-run",action="store_true"); args=ap.parse_args(argv)
    row=process_one(args.dataset,args.subject,Path(args.raw_root),Path(args.output_root),Path(args.annotation_root),args.dry_run); print(json.dumps(row,sort_keys=True)); return 0 if row["status"] in {"SUCCESS","DRY_RUN"} else 2
if __name__=="__main__": raise SystemExit(main())
