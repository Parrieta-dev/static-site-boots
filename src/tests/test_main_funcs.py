import unittest
from main import extract_title


class TestMainFunctions(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Tolkien Fan Club"
        self.assertEqual(extract_title(markdown), "Tolkien Fan Club")

    def test_extract_title_multiline(self):
        markdown = """## Subtitle
Some paragraph

# Main Title

### Another heading"""
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_extract_title_missing(self):
        markdown = """## Subtitle
### Another heading
Just a normal paragraph"""

        with self.assertRaises(Exception):
            extract_title(markdown)