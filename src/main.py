from textnode import TextNode
import os
import shutil
import sys
from markdown_to_html import markdown_to_html_node

def folder_copy(source, destination):
    contents = os.listdir(source)
    for element in contents:
        element_source_path = os.path.join(source, element)
        element_destination_path = os.path.join(destination, element)
        if os.path.isfile(element_source_path):
            print(f"File: {element}")
            shutil.copy(element_source_path, element_destination_path)
        else:
            print(f"Folder: {element_source_path}")
            os.mkdir(element_destination_path)
            folder_copy(element_source_path, element_destination_path)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")

def generate_page(source_path, template_path, public_path, basepath):
    print(f"Generating an amazing page from {source_path} to {public_path} using {template_path}")

    with open(source_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()
        # print(markdown_text)
    
    with open(template_path, "r", encoding="utf-8") as template:
        template_text = template.read()

    title =  extract_title(markdown_text)
    content = markdown_to_html_node(markdown_text).to_html()
    html_result = template_text.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html_result = html_result.replace('href="/', f'href="{basepath}')
    html_result = html_result.replace('src="/', f'src="{basepath}')

    with open(public_path, "w", encoding="utf-8") as file:
        file.write(html_result)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath:str):
    contents = os.listdir(dir_path_content)

    for element in contents:
        source_path = os.path.join(dir_path_content, element)
        destination_path = os.path.join(dest_dir_path, element)
        if os.path.isfile(source_path):
            generate_page(source_path, template_path, destination_path.replace("md", "html"), basepath)
        else:
            os.mkdir(destination_path)
            generate_pages_recursive(source_path, template_path, destination_path, basepath)

        # Aquí decidiremos si es archivo o carpeta

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    folder_copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()