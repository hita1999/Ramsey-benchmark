"""Regression checks for accepting witnesses and rejecting invalid certificates."""
import json
import unittest
from pathlib import Path
from verify import verify


class VerifierTests(unittest.TestCase):
    def test_saved_certificate(self):
        c = json.loads(Path(__file__).with_name('certificate.json').read_text())
        self.assertEqual(verify(c), dict(valid=True, n=8, red_edges=10,
                         triples_checked=56, quadruples_checked=70, lower_bound=9))

    def test_forbidden_structures(self):
        for c, message in [
            ({'n': 3, 'edges': [[0, 1], [0, 2], [1, 2]]}, 'red triangle'),
            ({'n': 4, 'edges': []}, 'blue K4'),
        ]:
            with self.subTest(c=c), self.assertRaisesRegex(ValueError, message):
                verify(c)

    def test_malformed_input(self):
        invalid = [
            None, {}, {'n': True, 'edges': []}, {'n': 0, 'edges': []},
            {'n': 2, 'edges': [[0, 0]]}, {'n': 2, 'edges': [[1, 0]]},
            {'n': 2, 'edges': [[0, 2]]}, {'n': 2, 'edges': [[0, 1], [0, 1]]},
            {'n': 2, 'edges': [[False, 1]]}, {'n': 2, 'edges': [[0]]},
            {'n': 2, 'edges': '01'},
        ]
        for c in invalid:
            with self.subTest(c=c), self.assertRaises(ValueError):
                verify(c)


if __name__ == '__main__':
    unittest.main()
