import unittest
import sys
import os

# Add parent directory to path so cli module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.validator import (
    check_rule_02,
    check_rule_10,
    check_rule_13,
    check_rule_21,
    check_rule_24,
    validate_trajectory
)

class TestAgentfullValidator(unittest.TestCase):

    def test_rule_02_all_present(self):
        """Rule 02: Emojis, headers, tables all present should PASS."""
        outputs = [
            "## Section Title\nSome content with an emoji 😊\n\n| Col1 | Col2 |\n|---|---|\n| val1 | val2 |"
        ]
        res = check_rule_02(outputs)
        self.assertTrue(res["passed"])
        self.assertTrue(res["has_emoji"])
        self.assertTrue(res["has_header"])
        self.assertTrue(res["has_table"])
        self.assertEqual(len(res["details"]), 0)

    def test_rule_02_missing_emoji(self):
        """Rule 02: Missing emoji should FAIL."""
        outputs = [
            "## Section Title\nSome content without emoji\n\n| Col1 | Col2 |\n|---|---|\n| val1 | val2 |"
        ]
        res = check_rule_02(outputs)
        self.assertFalse(res["passed"])
        self.assertFalse(res["has_emoji"])
        self.assertTrue(res["has_header"])
        self.assertTrue(res["has_table"])
        self.assertIn("Missing emojis", res["details"])

    def test_rule_02_missing_header(self):
        """Rule 02: Missing header should FAIL."""
        outputs = [
            "Some content with emoji 😊\n\n| Col1 | Col2 |\n|---|---|\n| val1 | val2 |"
        ]
        res = check_rule_02(outputs)
        self.assertFalse(res["passed"])
        self.assertTrue(res["has_emoji"])
        self.assertFalse(res["has_header"])
        self.assertTrue(res["has_table"])
        self.assertIn("Missing markdown headers", res["details"])

    def test_rule_02_missing_table(self):
        """Rule 02: Missing table should FAIL."""
        outputs = [
            "## Section Title\nSome content with emoji 😊\nNot a real table: | col1 | col2 |"
        ]
        res = check_rule_02(outputs)
        self.assertFalse(res["passed"])
        self.assertTrue(res["has_emoji"])
        self.assertTrue(res["has_header"])
        self.assertFalse(res["has_table"])
        self.assertIn("Missing markdown tables", res["details"])

    def test_rule_10_no_secrets(self):
        """Rule 10: Clean output should PASS."""
        texts = [
            "This is a clean response with no keys.",
            "api_key = 'val'"  # value is too short to trigger generic assignment match (< 8 chars)
        ]
        res = check_rule_10(texts)
        self.assertTrue(res["passed"])
        self.assertEqual(len(res["secrets"]), 0)

    def test_rule_10_has_openai_key(self):
        """Rule 10: OpenAI key present should FAIL."""
        texts = [
            "Using OpenAI key sk-" + "a" * 48
        ]
        res = check_rule_10(texts)
        self.assertFalse(res["passed"])
        self.assertIn("OpenAI API Key", res["secrets"])

    def test_rule_10_has_github_token(self):
        """Rule 10: GitHub token present should FAIL."""
        texts = [
            "My token is ghp_" + "b" * 36
        ]
        res = check_rule_10(texts)
        self.assertFalse(res["passed"])
        self.assertIn("GitHub Token", res["secrets"])

    def test_rule_10_generic_secret_assignment(self):
        """Rule 10: Generic secret assignment should FAIL."""
        texts = [
            'db_password = "supersecretpassword123"'
        ]
        res = check_rule_10(texts)
        self.assertFalse(res["passed"])
        self.assertTrue(any("Generic Credentials Assignment" in s for s in res["secrets"]))

    def test_rule_13_no_loop(self):
        """Rule 13: Distinct tool calls should PASS."""
        tool_calls = [
            {"name": "bash", "arguments": "ls"},
            {"name": "read", "arguments": "file.txt"},
            {"name": "bash", "arguments": "ls"},
        ]
        res = check_rule_13(tool_calls)
        self.assertTrue(res["passed"])
        self.assertEqual(len(res["loops"]), 0)

    def test_rule_13_loop_detected(self):
        """Rule 13: 3 consecutive identical tool calls should FAIL."""
        tool_calls = [
            {"name": "bash", "arguments": {"command": "ls"}},
            {"name": "bash", "arguments": {"command": "ls"}},
            {"name": "bash", "arguments": {"command": "ls"}},
        ]
        res = check_rule_13(tool_calls)
        self.assertFalse(res["passed"])
        self.assertEqual(len(res["loops"]), 1)
        self.assertEqual(res["loops"][0]["tool"], "bash")
        self.assertEqual(res["loops"][0]["consecutive_calls"], 3)

    def test_rule_21_under_budget(self):
        """Rule 21: Token usage under limit should PASS."""
        # Test dict format with telemetry metrics
        log_dict = {
            "telemetry": {
                "metrics": {
                    "total_tokens": 50000
                }
            }
        }
        res = check_rule_21(log_dict, task_type="coding")
        self.assertTrue(res["passed"])
        self.assertEqual(res["total_tokens"], 50000)

        # Test list of steps format
        log_list = [
            {"token_usage": {"total": 30000}},
            {"token_usage": {"total": 40000}},
        ]
        res2 = check_rule_21(log_list, task_type="coding")
        self.assertTrue(res2["passed"])
        self.assertEqual(res2["total_tokens"], 70000)

    def test_rule_21_over_budget(self):
        """Rule 21: Token usage over limit should FAIL."""
        log_dict = {
            "telemetry": {
                "metrics": {
                    "total_tokens": 600000
                }
            }
        }
        res = check_rule_21(log_dict, task_type="coding") # coding limit is 500k
        self.assertFalse(res["passed"])

        # Override limit
        res2 = check_rule_21(log_dict, task_type="coding", custom_limit=1000000)
        self.assertTrue(res2["passed"])

    def test_rule_24_valid_telemetry(self):
        """Rule 24: Valid telemetry should PASS."""
        log_dict = {
            "telemetry": {
                "session": "session-123",
                "metrics": {
                    "total_steps": 5
                }
            }
        }
        res = check_rule_24(log_dict)
        self.assertTrue(res["passed"])

    def test_rule_24_missing_telemetry(self):
        """Rule 24: Missing telemetry should FAIL."""
        log_dict = {
            "steps": []
        }
        res = check_rule_24(log_dict)
        self.assertFalse(res["passed"])

    def test_validate_trajectory_integration(self):
        """Integration validation test with a full trajectory."""
        trajectory = {
            "telemetry": {
                "session": "test-session",
                "metrics": {
                    "total_tokens": 45000
                }
            },
            "steps": [
                {
                    "role": "agent",
                    "content": "## Step 1\nLet's check details: 😊\n| A | B |\n|---|---|\n| 1 | 2 |",
                    "tool_calls": [
                        {"name": "bash", "arguments": "ls"}
                    ]
                },
                {
                    "role": "tool",
                    "content": "file1.txt"
                },
                {
                    "role": "agent",
                    "content": "## Step 2\nDone! 🟢",
                    "tool_calls": [
                        {"name": "read", "arguments": "file1.txt"}
                    ]
                }
            ]
        }
        res = validate_trajectory(trajectory)
        self.assertTrue(res["all_passed"])
        self.assertTrue(res["rules"]["Rule 02"]["passed"])
        self.assertTrue(res["rules"]["Rule 10"]["passed"])
        self.assertTrue(res["rules"]["Rule 13"]["passed"])
        self.assertTrue(res["rules"]["Rule 21"]["passed"])
        self.assertTrue(res["rules"]["Rule 24"]["passed"])

if __name__ == '__main__':
    unittest.main()
