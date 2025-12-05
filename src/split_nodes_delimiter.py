from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_delimiters = ["**", "`", "_"]
    if delimiter not in valid_delimiters:
        raise Exception("not a valid delimiter")
    new_node_list = []
    full_text = old_nodes.text
    indexes = []
    for i in range(0, len(full_text)):
        if full_text[i] == delimiter:
            indexes.append(i)
    split_text_list = [full_text[: indexes[0]], full_text[indexes[0]:indexes[1] +1], full_text[indexes[1] +1:]]
    for text in split_text_list:
        if text[0] == delimiter and text[len(text)-1] == delimiter:
            new_node_list.append(TextNode(text, text_type))
        else:
            new_node_list.append(TextNode(text, TextType.TEXT))
    return new_node_list
            


node = TextNode("This is text with a `code block` word", TextType.TEXT)

print(split_nodes_delimiter(node, "@", TextType.CODE))