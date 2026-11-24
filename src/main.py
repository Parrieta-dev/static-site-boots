from textnode import TextNode
import os
import shutil

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
            if os.path.exists(element_destination_path):
                shutil.rmtree(element_destination_path)
            os.mkdir(element_destination_path)
            folder_copy(element_source_path, element_destination_path)
            

def main():
    test_node = TextNode(text = "Helloooo", text_type="text", url="https://www.boot.dev")
    print(test_node)
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    folder_copy("static", "public")

main()