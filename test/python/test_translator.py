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
        expected = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"
        self.assertEqual(actual, expected)

    def test_quotes_around_all_words_with_single_spaces(self):
        actual = self.translate(['"hEllO 38 WorlD"'])
        expected = "O.OO.......OO.O.O.O.O.O.OOOOO.O..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."
        self.assertEqual(actual, expected)

    def test_quotes_around_all_words_with_multiple_spaces(self):
        # multiple quoted spaces are treated as single spaces
        actual = self.translate(['"hEllO    38            WorlD"'])
        expected = "O.OO.......OO.O.O.O.O.O.OOOOO.O..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."
        self.assertEqual(actual, expected)

    def test_unquoted_words_with_single_spaces(self):
        actual = self.translate(["hEllO 38 WorlD"])
        expected = "O.OO.......OO.O.O.O.O.O.OOOOO.O..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."
        self.assertEqual(actual, expected)

    def test_unquoted_words_with_multiple_spaces(self):
        actual = self.translate(["hEllO    38            WorlD"])
        expected = "O.OO.......OO.O.O.O.O.O.OOOOO.O..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."
        self.assertEqual(actual, expected)

    def test_some_quoted_words_with_multiple_spaces(self):
        # trailing/leading spaces are stripped
        actual = self.translate([' hEllO    "  38            WorlD  "   '])
        expected = "O.OO.......OO.O.O.O.O.O.OOOOO.O..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."
        self.assertEqual(actual, expected)

    def test_one_short_number(self):
        actual = self.translate(["8"])
        expected = ".O.OOOO.OO.."
        self.assertEqual(actual, expected)

    def test_one_long_number(self):
        actual = self.translate(["1672"])
        expected = ".O.OOOO.....OOO...OOOO..O.O..."
        self.assertEqual(actual, expected)

    def test_one_number_with_spaces(self):
        # trailing/leading spaces are stripped
        actual = self.translate(["    1672 "])
        expected = ".O.OOOO.....OOO...OOOO..O.O..."
        self.assertEqual(actual, expected)

    def test_one_word(self):
        actual = self.translate(["scuba"])
        expected = ".OO.O.OO....O...OOO.O...O....."
        self.assertEqual(actual, expected)

    def test_one_word_with_spaces(self):
        # trailing/leading spaces are stripped
        actual = self.translate(["  scuba         "])
        expected = ".OO.O.OO....O...OOO.O...O....."
        self.assertEqual(actual, expected)

    def translate(self, message: list[str]) -> str:
        """Translates the given message and returns the result."""
        command = ["python3", self.translator_script_path, *message]
        result = subprocess.run(command, capture_output=True, text=True)
        result = result.stdout.strip()
        return result


if __name__ == '__main__':
    unittest.main()

