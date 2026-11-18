import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Im a link!", {"href": "www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="www.boot.dev">Im a link!</a>')

    def test_repr(self):
        node = LeafNode("a", "Im a link!", {"href": "www.boot.dev"})
        self.assertEqual(repr(node), "LeafNode(TAG=a, VALUE=Im a link!, PROPS={'href': 'www.boot.dev'})" )

    def test_to_html_ValueError(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()