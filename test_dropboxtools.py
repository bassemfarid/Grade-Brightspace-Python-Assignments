"""Unittests for dropboxtools."""

import unittest
import dropboxtools


class FileCheckTestCase(unittest.TestCase):
    """Tests for file_check."""

    def test_valid_filenames(self):
        """Test all valid filenames with a True assert."""
        valid_filenames = [
            '4436593-32053592 - Kaavish H- May 26, 2023 841 AM - flowchart.assignment4.drawio.png',
            '5338034-32053592 - Will T- May 29, 2023 223 PM - 2.py',
            '4445693-32053592 - Maria R- May 29, 2023 846 AM - 4 (1).py',
            '4428874-32053592 - Rony W- May 24, 2023 233 PM - Fibonnaci Flowchart.png'
        ]
        for filename in valid_filenames:
            with self.subTest(filename=filename):
                self.assertTrue(dropboxtools.file_check(
                    filename), f"Failed for filename: {filename}")

    def test_invalid_filenames(self):
        """Test all invalid filenames with a False assert."""
        invalid_filenames = [
            'invalid_filename.txt',
            '2(3)',
            '2(3).c',
            '4428874-32053592 - Rony W- May 24, 2023 233 PM'
        ]
        for filename in invalid_filenames:
            with self.subTest(filename=filename):
                self.assertFalse(dropboxtools.file_check(
                    filename), f"Failed for filename: {filename}")


if __name__ == '__main__':
    unittest.main()
