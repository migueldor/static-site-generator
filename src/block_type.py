from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = 'ordered list'


def block_to_block_type(block):
    if check_if_heading(block):
        return BlockType.HEADING
    if check_if_code(block):
        return BlockType.CODE
    if check_if_quote(block):
        return BlockType.QUOTE
    if check_if_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if check_if_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def check_if_heading(block):
    splitted = block.split(" ")
    if len(splitted[0]) == 0:
        return False
    if splitted[0][0] == "#" and splitted[0][len(splitted[0])-1] == "#" and len(splitted[0]) < 7:
        return True
    return False

def check_if_code(block):
    if block[:3] == "```" and block[-3:]== "```":
        return True
    return False

def check_if_quote(block):
    split_block = block.split("\n")
    counter = 0
    for element in split_block:
        if element[0] == ">":
            counter += 1
    if counter == len(split_block):
        return True
    return False

def check_if_unordered_list(block):
    split_block = block.split("\n")
    counter = 0
    for element in split_block:
        if element[:2] == "- ":
            counter += 1
    if counter == len(split_block):
        return True
    return False

def check_if_ordered_list(block):
    split_block = block.split("\n")
    counter = 1
    for element in split_block:
        if element[:3] == f"{counter}. ":
            counter += 1
    if counter == len(split_block)+1:
        return True
    return False

''''
block1 = "###### somethig"
block2 = "```somethig```"
block3 = "# somethig"
block4 = "####### somethig"
block5 = ">somenthing\n>something something\n>also something"
block6 = "- somenthing\n- something something\n- also something"
block7 = "1. somenthing\n2. something something\n3. also something"

print(block_to_block_type(block1))
print(block_to_block_type(block2))
print(block_to_block_type(block3))
print(block_to_block_type(block4))
print(block_to_block_type(block5))
print(block_to_block_type(block6))
print(block_to_block_type(block7))
'''