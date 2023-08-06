"""Tests using invalid default files for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))
TEST_DEFAULT_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_default_files"))


class TestInvalidCasesWithDefaultFiles(unittest.TestCase):
    """Invalid test cases using default files."""

    def test_invalid_standalone(self):
        """Check if exception is raised if standalone is true."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "standalone_true.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("The default standalone should be set to false.", message)

    def test_invalid_self_contained(self):
        """Check if exception is raised if self-contained is true."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "selfcontained_true.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("The default self-contained should be set to false.", message)

    def test_no_input_format(self):
        """Check if exception is raised if no input format is specified."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "no_input_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("No input format specified.", message)

    def test_invalid_reader_input_format(self):
        """Check if exception is raised if reader input format is invalid."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "invalid_reader_input_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Input type has to be a Markdown variant.", message)

    def test_invalid_from_input_format(self):
        """Check if exception is raised if from input format is invalid."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "invalid_from_input_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Input type has to be a Markdown variant.", message)

    def test_from_reader_both_given(self):
        """Check if exception is raised if from and reader are both given."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "from_reader_both_given.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual(
            (
                "Specifying both from and reader is not supported."
                " Please specify just one."
            ),
            message,
        )

    def test_to_writer_both_given(self):
        """Check if exception is raised if to and writer are both given."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "to_writer_both_given.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual(
            (
                "Specifying both to and writer is not supported."
                " Please specify just one."
            ),
            message,
        )

    def test_no_output_format(self):
        """Check if exception is raised if no output format is specified."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "no_output_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Output format type must be either html or html5.", message)

    def test_invalid_writer_output_format(self):
        """Check if exception is raised if writer output format is invalid."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "invalid_writer_output_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Output format type must be either html or html5.", message)

    def test_invalid_to_output_format(self):
        """Check if exception is raised if to output format is invalid."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "invalid_to_output_format.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Output format type must be either html or html5.", message)


if __name__ == "__main__":
    unittest.main()
