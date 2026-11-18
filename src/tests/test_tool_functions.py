from textnode import TextNode, TextType
from tool_functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
import unittest

class TestTextNode(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(result, expected)


    def test_existing_bold_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(result, [node])


    def test_unclosed_delimiter(self):
        node = TextNode("Hello **world", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_images(self):
        text = "Hello ![cat](cat.png) and ![dog](dog.png)"
        matches = extract_markdown_images(text)

        expected = [
            ("cat", "cat.png"),
            ("dog", "dog.png"),
        ]

        self.assertEqual(matches, expected)

    def test_extract_images_mixed(self):
        text = "Look at ![cat](cat.png) and visit [Google](google.com)"
        matches = extract_markdown_images(text)

        expected = [("cat", "cat.png")]

        self.assertEqual(matches, expected)

    def test_extract_links(self):
        text = "Find [curso](www.boot.dev) but NOT ![dog](dog.png)"
        matches = extract_markdown_links(text)

        expected = [("curso", "www.boot.dev")]

        self.assertEqual(matches, expected)

    def test_extract_links_multiple(self):
        text = "Visit [Boot.dev](https://boot.dev) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)

        expected = [
            ("Boot.dev", "https://boot.dev"),
            ("GitHub", "https://github.com"),
        ]

        self.assertEqual(matches, expected)

    def test_split_images_multiple(self):
        node = TextNode(
            "Hello ![cat](cat.png) and ![dog](dog.png)!",
            TextType.TEXT
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_image_at_start(self):
        node = TextNode("![cat](cat.png) is cute", TextType.TEXT)

        result = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" is cute", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_links_multiple(self):
        node = TextNode(
            "Visit [Google](google.com) and [Boot.dev](boot.dev)!",
            TextType.TEXT
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "boot.dev"),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_links_existing_node(self):
        node1 = TextNode("Already bold", TextType.BOLD)
        node2 = TextNode("[Google](google.com)", TextType.TEXT)

        result = split_nodes_link([node1, node2])

        expected = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("Google", TextType.LINK, "google.com"),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_plain(self):
        text = "Hello world!"
        result = text_to_textnodes(text)

        expected = [
            TextNode("Hello world!", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_bold_italic(self):
        text = "Hello **bold** and _italic_!"
        result = text_to_textnodes(text)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "Run `python main.py` to start"
        result = text_to_textnodes(text)

        expected = [
            TextNode("Run ", TextType.TEXT),
            TextNode("python main.py", TextType.CODE),
            TextNode(" to start", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_images_links(self):
        text = "See ![cat](cat.png) and visit [Google](google.com)"
        result = text_to_textnodes(text)

        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "google.com"),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_all(self):
        text = (
            "This is **bold** with _italic_ and `code` "
            "plus ![dog](dog.png) and [Boot.dev](https://boot.dev)"
        )
        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" plus ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, expected)