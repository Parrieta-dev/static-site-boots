from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []

    cut_text = markdown.split("\n\n")

    for block in cut_text:
        block = block.strip()
        if block != "":
            blocks.append(block)

    return blocks

def block_to_block_type(block: str) -> BlockType:
    
    # Heading
    if block.startswith("#"):
        heading_level = len(block) - len(block.lstrip("#")) # .lstrip() es left strip, quita los caracteres que le pides pero solo al lado izquierdo

        if 1 <= heading_level <= 6:
            remaining_text = block[heading_level:]

            if remaining_text.startswith(" ") and remaining_text.strip():
                return BlockType.HEADING

    # Code
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in block.split("\n")): # all(list[] o cualquier iterable)  devuelve True solo si todos los elementos de la lista (en este caso las líneas empezando por ">") son true
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in block.split("\n")): 
        return BlockType.UNORDERED_LIST

    # Ordered list
    if block.startswith("1. "):
        lines = block.split("\n")
        ordered = True

        for i, line in enumerate(lines, start = 1):
            if not line.startswith(f"{i}. "):
                ordered = False
                break
            
        if ordered:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def main():
    md_ejemplo = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""

    test = markdown_to_blocks(md_ejemplo)
    print(test, type(test))

if __name__ == "__main__":
    main()