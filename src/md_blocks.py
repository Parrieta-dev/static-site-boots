# This needs filling

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []

    cut_text = markdown.split("\n\n")

    for block in cut_text:
        block = block.strip()
        if block != "":
            blocks.append(block)

    return blocks



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