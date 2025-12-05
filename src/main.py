from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from copystatic import copy_static
from markdown_blocks import markdown_to_html_node
import os
import sys

def extract_title(markdown):
    cleanup_content = markdown.strip()
    if cleanup_content.startswith("#"):
        raw_header = cleanup_content.split("\n", 1)[0]
        clean_header = raw_header.split(" ", 1)[1]
        return clean_header.strip()
    else:
        raise Exception("no header")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as ff:
        template = ff.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    index = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(index)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"creating directory at {dest_dir_path}")
    elements = os.listdir(dir_path_content)
    for element in elements:
        new_dir_path_content = os.path.join(dir_path_content, element)
        if new_dir_path_content.endswith(".md"):
            new_filename = "index.html"
            generate_page(new_dir_path_content, template_path, os.path.join(dest_dir_path, new_filename), basepath)
        elif os.path.isdir(new_dir_path_content):
            new_dest_dir_path = os.path.join(dest_dir_path, element)
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path, basepath)

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1] 
    target_dir = "/home/migueldor/site/docs"
    origin_dir = "/home/migueldor/site/static/"
    from_path = "/home/migueldor/site/content"
    template_path = "/home/migueldor/site/template.html"
    copy_static(origin_dir, target_dir)
    generate_pages_recursive(from_path, template_path, target_dir, basepath)
    

main()

