import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToHTML(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_blank_lines(self):
        md = (
        "First paragraph\n\n"
        "\n\n"
        "Second paragraph\n\n\n\n"
        "Third paragraph"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )
    
    def test_leading_trailing_blank_lines(self):
        md = "\n\nThis is a block\n\nAnother block\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a block", "Another block"]
        )

    def test_only_blank_lines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "Just a single paragraph block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph block"])

    def test_list_block(self):
        md = (
            "- Item 1\n"
            "- Item 2\n"
            "- Item 3"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    def test_whitespace_blocks(self):
        md = "Block 1\n\n    \n\nBlock 2   \n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

if __name__ == "__main__":
    unittest.main()