import unittest

from ipfabric import intent_models as imodels


class Models(unittest.TestCase):
    def test_checks(self):
        c = imodels.Checks(**{"0": 1, "20": "TEST", "30": {"hello": "world"}})
        self.assertIsNone(c.blue)
        self.assertEqual(c.green, 1)
        self.assertEqual(c.amber, "TEST")
        self.assertIsInstance(c.red, dict)

    def test_descr(self):
        desc = imodels.Description(general="TEST", checks={"0": "DESC"})
        self.assertEqual(desc.general, "TEST")
        self.assertEqual(desc.checks.green, "DESC")

    def test_result(self):
        result = imodels.Result(count=100, checks={"0": 1, "20": 5})
        self.assertEqual(result.count, 100)
        self.assertEqual(result.checks.green, 1)

    def test_result_compare(self):
        result = imodels.Result(count=100, checks={"0": 1, "20": 5})
        result2 = imodels.Result(count=80, checks={"0": 2, "20": 1, "30": 10})
        comp = result.compare(result2)
        self.assertEqual(comp["count"], {"loaded_snapshot": 100, "compare_snapshot": 80, "diff": -20})
        self.assertEqual(comp["green"], {"loaded_snapshot": 1, "compare_snapshot": 2, "diff": 1})
        self.assertEqual(comp["amber"], {"loaded_snapshot": 5, "compare_snapshot": 1, "diff": -4})
        self.assertEqual(comp["red"], {"loaded_snapshot": 0, "compare_snapshot": 10, "diff": 10})

    def test_child(self):
        child = imodels.Child(weight=10, id="TEST")
        self.assertEqual(child.weight, 10)
        self.assertEqual(child.intent_id, "TEST")

    def test_group(self):
        group = imodels.Group(custom=False, name="TEST", id="HELLO", children=[dict(weight=10, id="TEST")])
        self.assertEqual(group.name, "TEST")
        self.assertEqual(group.children[0].weight, 10)
        self.assertFalse(group.custom)

    def test_intent(self):
        intent = imodels.IntentCheck(
            groups=[dict(custom=False, name="TEST", id="HELLO", children=[dict(weight=10, id="TEST")])],
            column="hostname",
            custom=True,
            descriptions=dict(general="TEST", checks={"0": "DESC"}),
            name="TEST",
            status=1,
            apiEndpoint="/table",
            webEndpoint="report",
            id="ID",
            checks=dict(),
            result=dict(),
        )
        self.assertIsInstance(intent, imodels.IntentCheck)
