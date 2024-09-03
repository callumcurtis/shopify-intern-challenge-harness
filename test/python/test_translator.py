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

    def test_example_0_english_to_braille(self):
        # This test comes from the starter repo
        actual = self.translate(["Abc", "123", "xYz"])
        expected = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"
        self.assertEqual(actual, expected)

    def test_example_0_braille_to_english(self):
        actual = self.translate([".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"])
        expected = "Abc 123 xYz"
        self.assertEqual(actual, expected)

    def test_example_1_english_to_braille(self):
        # This test comes from the starter repo
        actual = self.translate(["Hello", "world"])
        expected = ".....OO.OO..O..O..O.O.O.O.O.O.O..OO........OOO.OO..OO.O.OOO.O.O.O.OO.O.."
        self.assertEqual(actual, expected)

    def test_example_1_braille_to_english(self):
        actual = self.translate([".....OO.OO..O..O..O.O.O.O.O.O.O..OO........OOO.OO..OO.O.OOO.O.O.O.OO.O.."])
        expected = "Hello world"
        self.assertEqual(actual, expected)

    def test_example_2_english_to_braille(self):
        # This test comes from the starter repo
        actual = self.translate(["42"])
        expected = ".O.OOOOO.O..O.O..."
        self.assertEqual(actual, expected)

    def test_example_2_braille_to_english(self):
        actual = self.translate([".O.OOOOO.O..O.O..."])
        expected = "42"
        self.assertEqual(actual, expected)

    def test_example_3_braille_to_english(self):
        # This test comes from the starter repo
        actual = self.translate([".....OO.....O.O...OO...........O.OOOO.....O.O...OO...."])
        expected = "Abc 123"
        self.assertEqual(actual, expected)

    def test_example_3_english_to_braille(self):
        actual = self.translate(["Abc", "123"])
        expected = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO...."
        self.assertEqual(actual, expected)

    def test_mixed_case_braille(self):
        actual = self.translate(["O.OO.......OO..O..O.O.O.O.O.O......OO..OO........O.OOOOO....O.OO.............O.OOO.OO..OO.O.OOO.O.O.O......OOO.O.."])
        expected = "hEllO 38 WorlD"
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

    def test_one_long_number_english(self):
        actual = self.translate(["1672"])
        expected = ".O.OOOO.....OOO...OOOO..O.O..."
        self.assertEqual(actual, expected)

    def test_one_long_number_braille(self):
        actual = self.translate([".O.OOOO.....OOO...OOOO..O.O..."])
        expected = "1672"
        self.assertEqual(actual, expected)

    def test_one_number_with_spaces_english(self):
        # trailing/leading spaces are stripped
        actual = self.translate(["    1672 "])
        expected = ".O.OOOO.....OOO...OOOO..O.O..."
        self.assertEqual(actual, expected)

    def test_one_number_with_spaces_braille(self):
        # trailing/leading spaces are stripped
        actual = self.translate([".......O.OOOO.....OOO...OOOO..O.O........."])
        expected = "1672"
        self.assertEqual(actual, expected)

    def test_one_word_english(self):
        actual = self.translate(["scuba"])
        expected = ".OO.O.OO....O...OOO.O...O....."
        self.assertEqual(actual, expected)

    def test_one_word_braille(self):
        actual = self.translate([".OO.O.OO....O...OOO.O...O....."])
        expected = "scuba"
        self.assertEqual(actual, expected)

    def test_one_word_with_spaces_english(self):
        # trailing/leading spaces are stripped
        actual = self.translate(["  scuba         "])
        expected = ".OO.O.OO....O...OOO.O...O....."
        self.assertEqual(actual, expected)

    def test_one_word_with_spaces_braille(self):
        # trailing/leading spaces are stripped
        actual = self.translate([".............OO.O.OO....O...OOO.O...O..........."])
        expected = "scuba"
        self.assertEqual(actual, expected)

    def test_zero_tokens(self):
        actual = self.translate([])
        expected = ""
        self.assertEqual(actual, expected)

    def test_valid_braille(self):
        actual = self.translate(["O..OO."])
        expected = "o"
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

    def test_number_followed_by_letter(self):
        actual = self.returncode([".O.OOOOO....O..OOO"])
        self.assertNotEqual(actual, 0)

    def test_number_followed_by_capitalize(self):
        actual = self.returncode([".O.OOOOO.........O"])
        self.assertNotEqual(actual, 0)

    def test_number_followed_by_numberize(self):
        actual = self.returncode([".O.OOOOO.....O.OOO"])
        self.assertNotEqual(actual, 0)

    def test_number_followed_by_nothing(self):
        actual = self.translate([".O.OOOOO...."])
        expected = "3"
        self.assertEqual(actual, expected)

    def test_english_characters(self):
        for character, expected in [
            # lowercase letters
            ("a", "O....."),
            ("b", "O.O..."),
            ("c", "OO...."),
            ("d", "OO.O.."),
            ("e", "O..O.."),
            ("f", "OOO..."),
            ("g", "OOOO.."),
            ("h", "O.OO.."),
            ("i", ".OO..."),
            ("j", ".OOO.."),
            ("k", "O...O."),
            ("l", "O.O.O."),
            ("m", "OO..O."),
            ("n", "OO.OO."),
            ("o", "O..OO."),
            ("p", "OOO.O."),
            ("q", "OOOOO."),
            ("r", "O.OOO."),
            ("s", ".OO.O."),
            ("t", ".OOOO."),
            ("u", "O...OO"),
            ("v", "O.O.OO"),
            ("w", ".OOO.O"),
            ("x", "OO..OO"),
            ("y", "OO.OOO"),
            ("z", "O..OOO"),
            # uppercase letters
            ("A", ".....OO....."),
            ("B", ".....OO.O..."),
            ("C", ".....OOO...."),
            ("D", ".....OOO.O.."),
            ("E", ".....OO..O.."),
            ("F", ".....OOOO..."),
            ("G", ".....OOOOO.."),
            ("H", ".....OO.OO.."),
            ("I", ".....O.OO..."),
            ("J", ".....O.OOO.."),
            ("K", ".....OO...O."),
            ("L", ".....OO.O.O."),
            ("M", ".....OOO..O."),
            ("N", ".....OOO.OO."),
            ("O", ".....OO..OO."),
            ("P", ".....OOOO.O."),
            ("Q", ".....OOOOOO."),
            ("R", ".....OO.OOO."),
            ("S", ".....O.OO.O."),
            ("T", ".....O.OOOO."),
            ("U", ".....OO...OO"),
            ("V", ".....OO.O.OO"),
            ("W", ".....O.OOO.O"),
            ("X", ".....OOO..OO"),
            ("Y", ".....OOO.OOO"),
            ("Z", ".....OO..OOO"),
            # numbers
            ("0", ".O.OOO.OOO.."),
            ("1", ".O.OOOO....."),
            ("2", ".O.OOOO.O..."),
            ("3", ".O.OOOOO...."),
            ("4", ".O.OOOOO.O.."),
            ("5", ".O.OOOO..O.."),
            ("6", ".O.OOOOOO..."),
            ("7", ".O.OOOOOOO.."),
            ("8", ".O.OOOO.OO.."),
            ("9", ".O.OOO.OO..."),
        ]:
            with self.subTest(character=character, expected=expected):
                actual = self.translate([character])
                self.assertEqual(actual, expected)

    def test_braille_cells(self):
        for cell, expected in [
            # lowercase letters
            ("O.....", "a"),
            ("O.O...", "b"),
            ("OO....", "c"),
            ("OO.O..", "d"),
            ("O..O..", "e"),
            ("OOO...", "f"),
            ("OOOO..", "g"),
            ("O.OO..", "h"),
            (".OO...", "i"),
            (".OOO..", "j"),
            ("O...O.", "k"),
            ("O.O.O.", "l"),
            ("OO..O.", "m"),
            ("OO.OO.", "n"),
            ("O..OO.", "o"),
            ("OOO.O.", "p"),
            ("OOOOO.", "q"),
            ("O.OOO.", "r"),
            (".OO.O.", "s"),
            (".OOOO.", "t"),
            ("O...OO", "u"),
            ("O.O.OO", "v"),
            (".OOO.O", "w"),
            ("OO..OO", "x"),
            ("OO.OOO", "y"),
            ("O..OOO", "z"),
            # uppercase letters
            (".....OO.....", "A"),
            (".....OO.O...", "B"),
            (".....OOO....", "C"),
            (".....OOO.O..", "D"),
            (".....OO..O..", "E"),
            (".....OOOO...", "F"),
            (".....OOOOO..", "G"),
            (".....OO.OO..", "H"),
            (".....O.OO...", "I"),
            (".....O.OOO..", "J"),
            (".....OO...O.", "K"),
            (".....OO.O.O.", "L"),
            (".....OOO..O.", "M"),
            (".....OOO.OO.", "N"),
            (".....OO..OO.", "O"),
            (".....OOOO.O.", "P"),
            (".....OOOOOO.", "Q"),
            (".....OO.OOO.", "R"),
            (".....O.OO.O.", "S"),
            (".....O.OOOO.", "T"),
            (".....OO...OO", "U"),
            (".....OO.O.OO", "V"),
            (".....O.OOO.O", "W"),
            (".....OOO..OO", "X"),
            (".....OOO.OOO", "Y"),
            (".....OO..OOO", "Z"),
            # numbers
            (".O.OOO.OOO..", "0"),
            (".O.OOOO.....", "1"),
            (".O.OOOO.O...", "2"),
            (".O.OOOOO....", "3"),
            (".O.OOOOO.O..", "4"),
            (".O.OOOO..O..", "5"),
            (".O.OOOOOO...", "6"),
            (".O.OOOOOOO..", "7"),
            (".O.OOOO.OO..", "8"),
            (".O.OOO.OO...", "9"),
        ]:
            with self.subTest(cell=cell, expected=expected):
                actual = self.translate([cell])
                self.assertEqual(actual, expected)

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

