import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type


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


    def test_heading_levels(self):
        for level in range(1, 7):
            block = "#" * level + " Heading level " + str(level)
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # More than 6 hashes is paragraph
        self.assertEqual(block_to_block_type("####### Heading level 7"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> This is a quote\n> Still a quote"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

        # Leading spaces before >
        quote_with_space = "   > Quote with leading spaces\n\t> Another quote line"
        self.assertEqual(block_to_block_type(quote_with_space), BlockType.QUOTE)

        # Mixed lines (one doesn't start with >)
        mixed = "> Quote line\nNot a quote"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

        # Lines not all starting with "- "
        mixed = "- Item one\nWrong line\n- Item two"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

        # Numbers start at 2, invalid
        invalid_start = "2. First item\n3. Second item"
        self.assertEqual(block_to_block_type(invalid_start), BlockType.PARAGRAPH)

        # Numbers not incrementing by 1
        invalid_increment = "1. First item\n3. Second item"
        self.assertEqual(block_to_block_type(invalid_increment), BlockType.PARAGRAPH)

        # Lines without numbers
        no_numbers = "One. First item\nTwo. Second item"
        self.assertEqual(block_to_block_type(no_numbers), BlockType.PARAGRAPH)

    def test_paragraph(self):
        paragraph = "This is just a normal paragraph, without any special markdown."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

        # Empty string returns paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

        # Lines that don't match any pattern
        multiline = "This is line one\nThis is line two"
        self.assertEqual(block_to_block_type(multiline), BlockType.PARAGRAPH)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main() 