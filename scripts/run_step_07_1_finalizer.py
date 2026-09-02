"""Bounded Step 7.1 finalizer: wait for eight audited acquisition shards, then fail closed or freeze."""
from __future__ import annotations
import os, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'reports'
def run(*args):
 print('+',' '.join(args),flush=True); subprocess.run(args,cwd=ROOT,check=True,env={**os.environ,'PYTHONPATH':'src'})
def main():
 deadline=time.monotonic()+12*3600
 parts=lambda: list(R.glob('provider_integrity_audit.part-*-of-08.csv'))
 while len(parts())<8:
  if time.monotonic()>deadline: raise RuntimeError('acquisition shards did not complete within 12 hours')
  time.sleep(30)
 run(sys.executable,'scripts/merge_step_07_1_provider_audits.py')
 run(sys.executable,'scripts/step_07_1_process_and_audit.py')
 run(sys.executable,'scripts/step_07_1_freeze_and_report.py')
 run('pytest','-q')
 run(sys.executable,'-m','compileall','-q','src','tests','scripts')
 run('git','diff','--check')
 # Explicit forbidden-artifact and credential checks before local commit.
 tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
 forbidden=[x for x in tracked if x.lower().endswith(('.edf','.rec','.npz','.zip','.tar','.gz'))]
 if forbidden: raise RuntimeError('forbidden tracked signal artifacts: '+str(forbidden))
 run('git','add','src/shiftsleep_uq/data/preprocessing.py','src/shiftsleep_uq/data/preprocess.py','tests','scripts','reports','docs','configs/core_cohort_v1.yaml')
 run('git','commit','-m','data: freeze accessible PSG core cohort')
 print('STEP_07_1_FINALIZED',flush=True)
if __name__=='__main__': main()
