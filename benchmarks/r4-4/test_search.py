"""Check incremental search score against full recomputation; no discovery run."""
import random
import unittest
from search import setup, initial_score, flip_delta


class ScoreTests(unittest.TestCase):
    def test_every_flip_of_all_four_vertex_graphs(self):
        pairs, quads, affected = setup(4)
        for mask in range(64):
            bits = [(mask >> i)&1 for i in range(len(pairs))]
            counts, score = initial_score(bits,quads)
            for e in range(len(pairs)):
                delta = flip_delta(bits[e],affected[e],counts)
                flipped = bits.copy()
                flipped[e] ^= 1
                self.assertEqual(score+delta,initial_score(flipped,quads)[1])

    def test_long_flip_sequence(self):
        rng = random.Random(42)
        pairs,quads,affected = setup(9)
        bits = [rng.randrange(2) for _ in pairs]
        counts,score = initial_score(bits,quads)
        for _ in range(1000):
            e = rng.randrange(len(pairs))
            score += flip_delta(bits[e],affected[e],counts)
            change = 1-2*bits[e]
            bits[e] ^= 1
            for q in affected[e]:
                counts[q] += change
            self.assertEqual((counts,score),initial_score(bits,quads))


if __name__ == '__main__':
    unittest.main()
