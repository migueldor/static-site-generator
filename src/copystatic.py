import os
import shutil
from markdown_blocks import markdown_to_html_node

def copy_static(origin, target, is_first_call=True):
    if os.path.exists(target) and is_first_call:
        shutil.rmtree(target)
        print(f"f{target} purged")
    if not os.path.exists(target):
        os.mkdir(target)
        print(f"making {target} fresh as new")
    elements = os.listdir(origin)
    for element in elements:
        new_origin = os.path.join(origin, element)
        if os.path.isfile(new_origin):
            shutil.copy(new_origin, target)
            print(f"copying {element} to {target}")
        elif os.path.isdir(new_origin):
            new_target = os.path.join(target, element)
            copy_static(new_origin, new_target, False)


def extract_title(markdown):
    cleanup_content = markdown.strip()
    if cleanup_content.startswith("#"):
        raw_header = cleanup_content.split("\n", 1)[0]
        clean_header = raw_header.split(" ", 1)[1]
        return clean_header.strip()
    else:
        raise Exception("no header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as ff:
        template = ff.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    index = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(index)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"creating directory at {dest_dir_path}")
    elements = os.listdir(dir_path_content)
    for element in elements:
        new_dir_path_content = os.path.join(dir_path_content, element)
        if new_dir_path_content.endswith(".md"):
            new_filename = f"{element}"[0,-3] + ".html"
            generate_page(new_dir_path_content, template_path, os.path.join(dest_dir_path, new_filename))
        elif os.path.isdir(new_dir_path_content):
            new_dest_dir_path = os.path.join(dest_dir_path, element)
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)