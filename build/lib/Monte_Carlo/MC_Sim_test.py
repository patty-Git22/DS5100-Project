import unittest
import numpy as np
import pandas as pd
from MC_Sim import Die, Game, Analyzer

class TestDie(unittest.TestCase):

    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.die = Die(self.faces)

    def test_change_weight(self):
        self.die.change_weight(3, 2.0)
        weight = self.die.show_die().loc[3, 'Weight']
        self.assertEqual(weight, 2.0)

    def test_roll_die(self):
        rolls = self.die.roll_die(5)
        self.assertEqual(len(rolls), 5)
        self.assertTrue(all(r in self.faces for r in rolls))

    def test_show_die(self):
        df = self.die.show_die()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Weight', df.columns)


class TestGame(unittest.TestCase):

    def setUp(self):
        dice = [Die(np.array([1, 2, 3])) for _ in range(3)]
        self.game = Game(dice)
        self.game.play(5)

    def test_play(self):
        self.assertEqual(self.game.results.shape, (5, 3))

    def test_show_wide(self):
        wide = self.game.show('wide')
        self.assertIsInstance(wide, pd.DataFrame)
        self.assertEqual(wide.shape, (5, 3))

    def test_show_narrow(self):
        narrow = self.game.show('narrow')
        self.assertIsInstance(narrow, pd.DataFrame)
        self.assertEqual(set(narrow.columns), {'Roll', 'Die', 'Face'})


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        dice = [Die(np.array(['A', 'B'])) for _ in range(3)]
        self.game = Game(dice)
        self.game.play(10)
        self.analyzer = Analyzer(self.game)

    def test_jackpot(self):
        result = self.analyzer.jackpot()
        self.assertTrue(isinstance(result, (int, np.integer)))

    def test_face_counts(self):
        counts = self.analyzer.face_counts()
        self.assertIsInstance(counts, pd.DataFrame)
        self.assertGreaterEqual(counts.values.sum(), 0)

    def test_combo_count(self):
        combos = self.analyzer.combo_count()
        self.assertIsInstance(combos, pd.Series)

    def test_perm_count(self):
        perms = self.analyzer.perm_count()
        self.assertIsInstance(perms, pd.Series)


if __name__ == '__main__':
    unittest.main(verbosity=2)
