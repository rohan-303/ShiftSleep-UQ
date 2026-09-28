from __future__ import annotations

import csv
import ctypes
import json
import time
from ctypes import wintypes
from pathlib import Path

import torch
from run_r3_scientific import (
 RemediationManifestDataset,
 _build_or_open_cache,
 source_dataset_for_experiment,
)

ROOT=Path(__file__).resolve().parents[1]
class _PROCESS_MEMORY_COUNTERS(ctypes.Structure):
 _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
_PSAPI=ctypes.WinDLL('Psapi.dll');_PSAPI.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(_PROCESS_MEMORY_COUNTERS),wintypes.DWORD];_PSAPI.GetProcessMemoryInfo.restype=wintypes.BOOL
def rss():
 c=_PROCESS_MEMORY_COUNTERS();c.cb=ctypes.sizeof(c);ok=_PSAPI.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(c),c.cb)
 if not ok:raise ctypes.WinError()
 return c.WorkingSetSize
def host_percent():
 class M(ctypes.Structure):_fields_=[('dwLength',ctypes.c_ulong),('dwMemoryLoad',ctypes.c_ulong),('ullTotalPhys',ctypes.c_ulonglong),('ullAvailPhys',ctypes.c_ulonglong),('ullTotalPageFile',ctypes.c_ulonglong),('ullAvailPageFile',ctypes.c_ulonglong),('ullTotalVirtual',ctypes.c_ulonglong),('ullAvailVirtual',ctypes.c_ulonglong),('sAvailExtendedVirtual',ctypes.c_ulonglong)]
 m=M();m.dwLength=ctypes.sizeof(m);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return m.dwMemoryLoad
def main():
 exp='D1_SLEEPEDF_TO_ISRUC';ds=RemediationManifestDataset(source_dataset_for_experiment(exp),'TRAIN','train',root=ROOT);p=ds.records[0][0];before=rss();start=time.time();cache,meta=_build_or_open_cache(p);after=rss()
 row={'experiment':exp,'recording_path':str(p),'cache_shape':json.dumps(list(cache.shape)),'cache_dtype':str(cache.dtype),'cache_sha256':meta['cache_sha256'],'stft_config_sha256':meta['stft_config_sha256'],'elapsed_seconds':time.time()-start,'rss_before_bytes':before,'rss_after_bytes':after,'host_utilization_percent':host_percent(),'gpu_allocated_bytes':torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,'gpu_reserved_bytes':torch.cuda.memory_reserved() if torch.cuda.is_available() else 0,'gpu_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}
 out=ROOT/'reports/remediation/r3_memory_profile_v1.csv';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row)
 print(json.dumps(row))
if __name__=='__main__':main()
