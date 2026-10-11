"""Exercise the checker as a user would, against disposable Git repositories."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "check_json.py"


class JsonCheckTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)

    def add_file(self, name, contents, tracked=True):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents.encode("utf-8") if isinstance(contents, str) else contents)
        if tracked:
            subprocess.run(["git", "-C", str(self.root), "add", "--", name], check=True,
                           capture_output=True)

    def check(self):
        return subprocess.run([sys.executable, str(CHECKER), "--root", str(self.root)],
                              capture_output=True, text=True, encoding="utf-8")

    def test_valid_json_including_false_zero_arrays_and_large_numbers(self):
        fixtures = {
            "object.json": '{"nested": {"name": "evidence"}, "ok": true}',
            "false.json": "false",
            "zero.json": "0",
            "array.json": '[null, 0, false, "value"]',
            "string.json": '"review"',
            "large-number.json": "1e400",
        }
        for name, contents in fixtures.items():
            self.add_file(name, contents)
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("6 tracked JSON files", result.stdout)

    def test_only_tracked_json_is_checked_and_extension_is_case_insensitive(self):
        self.add_file("nested space/record.JSON", "{}")
        self.add_file("scratch.json", "not JSON", tracked=False)
        self.add_file("notes.txt", "not JSON")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 tracked JSON files", result.stdout)
        self.add_file("nested space/record.JSON", '{"broken":}')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("nested space/record.JSON", result.stderr)

    def test_malformed_json_reports_path_and_line(self):
        self.add_file("examples/broken.json", '{\n  "value": true,\n}')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("examples/broken.json", result.stderr)
        self.assertIn("line 3", result.stderr)

    def test_duplicate_keys_are_rejected_even_when_nested_or_escaped(self):
        self.add_file("duplicate.json", r'{"record": {"name": 1, "\u006eame": 2}}')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate object key 'name'", result.stderr)

    def test_nan_and_infinity_tokens_are_rejected(self):
        for token in ["NaN", "Infinity", "-Infinity"]:
            with self.subTest(token=token):
                self.add_file("nonfinite.json", '{"score": ' + token + '}')
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn(f"{token} is not a JSON number", result.stderr)

    def test_invalid_utf8_and_bom_are_rejected(self):
        for content, expected in [(b'{"name": "\xff"}', "utf-8"),
                                  (b"\xef\xbb\xbf{}", "byte-order mark")]:
            with self.subTest(content=content):
                self.add_file("encoding.json", content)
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)

    def test_all_failures_are_reported(self):
        self.add_file("one.json", "{")
        self.add_file("two.json", "[1,]")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("one.json", result.stderr)
        self.assertIn("two.json", result.stderr)
        self.assertIn("2 of 2", result.stderr)

    def test_empty_scan_does_not_pass_silently(self):
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no tracked JSON files found", result.stderr)

    def test_symlink_to_outside_repository_fails(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "record.json"
            target.write_text("{}", encoding="utf-8")
            try:
                (self.root / "record.json").symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable on this system")
            subprocess.run(["git", "-C", str(self.root), "add", "--", "record.json"], check=True,
                           capture_output=True)
            result = self.check()
            self.assertEqual(result.returncode, 1)
            self.assertIn("resolves outside the repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
