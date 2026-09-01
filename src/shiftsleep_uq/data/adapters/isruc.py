from .base import PSGAdapter

ISRUC_PRIMARY_EVENT_FIELD = "trial_type"
ISRUC_SCORER2_FIELDS = ("scorer2_label", "scorer2_label_value")
ISRUC_EVENT_LABEL_CODES = {
    "Sleep stage W": 0, "Sleep stage N1": 1, "Sleep stage N2": 2,
    "Sleep stage N3": 3, "Sleep stage R": 5, "Sleep stage U": 6,
}

class ISRUC_S1Adapter(PSGAdapter):
    dataset_id = "isruc_s1"
    def enumerate_recordings(self):
        return sorted(p.name.removeprefix("sub-").removesuffix("_task-sleep_eeg.edf") for p in (self.raw_root/"isruc-nemar/v1.0.1").glob("sub-I*_task-sleep_eeg.edf"))
    def resolve_subject_id(self, recording_id): return recording_id
    def load_required_signals(self, recording_id): return None
    def load_annotations(self, recording_id): return None
    def get_native_schema(self, recording_id): return {"EEG":"C3-A2","EOG":"LOC-A2","EEG_rate":200,"EOG_rate":200,"scorer":"scorer_1"}
    def get_annotation_source(self, recording_id): return "NEMAR v1.0.1 scorer-1 events; trial_type primary; scorer-2 diagnostic extras"
    def validate_recording(self, recording_id): return []
