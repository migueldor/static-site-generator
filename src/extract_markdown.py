import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches





def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extrated_text = extract_markdown_links(original_text)
        if len(extrated_text) == 0:
            new_nodes.append(node)
            
        elif node.text_type == "link":
            new_nodes.append(node)
        else:
            extracted = extract_markdown_links(original_text)
            element = extracted[0]
            reformated = f"[{element[0]}]({element[1]})"
            sections = original_text.split(reformated, 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(element[0], TextType.LINK, element[1]))
            if len(sections[1]) > 0:
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    if new_nodes == old_nodes:
        return new_nodes
    return split_nodes_link(new_nodes)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extrated_text = extract_markdown_images(original_text)
        if len(extrated_text) == 0:
            new_nodes.append(node)
            
        elif node.text_type == "image":
            new_nodes.append(node)
        else:
            extracted = extract_markdown_images(original_text)
            element = extracted[0]
            reformated = f"![{element[0]}]({element[1]})"
            sections = original_text.split(reformated, 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(element[0], TextType.LINK, element[1]))
            if len(sections[1]) > 0:
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    if new_nodes == old_nodes:
        return new_nodes
    return split_nodes_image(new_nodes)
    

