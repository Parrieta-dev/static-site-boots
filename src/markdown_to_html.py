from htmlnode import ParentNode, LeafNode
from md_blocks import markdown_to_blocks, block_to_block_type, BlockType
from tool_functions import text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType

def text_to_children(text:str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children = []

    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)

    return children

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            heading_lvl = len(block) - len(block.lstrip("#"))
            tag = f"h{heading_lvl}"
            leaf_nodes = text_to_children(block[heading_lvl+1:])
            block_nodes.append(ParentNode(tag, leaf_nodes))
            continue

        if block_type == BlockType.QUOTE:
            tag = "blockquote"
            lines = block.split("\n")
            clean_lines = []

            for line in lines:
                quote_text = line[1:].lstrip()
                clean_lines.append(quote_text)

            leaf_nodes = text_to_children(" ".join(clean_lines))
            block_nodes.append(ParentNode(tag, leaf_nodes))
            continue

        if block_type == BlockType.UNORDERED_LIST:
            tag1 = "ul"
            tag2 = "li"

            lines = block.split("\n")
            line_nodes = []

            for line in lines:
                line_nodes.append(ParentNode(tag2, text_to_children(line[2:])))

            block_nodes.append(ParentNode(tag1, line_nodes))
            continue

        if block_type == BlockType.ORDERED_LIST:
            tag1 = "ol"
            tag2 = "li"

            lines = block.split("\n")
            line_nodes = []

            for i, line in enumerate(lines, start=1):
                jump_string = f"{i}. "
                line_nodes.append(ParentNode(tag2, text_to_children(line[len(jump_string):])))

            block_nodes.append(ParentNode(tag1, line_nodes))
            continue

        if block_type == BlockType.CODE:
            code_text = block[4:-3]

            text_node = TextNode(code_text, TextType.TEXT)
            leaf_node = text_node_to_html_node(text_node)

            code_node = ParentNode("code", [leaf_node])
            pre_node = ParentNode("pre", [code_node])

            block_nodes.append(pre_node)
            continue

        leaf_nodes = text_to_children(block.replace("\n", " "))
        block_nodes.append(ParentNode("p", leaf_nodes)) # El p lo cambiaremos luego por una variable tag asociada a blocktype

    html_root = ParentNode("div", block_nodes)
    return html_root

def main():
    markdown = """
### Mi _título_


> Estas son
>mis
> quotes **super** epicas


- Esta es mi lista
- rabiosa y maligna
- _diablo_ letal! Metal.


```
This is **bold** text
print("Hello world")
```


1. Mañana
2. por _la_ mañana
3. la araña de
4.  España
5. araña con
6. maña su
7. telaraña.
8. I do
9. not want to
10. be set free.


Hello **world** es
un puto fiera
"""
    html_node = markdown_to_html_node(markdown)
    print(html_node.to_html())

if __name__ == "__main__":
    main()