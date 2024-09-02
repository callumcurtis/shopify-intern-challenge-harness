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

    def test_zero_tokens(self):
        actual = self.translate([])
        expected = ""
        self.assertEqual(actual, expected)

    def test_valid_braille(self):
        actual = self.translate(["O..OO."])
        expected = "O"
        self.assertEqual(actual, expected)

    def test_braille_indivisible_by_6(self):
        actual = self.returncode(["O..OO"])
        self.assertNotEqual(actual, 0)

    def test_non_braille_characters(self):
        # non-braille characters indicate the message is in English
        actual = self.translate(["OOAOOO"])
        expected = "O..OO.O..OO.O.....O..OO.O..OO.O..OO."
        self.assertEqual(actual, expected)

    def test_space_inside_braille(self):
        actual = self.translate(["OO OOO"])
        expected = "O..OO.O..OO.......O..OO.O..OO.O..OO."
        self.assertEqual(actual, expected)

    def test_period_inside_english(self):
        # since A is non-braille, the message must be in English,
        # but the "." characters are not in the English alphabet
        actual = self.returncode(["O..A.O"])
        self.assertNotEqual(actual, 0)

    def test_capitalize(self):
        actual = self.translate([".....OO....."])
        expected = "A"
        self.assertEqual(actual, expected)

    def test_single_character_is_capitalized(self):
        actual = self.translate([".....OO.....O....."])
        expected = "Aa"
        self.assertEqual(actual, expected)

    def test_capitalize_followed_by_nothing(self):
        actual = self.returncode([".....O"])
        self.assertNotEqual(actual, 0)

    def test_capitalize_followed_by_space(self):
        actual = self.returncode([".....O......"])
        self.assertNotEqual(actual, 0)

    def test_capitalize_followed_by_number(self):
        actual = self.returncode([".....O.O.OOO"])
        self.assertNotEqual(actual, 0)

    def test_capitalize_followed_by_capitalize(self):
        actual = self.returncode([".....O.....O"])
        self.assertNotEqual(actual, 0)

    def test_numberize_followed_by_space(self):
        actual = self.returncode([".O.OOO......"])
        self.assertNotEqual(actual, 0)

    def test_numberize_followed_by_letter(self):
        actual = self.returncode([".O.OOOOO.OOO"])
        self.assertNotEqual(actual, 0)

    def test_numberize_followed_by_capital(self):
        actual = self.returncode([".O.OOO.....O"])
        self.assertNotEqual(actual, 0)

    def test_numberize_followed_by_numberize(self):
        actual = self.returncode([".O.OOO.O.OOO"])
        self.assertNotEqual(actual, 0)

    def test_numberize_followed_by_nothing(self):
        actual = self.returncode([".O.OOO"])
        self.assertNotEqual(actual, 0)

    def translate(self, message: list[str]) -> str:
        """Translates the given message and returns the result."""
        return self._translate_in_subprocess(message).stdout.strip()

    def returncode(self, message: list[str]) -> int:
        """Translates the given message and returns the return code."""
        return self._translate_in_subprocess(message).returncode

    def _translate_in_subprocess(self, message: list[str]) -> subprocess.CompletedProcess:
        command = ["python3", self.translator_script_path, *message]
        subp = subprocess.run(command, capture_output=True, text=True)
        return subp


if __name__ == '__main__':
    unittest.main()

