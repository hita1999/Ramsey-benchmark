import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from verify import verify


class VerifierTests(unittest.TestCase):
    def test_cycle_five_is_valid(self):
        result = verify({'n': 5, 'edges': [[0, 1], [0, 4], [1, 2], [2, 3], [3, 4]]})
        self.assertTrue(result['valid'])
        self.assertEqual(result['ramsey_lower_bound'], 6)
        self.assertEqual(result['triples_checked'], 10)
        self.assertEqual(result['five_sets_checked'], 1)

    def test_complete_and_empty_graphs(self):
        for n in (1, 2, 3, 4, 5, 6, 8):
            with self.subTest(n=n):
                complete = verify({'n': n, 'edges': list(map(list, itertools.combinations(range(n), 2)))})
                empty = verify({'n': n, 'edges': []})
                self.assertEqual(complete['triangles'], math.comb(n, 3))
                self.assertEqual(complete['independent_fives'], 0)
                self.assertEqual(empty['triangles'], 0)
                self.assertEqual(empty['independent_fives'], math.comb(n, 5))
                for result in (complete, empty):
                    self.assertEqual(result['triples_checked'], math.comb(n, 3))
                    self.assertEqual(result['five_sets_checked'], math.comb(n, 5))

    def test_all_labeled_five_vertex_graphs_against_matrix_oracle(self):
        pairs = list(itertools.combinations(range(5), 2))
        for mask in range(1 << len(pairs)):
            edges = [list(e) for i, e in enumerate(pairs) if mask & (1 << i)]
            adjacency = [[0] * 5 for _ in range(5)]
            for u, v in edges:
                adjacency[u][v] = adjacency[v][u] = 1
            # trace(A^3)/6 counts triangles via ordered closed walks.
            triangles = sum(adjacency[i][j] * adjacency[j][k] * adjacency[k][i]
                            for i in range(5) for j in range(5) for k in range(5)) // 6
            result = verify({'n': 5, 'edges': edges})
            self.assertEqual(result['triangles'], triangles)
            self.assertEqual(result['independent_fives'], int(mask == 0))
            self.assertEqual(result['valid'], triangles == 0 and mask != 0)

    def test_enumeration_does_not_stop_at_first_violation(self):
        result = verify({'n': 8, 'edges': [[0, 1], [0, 2], [1, 2]]})
        self.assertFalse(result['valid'])
        self.assertEqual(result['triangles'], 1)
        self.assertEqual(result['independent_fives'], 16)
        self.assertEqual(result['triples_checked'], 56)
        self.assertEqual(result['five_sets_checked'], 56)
        self.assertIsNone(result['ramsey_lower_bound'])

    def test_malformed_certificates_rejected(self):
        invalid = [None, [], {}, {'n': 5}, {'n': 5, 'edges': [], 'extra': 1},
                   {'n': True, 'edges': []}, {'n': 5.0, 'edges': []},
                   {'n': 0, 'edges': []}, {'n': -1, 'edges': []},
                   {'n': 5, 'edges': None}]
        invalid_edges = [[[0, 0]], [[1, 0]], [[-1, 2]], [[0, 5]], [[False, 1]],
                         [[0.0, 1]], [[0]], [[0, 1, 2]], ['01'], [[0, 1], [0, 1]]]
        invalid.extend({'n': 5, 'edges': edges} for edges in invalid_edges)
        for certificate in invalid:
            with self.subTest(certificate=certificate):
                with self.assertRaises(ValueError):
                    verify(certificate)

    def test_cli_exit_codes(self):
        script = str(Path(__file__).with_name('verify.py'))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'certificate.json'
            for contents, code in [(json.dumps({'n': 2, 'edges': []}), 0),
                                   (json.dumps({'n': 5, 'edges': []}), 1),
                                   ('{', 2), ('{"n": true, "edges": []}', 2)]:
                path.write_text(contents)
                process = subprocess.run([sys.executable, script, str(path)], capture_output=True, text=True)
                self.assertEqual(process.returncode, code)
                self.assertEqual(json.loads(process.stdout)['valid'], code == 0)
            process = subprocess.run([sys.executable, script, str(path) + '.missing'], capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)


if __name__ == '__main__':
    unittest.main()
