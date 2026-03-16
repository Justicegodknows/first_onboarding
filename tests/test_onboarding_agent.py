"""Tests for the onboarding agent."""

import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from onboarding_agent import COMMON_CHECKLIST, RESOURCES, run_onboarding


class TestOnboardingAgent(unittest.TestCase):
    """Unit tests for onboarding_agent.py"""

    def _make_inputs(self, name, start_date, dept_num, role, manager, save="no"):
        """Build an iterator of inputs for run_onboarding()."""
        return iter([name, start_date, str(dept_num), role, manager, save])

    def test_run_onboarding_engineering(self):
        """Engineering department produces engineering-specific resources."""
        inputs = self._make_inputs("Alice Smith", "2026-04-01", 1, "Software Engineer", "Bob", "no")
        with patch("builtins.input", side_effect=inputs):
            profile = run_onboarding()

        self.assertEqual(profile["name"], "Alice Smith")
        self.assertEqual(profile["role"], "Software Engineer")
        self.assertEqual(profile["department"], "engineering")
        self.assertEqual(profile["manager"], "Bob")
        self.assertEqual(profile["start_date"], "2026-04-01")
        self.assertIn("onboarded_at", profile)
        self.assertIn("checklist", profile)
        self.assertEqual(profile["checklist"]["common"], COMMON_CHECKLIST)
        self.assertEqual(profile["checklist"]["department_specific"], RESOURCES["engineering"])

    def test_run_onboarding_design(self):
        """Design department produces design-specific resources."""
        inputs = self._make_inputs("Jane Doe", "2026-05-01", 2, "UX Designer", "", "no")
        with patch("builtins.input", side_effect=inputs):
            profile = run_onboarding()

        self.assertEqual(profile["department"], "design")
        self.assertEqual(profile["checklist"]["department_specific"], RESOURCES["design"])

    def test_run_onboarding_saves_file(self):
        """Profile is saved to a JSON file when the user confirms."""
        inputs = self._make_inputs("Test User", "2026-06-01", 3, "Analyst", "Manager", "yes")
        expected_filename = "onboarding_test_user.json"
        if os.path.exists(expected_filename):
            os.remove(expected_filename)

        try:
            with patch("builtins.input", side_effect=inputs):
                profile = run_onboarding()

            self.assertTrue(os.path.exists(expected_filename))
            with open(expected_filename, encoding="utf-8") as fh:
                saved = json.load(fh)
            self.assertEqual(saved["name"], "Test User")
            self.assertEqual(saved["department"], "product")
        finally:
            if os.path.exists(expected_filename):
                os.remove(expected_filename)

    def test_run_onboarding_does_not_save_file_when_declined(self):
        """No file is created when the user declines to save."""
        inputs = self._make_inputs("No Save", "2026-07-01", 5, "Intern", "", "no")
        expected_filename = "onboarding_no_save.json"
        if os.path.exists(expected_filename):
            os.remove(expected_filename)

        with patch("builtins.input", side_effect=inputs):
            run_onboarding()

        self.assertFalse(os.path.exists(expected_filename))

    def test_resources_have_all_departments(self):
        """RESOURCES dict covers the expected departments."""
        expected_depts = {"engineering", "design", "product", "marketing", "other"}
        self.assertEqual(set(RESOURCES.keys()), expected_depts)

    def test_common_checklist_is_not_empty(self):
        """COMMON_CHECKLIST has at least one item."""
        self.assertGreater(len(COMMON_CHECKLIST), 0)

    def test_empty_name_re_prompts(self):
        """An empty name is rejected and the user is re-prompted."""
        inputs = iter(["", "Valid Name", "2026-08-01", "1", "Engineer", "", "no"])
        with patch("builtins.input", side_effect=inputs):
            profile = run_onboarding()

        self.assertEqual(profile["name"], "Valid Name")


if __name__ == "__main__":
    unittest.main()
