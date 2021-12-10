import os
import unittest

from ipfabric import IPFClient

condition = False if os.getenv('IPF_TOKEN', None) and os.getenv('IPF_URL', None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_intent(self):
        ipf = IPFClient()
        ipf.intent.load_intent()
        self.assertIsInstance(ipf.intent.intent_by_id, dict)
        self.assertIsInstance(ipf.intent.intent_by_name, dict)
        self.assertIsInstance(ipf.intent.group_by_id, dict)
        self.assertIsInstance(ipf.intent.group_by_name, dict)
        self.assertIsInstance(ipf.intent.custom, list)
        self.assertIsInstance(ipf.intent.builtin, list)

    def test_compare(self):
        ipf = IPFClient()
        ipf.intent.load_intent()
        self.assertIsInstance(ipf.intent.compare_snapshot('$prev'), list)


if __name__ == '__main__':
    unittest.main()
