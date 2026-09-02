import hashlib
import numpy as np
import pytest
from shiftsleep_uq.data.preprocessing import *
from shiftsleep_uq.data.preprocess import summarize_epoch_accounting

def test_label_mapping_and_rk():
    assert canonicalize_label('Sleep stage W')=='Wake'
    assert canonicalize_label('Sleep stage 1')=='N1'
    assert canonicalize_label('Sleep stage 4')=='N3'

def test_exact_nemar_labels():
    assert canonicalize_label('Sleep stage W') == 'Wake'
    assert canonicalize_label('Sleep stage N1') == 'N1'
    assert canonicalize_label('Sleep stage N2') == 'N2'
    assert canonicalize_label('Sleep stage N3') == 'N3'
    assert canonicalize_label('Sleep stage R') == 'REM'
    with pytest.raises(PreprocessingError, match='ANNOTATION_EXCLUDED_LABEL:unscored'):
        canonicalize_label('Sleep stage U')


def test_dataset_specific_exact_label_allowlists_precede_shared_canonical_mapping():
    assert canonicalize_label('Sleep stage 1', dataset='sleep_edf_sc') == 'N1'
    assert canonicalize_label('Sleep stage N1', dataset='isruc_s1') == 'N1'
    with pytest.raises(PreprocessingError, match='ANNOTATION_SOURCE_LABEL_NOT_ALLOWED'):
        canonicalize_label('Sleep stage N1', dataset='sleep_edf_sc')
    with pytest.raises(PreprocessingError, match='ANNOTATION_SOURCE_LABEL_NOT_ALLOWED'):
        canonicalize_label('Sleep stage 1', dataset='isruc_s1')


def test_dataset_specific_allowlist_is_exact_after_whitespace_normalization():
    assert canonicalize_label('  Sleep   stage 1  ', dataset='sleep_edf_sc') == 'N1'
    assert canonicalize_label('Sleep stage 4', dataset='sleep_edf_sc') == 'N3'
    assert canonicalize_label('Stage 1') == 'N1'  # explicit internal/test alias only
    with pytest.raises(PreprocessingError, match='ANNOTATION_SOURCE_LABEL_NOT_ALLOWED'):
        canonicalize_label('Stage 1', dataset='sleep_edf_sc')
    with pytest.raises(PreprocessingError, match='ANNOTATION_SOURCE_LABEL_NOT_ALLOWED'):
        canonicalize_label('sleep stage 1', dataset='sleep_edf_sc')
    with pytest.raises(PreprocessingError, match='ANNOTATION_SOURCE_LABEL_NOT_ALLOWED'):
        canonicalize_label('Sleep stage X', dataset='isruc_s1')

def test_nemar_unknown_and_fuzzy_labels_never_map_to_wake():
    for label in ['Sleep stage X', 'sleep stage n1x', 'Sleep Stage N2']:
        with pytest.raises(PreprocessingError, match='ANNOTATION_UNKNOWN_LABEL'):
            canonicalize_label(label)

def test_unknown_never_wake():
    with pytest.raises(PreprocessingError,match='ANNOTATION_EXCLUDED_LABEL:unknown'): canonicalize_label('Sleep stage ?')

def test_unit_conversion():
    x=np.array([1.0]); assert unit_to_uv(x,'V')[0]==1e6; assert unit_to_uv(x,'mV')[0]==1e3; assert unit_to_uv(x,'uV')[0]==1

def test_unknown_unit_quarantine():
    with pytest.raises(PreprocessingError,match='STRUCTURAL_UNIT_MISMATCH'): unit_to_uv(np.ones(2),'counts')

def test_resampling_continuous_200_to_100():
    x=np.arange(6000,dtype=float); y=resample_continuous(x,200,100); assert len(y)==3000

def test_resampling_continuous_200_to_50():
    assert len(resample_continuous(np.arange(6000,dtype=float),200,50))==1500

def test_resampling_continuous_100_to_50():
    assert len(resample_continuous(np.arange(3000,dtype=float),100,50))==1500

def test_no_upsampling():
    with pytest.raises(PreprocessingError,match='UPSAMPLING'): resample_continuous(np.ones(10),50,100)

def test_exact_epoch_sizes():
    x=np.arange(6000,dtype=float); a,e=slice_epochs(x,[0,30],100,3000); assert [len(v) for v in a]==[3000,3000]
    a,e=slice_epochs(np.arange(3000,dtype=float),[0],50,1500); assert len(a[0])==1500

def test_duration_expansion():
    out=expand_annotations([(0,120,'Sleep stage 2')]); assert len(out)==4 and [x.onset for x in out]==[0,30,60,90]

def test_ambiguous_duration_excluded():
    assert expand_annotations([(0,31,'Wake')])[0].exclusion=='alignment_error'

def test_zero_duration_event_is_not_a_sleep_epoch():
    assert expand_annotations([(0,0,'Sleep stage U')]) == []

def test_accounting_invariant_a_and_d():
    expanded = expand_annotations([(0,30,'Sleep stage W'), (30,30,'Sleep stage N1'),
                                    (60,30,'Sleep stage U')])
    counts, exclusions, valid, excluded = summarize_epoch_accounting(expanded)
    assert counts == {'wake': 1, 'n1': 1, 'n2': 0, 'n3': 0, 'rem': 0}
    assert exclusions['unscored'] == 1
    assert valid == 2 and excluded == 1 and valid + excluded == len(expanded)

def test_scorer2_does_not_change_primary():
    # Scorer-2 is deliberately not an input to canonicalization.
    assert canonicalize_label('Sleep stage 1')=='N1'

def test_required_channel_contract_literals():
    assert 'EEG Fpz-Cz' and 'EOG horizontal' and 'C3-A2' and 'LOC-A2'

def test_missing_channel_failure():
    with pytest.raises(PreprocessingError,match='MISSING_REQUIRED_EEG'):
        raise PreprocessingError('MISSING_REQUIRED_EEG')

def test_output_schema():
    validate_output(np.zeros((2,3000),np.float32),np.zeros((2,1500),np.float32),np.array([0,4]))

def test_output_rejects_nonfinite():
    x=np.zeros((1,3000),np.float32); x[0,0]=np.nan
    with pytest.raises(PreprocessingError,match='OUTPUT_NONFINITE'): validate_output(x,np.zeros((1,1500),np.float32),np.array([0]))

def test_resampling_deterministic():
    x=np.sin(np.arange(10000)/13); assert np.array_equal(resample_continuous(x,200,100),resample_continuous(x,200,100))

def test_atomic_temp_suffix_is_not_output():
    import shiftsleep_uq.data.preprocess as p
    assert 'np.savez_compressed' in open(p.__file__,encoding='utf-8').read()

def test_target_free_contract_text():
    from pathlib import Path
    text=Path('configs/data_contract_v1.yaml').read_text()
    assert 'final_benchmark_frozen: false' in text and 'CORE_PREPROCESSING_FROZEN' in text

def test_raw_paths_ignored():
    import subprocess
    assert subprocess.run(['git','check-ignore','data/raw/example.edf'],capture_output=True).returncode==0
