import unittest
from md_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMdBlocks(unittest.TestCase):
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
    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_excessive_newlines(self):
        md = "First block\n\n\n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"]
        )

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"),
            BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```\nprint('hello')"),
            BlockType.PARAGRAPH
        )

    def test_quotes_and_unordered_lists(self):
        self.assertEqual(
            block_to_block_type("> First line\n> Second line"),
            BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("> First line\nSecond line"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- First item\n- Second item"),
            BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- First item\nSecond item"),
            BlockType.PARAGRAPH
        )

    def test_ordered_lists_and_paragraphs(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"),
            BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. First\n3. Second"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("2. First\n3. Second"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH
        )