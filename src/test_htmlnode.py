
import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_single_prop(self):
        node = HTMLNode("a", "Click here", None, {"href": "https://boot.dev"})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev"'
        )

    def test_multiple_props(self):
        node = HTMLNode("a", "Click here", None, {
            "href": "https://boot.dev",
            "target": "_blank"
        })
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" target="_blank"'
        )

    def test_no_props(self):
        node = HTMLNode("p", "Hello world", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode("div", None, None, {})
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
