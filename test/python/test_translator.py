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

        # Command to run translator.py script
        command = ["python3", self.translator_script_path, "Abc", "123", "xYz"]

        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)

        # Expected output without the newline at the end
        expected_output = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"

        # Strip any leading/trailing whitespace from the output and compare
        self.assertEqual(result.stdout.strip(), expected_output)


if __name__ == '__main__':
    unittest.main()

