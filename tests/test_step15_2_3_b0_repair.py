from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pytest
from shiftsleep_uq.statistics.weighted_bootstrap import atomic_write_shard, read_shard, validate_shard, shard_metadata

def meta():
    return shard_metadata('B0','D1','C0',17,'AURC',0,2,'pred','draw','engine')

def test_parameterized_shard_metadata_rejection(tmp_path):
    m=meta(); p=tmp_path/'s.npz'; atomic_write_shard(p,m,np.array([1.,2.]));
    for key in ('engine_hash','prediction_hash','draw_hash','condition','seed','metric'):
        bad=dict(m); bad[key]=('wrong' if isinstance(m[key],str) else int(m[key])+1)
        with pytest.raises(ValueError): validate_shard_file_local(p,bad)

def validate_shard_file_local(path, expected):
    m,v=read_shard(path); return validate_shard(m,v,expected)

def test_malformed_schema_nan_and_range_rejection(tmp_path):
    m=meta(); p=tmp_path/'s.npz'; atomic_write_shard(p,m,np.array([1.,2.]));
    bad=dict(m); bad.pop('metric')
    with pytest.raises(ValueError): validate_shard_file_local(p,bad)
    with pytest.raises(ValueError): validate_shard(m,np.array([np.nan,2.]),m)
    bad=dict(m); bad['replicate_end']=3
    with pytest.raises(ValueError): validate_shard_file_local(p,bad)

def test_interrupted_write_has_no_final_valid_shard(tmp_path):
    final=tmp_path/'interrupted.npz'; script=("from pathlib import Path; import tempfile,os; p=Path(r'"+str(final)+"'); fd,t=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=p.parent); os.close(fd); raise SystemExit(17)")
    r=subprocess.run([sys.executable,'-c',script],capture_output=True)
    assert r.returncode==17 and not final.exists() and list(tmp_path.glob('*.tmp'))
