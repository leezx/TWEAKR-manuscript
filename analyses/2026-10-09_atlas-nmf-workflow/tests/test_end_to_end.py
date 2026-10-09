import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1] / 'code'


class InterfaceTests(unittest.TestCase):
    def test_06_to_07_preserves_deduplicated_programs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cohort = []
            tasks = []
            for dataset in ('D1', 'D2'):
                cohort.append(dict(dataset_id=dataset, source_id='src', sample_id='S1',
                    biological_sample_id=dataset+':S1', patient_id='', patient_id_status='unknown'))
                for rank in (4,5):
                    output = root / dataset / str(rank)
                    output.mkdir(parents=True)
                    with (output / 'deliver.nmf_top50.repeated.csv').open('w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['factor','gene'])
                        writer.writeheader()
                        writer.writerows(dict(factor='1', gene=f'G{i}') for i in range(50))
                    tasks.append(dict(dataset_id=dataset, source_id='src', sample_id='S1',
                                      rank=rank, output_dir=str(output)))
            for name, rows in (('cohort',cohort),('tasks',tasks)):
                with (root / (name+'.tsv')).open('w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
                    writer.writeheader()
                    writer.writerows(rows)
            subprocess.run([sys.executable,str(CODE/'06_filter_robust_programs.py'),
                '--tasks',str(root/'tasks.tsv'),'--cohort',str(root/'cohort.tsv'),
                '--output',str(root/'robust.tsv')],check=True)
            with (root/'robust.tsv').open() as f:
                rows = list(csv.DictReader(f, delimiter='\t'))
            self.assertEqual(len(rows),2)
            self.assertEqual(len({p['program_id'] for p in rows}),2)
            subprocess.run([sys.executable,str(CODE/'07_discover_metaprograms.py'),
                '--programs',str(root/'robust.tsv'),'--cohort',str(root/'cohort.tsv'),
                '--output',str(root/'mp.json')],check=True)
            result = json.loads((root/'mp.json').read_text())
            self.assertEqual(len(result),1)
            self.assertEqual(result[0]['n_samples'],2)
            self.assertEqual(result[0]['n_patients'],0)
            self.assertEqual(result[0]['n_datasets'],2)


if __name__ == '__main__':
    unittest.main()
