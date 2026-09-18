from __future__ import annotations
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def rows(p):
 with open(ROOT/p,newline='') as f:return list(csv.DictReader(f))

def test_step17_gates_and_frozen_inputs():
 assert json.loads((ROOT/'reports/step12_gate_v1_2.json').read_text())['b0_statistical_version']=='v1_2'
 assert json.loads((ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').read_text())['engine_gate']=='WEIGHTED_RANKING_ENGINE_FROZEN'
 assert json.loads((ROOT/'reports/step15_3_b1_evaluation_gate.json').read_text())['evaluation_gate']=='B1_PRIMARY_EVALUATION_COMPLETE'
 g=json.loads((ROOT/'reports/step16_method_gate.json').read_text())
 assert g['step16_gate']=='STEP16_METHOD_GATE_COMPLETE' and g['method_authorization_gate']=='RELIABILITY_METHOD_NOT_AUTHORIZED'

def test_step17_tables_and_compound_values():
 assert len(rows('reports/paper_tables/table1_benchmark_design.csv'))==2
 assert len(rows('reports/paper_tables/table2_b0_primary_shift_results.csv'))==12
 t3=rows('reports/paper_tables/table3_b1_vs_b0_compound_effects.csv'); assert len(t3)==4
 expected={('D1_SLEEPEDF_TO_ISRUC','C4'):.03673,('D1_SLEEPEDF_TO_ISRUC','C5'):.18587,('D2_ISRUC_TO_SLEEPEDF','C4'):.05992,('D2_ISRUC_TO_SLEEPEDF','C5'):.00063}
 for r in t3: assert abs(float(r['macro_F1_delta'])-expected[(r['direction'],r['condition'])])<1e-5
 assert len(rows('reports/paper_tables/table4_residual_diagnosis.csv'))==4

def test_step17_figures_provenance_and_source_data():
 p=rows('reports/step17_figure_provenance_v1.csv'); assert len(p)==8
 for r in p:
  assert (ROOT/r['output_pdf']).stat().st_size>0 and (ROOT/r['output_png']).stat().st_size>0
  assert r['b0_version']=='v1_2'
  assert (ROOT/'reports/paper_figures/source_data'/f"{r['figure_id']}.csv").exists()
 for r in rows('reports/step17_table_provenance_v1.csv'): assert r['output_sha256'] and r['b0_version']=='v1_2'

def test_step17_evidence_maps_and_nonclaims():
 claims=rows('reports/step17_claim_evidence_matrix_v1.csv'); assert len(claims)==8
 h=rows('reports/step17_hypothesis_evidence_map_v1.csv'); f6=next(r for r in h if r['hypothesis']=='F6'); assert 'NOT TESTED' in f6['evidence_status']
 assert 'universal uncertainty failure' in (ROOT/'reports/step17_nonclaims_v1.md').read_text()
 assert 'DIAGNOSTIC_ONLY' in {r['classification'] for r in claims}
 assert json.loads((ROOT/'reports/paper_evidence/paper_evidence_manifest_v1.json').read_text())['gate']=='BENCHMARK_SYNTHESIS_FROZEN'

def test_step17_no_silent_nan_in_source_tables():
 for p in [ROOT/'reports/paper_tables/table1_benchmark_design.csv',ROOT/'reports/paper_tables/table2_b0_primary_shift_results.csv',ROOT/'reports/paper_tables/table3_b1_vs_b0_compound_effects.csv',ROOT/'reports/paper_tables/table4_residual_diagnosis.csv']:
  text=p.read_text().lower(); assert 'nan' not in text
