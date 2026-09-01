from .base import PSGAdapter

class SleepEDFSCAdapter(PSGAdapter):
    dataset_id = "sleep_edf_sc"
    def enumerate_recordings(self):
        return sorted(p.stem.replace("-PSG", "") for p in (self.raw_root/"sleep-edfx/1.0.0/sleep-cassette").glob("SC*E0-PSG.edf"))
    def resolve_subject_id(self, recording_id): return recording_id
    def load_required_signals(self, recording_id): return None
    def load_annotations(self, recording_id): return None
    def get_native_schema(self, recording_id): return {"EEG":"EEG Fpz-Cz","EOG":"EOG horizontal","EEG_rate":100,"EOG_rate":100}
    def get_annotation_source(self, recording_id): return "official Sleep-EDF hypnogram EDF+ annotations"
    def validate_recording(self, recording_id): return []
