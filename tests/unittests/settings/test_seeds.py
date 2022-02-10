import unittest
from unittest.mock import MagicMock, patch

from ipfabric.settings.seeds import Seeds


class TestSeeds(unittest.TestCase):
    def setUp(self) -> None:
        self.seed = Seeds(MagicMock())
        self.seed.client.get().json.return_value = ["10.0.0.1"]

    def test_check_seeds(self):
        self.assertTrue(self.seed._check_seeds(["10.0.0.2"]))
        self.assertFalse(self.seed._check_seeds(["Hello"]))

    def test_set_seeds(self):
        seeds = ["10.0.0.1", "10.0.0.2"]
        self.seed.client.put().json.return_value = seeds
        self.assertEqual(self.seed.set_seeds(seeds), seeds)

    def test_set_seeds_failed(self):
        with self.assertRaises(SyntaxError) as err:
            self.seed.set_seeds("10.0.0.1")

    @patch("ipfabric.settings.seeds.Seeds.set_seeds")
    def test_add_seeds(self, mock_set):
        mock_set.return_value = ["10.0.0.1", "10.0.0.2"]
        seeds = self.seed.add_seeds("10.0.0.1")
        self.assertEqual(seeds, ["10.0.0.1", "10.0.0.2"])

    @patch("ipfabric.settings.seeds.Seeds.set_seeds")
    def test_delete_seeds(self, mock_set):
        mock_set.return_value = ["10.0.0.1"]
        seeds = self.seed.delete_seeds("10.0.0.2")
        self.assertEqual(seeds, ["10.0.0.1"])
