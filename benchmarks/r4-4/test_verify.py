"""Verifier tests include all labeled graphs through n=5 against a matrix oracle."""
from itertools import combinations
import json
from math import comb
from pathlib import Path
import unittest
from verify import verify


def oracle(n, edges):
    matrix = [[False]*n for _ in range(n)]
    for u,v in edges:
        matrix[u][v] = matrix[v][u] = True
    clique = independent = 0
    for a in range(n):
        for b in range(a+1,n):
            for c in range(b+1,n):
                for d in range(c+1,n):
                    bits = [matrix[a][b],matrix[a][c],matrix[a][d],
                            matrix[b][c],matrix[b][d],matrix[c][d]]
                    clique += all(bits)
                    independent += not any(bits)
    return clique, independent


class VerifyTests(unittest.TestCase):
    def test_all_graphs_through_five(self):
        for n in range(6):
            pairs = list(combinations(range(n),2))
            for mask in range(1 << len(pairs)):
                edges = [list(p) for i,p in enumerate(pairs) if mask >> i & 1]
                r = verify(dict(n=n,edges=edges))
                k, independent = oracle(n,edges)
                self.assertEqual((r['k4_count'],r['independent4_count']), (k,independent))
                self.assertEqual(r['checked_four_sets'],comb(n,4) if n >= 4 else 0)
                self.assertEqual(r['valid'], k == independent == 0)

    def test_no_early_exit(self):
        for edges in ([],[list(p) for p in combinations(range(6),2)]):
            r = verify(dict(n=6,edges=edges))
            self.assertFalse(r['valid'])
            self.assertEqual(r['checked_four_sets'],15)
            self.assertEqual(r['k4_count']+r['independent4_count'],15)

    def test_both_violation_types(self):
        edges = [list(p) for p in combinations(range(4),2)]
        r = verify(dict(n=8,edges=edges))
        self.assertEqual(r['checked_four_sets'],70)
        self.assertEqual(r['k4_count'],1)
        self.assertEqual(r['independent4_count'],17)
        self.assertFalse(r['valid'])

    def test_malformed(self):
        invalid = [None,[],{},dict(n=True,edges=[]),dict(n=-1,edges=[]),
                   dict(n=4.0,edges=[]),dict(n=4,edges=None)]
        for edges in ([[0,0]],[[1,0]],[[0,4]],[[-1,1]],[[0,1],[0,1]],
                      [[False,1]],[[0,1.0]],[[0]],[[0,1,2]],['01']):
            invalid.append(dict(n=4,edges=edges))
        for cert in invalid:
            self.assertFalse(verify(cert)['valid'],repr(cert))
            self.assertFalse(verify(cert)['format_valid'],repr(cert))

    def test_saved_certificates(self):
        paths = sorted((Path(__file__).parent/'run'/'certificates').glob('*.json'))
        self.assertTrue(paths, 'production certificates must exist')
        for path in paths:
            self.assertTrue(verify(json.loads(path.read_text()))['valid'],str(path))


if __name__ == '__main__':
    unittest.main()
