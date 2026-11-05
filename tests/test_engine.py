"""Tests for agent-belief-revision-engine."""
import unittest
from agent_belief_revision_engine.engine import BeliefRevisionEngine


class TestBeliefRevisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BeliefRevisionEngine()

    def test_cascading_contraction(self):
        self.engine.add_belief("is_cloud", True, entrenchment=0.8)
        self.engine.add_belief("use_s3", True, entrenchment=0.6, derived_from=["is_cloud"])
        self.engine.add_belief("s3_bucket", "my-bucket", entrenchment=0.5, derived_from=["use_s3"])
        
        retracted = self.engine.contract("is_cloud")
        self.assertIn("is_cloud", retracted)
        self.assertIn("use_s3", retracted)
        self.assertIn("s3_bucket", retracted)
        self.assertEqual(len(self.engine.get_beliefs()), 0)


if __name__ == "__main__":
    unittest.main()
