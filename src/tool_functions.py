from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

        case _:
            raise ValueError(f"Unknown TextType: {text_node.text_type}")

def text_to_textnodes(text) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

# Example Nodes:
# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        i = 0
        
        if len(split_text) % 2 == 0:
            raise Exception("The delimiter did not have another closing delimiter. Wrong markdown syntax")
        
        for sentence in split_text:
            if sentence == "":
                continue
            new_node = TextNode(sentence, TextType.TEXT if i % 2 == 0 else text_type)
            new_nodes.append(new_node)
            i += 1

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in images:
            prev_text, remaining_text = text.split(f"![{alt}]({url})", 1)
            if prev_text:
                text_node = TextNode(prev_text, TextType.TEXT)
                new_nodes.append(text_node)
            img_node = TextNode(alt, TextType.IMAGE, url)
            new_nodes.append(img_node)
            text = remaining_text

        if text:
            text_node = TextNode(text, TextType.TEXT)
            new_nodes.append(text_node)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in links:
            prev_text, remaining_text = text.split(f"[{alt}]({url})", 1)
            if prev_text:
                text_node = TextNode(prev_text, TextType.TEXT)
                new_nodes.append(text_node)
            link_node = TextNode(alt, TextType.LINK, url)
            new_nodes.append(link_node)
            text = remaining_text
        if text:
            text_node = TextNode(text, TextType.TEXT)
            new_nodes.append(text_node)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    pattern_img = r"!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern_img, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    pattern_link = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern_link, text)
    return matches

