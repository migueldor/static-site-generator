from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes




def clean_block(block):
    no_jump_block = block.split("\n")
    return " ".join(no_jump_block)

def paragraph_block_to_htmlnode(block):
    cleaned_block = clean_block(block)
    block_textnodes = text_to_textnodes(cleaned_block)
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode("p", block_htmlnodes, None)

def heading_block_to_htmlnode(block):
    cleaned_block = clean_block(block)
    block_list = cleaned_block.split(" ", 1)
    block_textnodes = text_to_textnodes(block_list[1])
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode(f"h{len(block_list[0])}", block_htmlnodes, None)

def code_block_to_htmlnode(block):
    clean = clean_block(block)
    text_block = clean[4:-4]
    block_textnodes = text_to_textnodes(text_block)
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode("code", block_htmlnodes, None)

def quote_block_to_htmlnode(block):
    clean = clean_block(block)
    block_list = clean.split(">")
    block_join = " ".join(block_list)
    block_textnodes = text_to_textnodes(block_join)
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode("blockquote", block_htmlnodes, None)

def ulist_block_to_htmlnode(block):
    clean = clean_block(block)
    block_list = clean.split("- ")
    new_block = []
    for element in block_list:
        if element != "":
            new_block.append(f"<li>{element}</li>")
    block_join = "".join(new_block)
    block_textnodes = text_to_textnodes(block_join)
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode("ul", block_htmlnodes, None)

def olist_block_to_htmlnode(block):
    block_list = block.split("\n")
    no_number_list = []
    for item in block_list:
        no_number_list.append(f"<li>{item[3:]}</li>")
    block_join = "".join(no_number_list)
    block_textnodes = text_to_textnodes(block_join)
    block_htmlnodes = []
    for textnode in block_textnodes:
        block_htmlnodes.append(text_node_to_html_node(textnode))
    return ParentNode("ol", block_htmlnodes, None)



def block_to_htmlnode(block):
    if block_to_block_type(block) == BlockType.PARAGRAPH:
        return paragraph_block_to_htmlnode(block)
    if block_to_block_type(block) == BlockType.HEADING:
        return heading_block_to_htmlnode(block) 
    if block_to_block_type(block) == BlockType.CODE:
        return ParentNode("pre", [code_block_to_htmlnode(block)])
    if block_to_block_type(block) == BlockType.QUOTE:
        return quote_block_to_htmlnode(block)
    if block_to_block_type(block) == BlockType.ULIST:
        return ulist_block_to_htmlnode(block)
    if block_to_block_type(block) == BlockType.OLIST:
        return olist_block_to_htmlnode(block)
    else:
        raise Exception("non-supported type")
    


def markdown_to_html(document):
    blocks = markdown_to_blocks(document)
    nodes = []
    for block in blocks:
        nodes.append(block_to_htmlnode(block))
    return ParentNode("div", nodes, None)
    

