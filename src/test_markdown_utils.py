import unittest
from markdown_utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_h1_with_whitespace(self):
        markdown = "#   Hello World  "
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_h1_in_multiline(self):
        markdown = """Some text
# My Title
Some other text"""
        self.assertEqual(extract_title(markdown), "My Title")
    
    def test_no_h1(self):
        markdown = "Some text\nNo header here"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in Markdown")
    
    def test_only_h2(self):
        markdown = "## Subheader"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in Markdown")
    
    def test_multiple_h1(self):
        markdown = "# First\n\n# Second"
        self.assertEqual(extract_title(markdown), "First")
    
    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in Markdown")
    
    def test_h1_with_extra_hash(self):
        markdown = "# Title # Extra"
        self.assertEqual(extract_title(markdown), "Title # Extra")

if __name__ == "__main__":
    unittest.main()