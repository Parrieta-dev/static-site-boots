
import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    # Official Boot.dev tests
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    # Additional tests
    def test_headings(self):
        md = """# Main **title**

###### Small _heading_"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Main <b>title</b></h1><h6>Small <i>heading</i></h6></div>"
        )

    def test_quotes(self):
        md = """> First line
>Second **bold** line
> Third _italic_ line"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First line Second <b>bold</b> line Third <i>italic</i> line</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """- First item
- Second **bold** item
- Third _italic_ item"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second <b>bold</b> item</li><li>Third <i>italic</i> item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "\n".join(
            f"{i}. Item {i}" for i in range(1, 11)
        )

        html = markdown_to_html_node(md).to_html()
        expected_items = "".join(
            f"<li>Item {i}</li>" for i in range(1, 11)
        )

        self.assertEqual(
            html,
            f"<div><ol>{expected_items}</ol></div>"
        )


if __name__ == "__main__":
    unittest.main()
