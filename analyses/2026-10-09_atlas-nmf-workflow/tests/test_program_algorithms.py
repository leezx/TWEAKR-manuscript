import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from program_algorithms import robust, discover, summarize, validate_cohort


def program(pid, sample, rank, genes, dataset='D1', patient=None):
    return dict(program_id=pid, sample_id=sample, rank=str(rank), genes=genes,
                dataset_id=dataset, source_id='source1',
                biological_sample_id=dataset + ':' + sample,
                patient_id=patient or sample, patient_id_status='confirmed')


class AlgorithmTests(unittest.TestCase):
    def test_cross_dataset_sample_collision(self):
        genes = [f'G{i}' for i in range(50)]
        rows = [program('a','S1',4,genes,'D1'), program('b','S1',5,genes,'D2')]
        self.assertEqual(robust(rows), [])
        self.assertEqual(len(discover(rows)), 1)

    def test_unknown_and_technical_replicates(self):
        genes = [f'G{i}' for i in range(50)]
        rows = [program('a','S1',4,genes), program('b','S2',4,genes),
                program('c','S3',4,genes)]
        rows[1]['biological_sample_id'] = rows[0]['biological_sample_id']
        for p in rows:
            p.update(patient_id='', patient_id_status='unknown', within_rank_overlap=50)
        validate_cohort(rows)
        out = summarize(rows, rows)
        self.assertEqual((out['n_samples'], out['n_patients'], out['n_unknown_patient_samples']), (2,0,2))
        self.assertEqual(out['dataset_support'][0]['eligible_samples'], 2)

    def test_many_to_one_recurrence(self):
        a = [f'G{i}' for i in range(50)]
        rows = [program('a','S1',4,a), program('b','S1',4,a),
                program('c','S1',5,a), program('d','S2',4,a), program('e','S2',5,a)]
        self.assertEqual(len(robust(rows)), 2)

    def test_consensus_does_not_union_sample_geps(self):
        a = [f'A{i}' for i in range(50)]
        b = [f'B{i}' for i in range(50)]
        rows = [program('a','S1',4,a), program('b','S1',5,b),program('c','S2',4,a)]
        for p in rows: p['within_rank_overlap'] = 50
        self.assertEqual(set(summarize(rows, rows[:1]+rows[2:])['consensus']), set(a))

    def test_threshold_and_leave_one_dataset_out(self):
        a = [f'A{i}' for i in range(50)]
        b = a[:10] + [f'B{i}' for i in range(40)]
        rows = [program('a','S1',4,a),program('b','S2',4,a),program('c','S1',4,b,'D2')]
        self.assertEqual([len(c) for c in discover(rows,10)], [3])
        self.assertEqual([len(c) for c in discover(rows,11)], [2])
        self.assertEqual([len(c) for c in discover([p for p in rows if p['dataset_id'] != 'D2'])], [2])
    def test_threshold_and_cross_rank(self):
        a = [f'A{i}' for i in range(50)]
        b = a[:35] + [f'B{i}' for i in range(15)]
        c = a[:34] + [f'C{i}' for i in range(16)]
        rows = [program('a','S1',4,a), program('b','S1',5,b),
                program('c','S2',4,a), program('d','S2',5,b)]
        self.assertEqual(len(robust(rows)), 2)
        self.assertEqual(robust([program('a','S1',4,a),program('b','S1',5,c)]), [])
        self.assertEqual(robust([program('a','S1',4,a),program('b','S1',4,a)]), [])

    def test_patient_and_dataset_denominators(self):
        genes = [f'G{i}' for i in range(50)]
        rows = [program('a','S1',4,genes,patient='P1'),
                program('b','S2',4,genes,patient='P1'),
                program('c','S3',4,genes,dataset='D2',patient='P2')]
        for p in rows: p['within_rank_overlap'] = 50
        cohort = rows + [program('d','S4',4,genes,dataset='D2')]
        out = summarize(rows, cohort)
        self.assertEqual((out['n_samples'],out['n_patients'],out['n_datasets']), (3,2,2))
        self.assertEqual([r['proportion'] for r in out['dataset_support']], [1, .5])
        self.assertEqual(len(out['consensus']), 50)

    def test_clustering_and_noise(self):
        a = [f'A{i}' for i in range(50)]
        b = [f'B{i}' for i in range(50)]
        rows = [program('a','S1',4,a),program('b','S2',4,a),
                program('c','S3',4,b),program('d','S4',4,b),
                program('noise','S5',4,[f'N{i}' for i in range(50)])]
        clusters = discover(rows)
        self.assertEqual(sorted(len(c) for c in clusters), [2,2])
        self.assertEqual([[p['program_id'] for p in c] for c in discover(rows[::-1])],
                         [[p['program_id'] for p in c] for c in clusters])


if __name__ == '__main__': unittest.main()
