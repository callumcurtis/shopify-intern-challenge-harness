from __future__ import annotations

import unittest
import subprocess
import pathlib


class TestTranslator(unittest.TestCase):

    def setUp(self):
        repo_root_path = pathlib.Path(
            subprocess.Popen(
                ['git', 'rev-parse', '--show-toplevel'],
                stdout=subprocess.PIPE
            ).communicate()
            [0]
            .rstrip()
            .decode('utf-8')
        )

        translator_script_path = repo_root_path / "eng-intern-challenge" / "python" / "translator.py"
        assert translator_script_path.is_file()

        self.translator_script_path = translator_script_path

    def test_output(self):
        # This test comes from the starter repo
        actual = self.translate(["Abc", "123", "xYz"])
        expected_output = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"
        self.assertEqual(actual, expected_output)

    def translate(self, message: list[str]) -> str:
        """Translates the given message and returns the result."""
        command = ["python3", self.translator_script_path, *message]
        result = subprocess.run(command, capture_output=True, text=True)
        result = result.stdout.strip()
        return result


if __name__ == '__main__':
    unittest.main()

