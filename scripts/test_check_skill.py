"""Regression tests for conservative structure checks."""
import tempfile
import unittest
from pathlib import Path
from check_skill import check


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def entry(self, body="Do the task.", name="example-task"):
        (self.root / "SKILL.md").write_text(
            f'---\nname: {name}\ndescription: "Use for incoming reports."\n---\n{body}\n',
            encoding="utf-8")

    def test_minimal_valid(self):
        self.entry()
        self.assertEqual(check(self.root)[0], [])

    def test_missing_entry(self):
        self.assertTrue(check(self.root)[0])

    def test_bad_yaml(self):
        self.entry()
        (self.root / "SKILL.md").write_text('---\nname: demo\ndescription: "unclosed\n---\nDo it.')
        self.assertTrue(check(self.root)[0])

    def test_markdown_link(self):
        self.entry('Read [rules](references/missing.md).')
        self.assertTrue(check(self.root)[0])

    def test_bad_name(self):
        self.entry(name="Wrong Name")
        self.assertTrue(check(self.root)[0])

    def test_placeholder(self):
        self.entry("TODO: complete")
        self.assertTrue(check(self.root)[0])

    def test_missing_reference(self):
        self.entry("Read `references/missing.md`.")
        self.assertTrue(check(self.root)[0])

    def test_existing_reference(self):
        (self.root / "references").mkdir()
        (self.root / "references" / "rules.md").write_text("Rule")
        self.entry("Read `references/rules.md`.")
        self.assertEqual(check(self.root)[0], [])

    def test_author_absolute_path(self):
        self.entry("Read /workspace/private/data.json")
        self.assertTrue(check(self.root)[0])

    def test_traversal_reference(self):
        self.entry("Read `references/../../outside.md`.")
        self.assertTrue(check(self.root)[0])


if __name__ == "__main__":
    unittest.main()
