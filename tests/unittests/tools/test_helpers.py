import unittest

from ipfabric.tools import helpers


class Helpers(unittest.TestCase):

    def test_regex(self):
        test = helpers.create_regex('TeSt1234.')
        self.assertEqual(test, '^[Tt][Ee][Ss][Tt]1234.$')
