
from textnode import TextNode, TextType, text_node_to_html_node
from itertools import zip_longest
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text == " ":
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if not delimiter in node.text:
            new_nodes.append(node)
            continue
        if node.text[0] == " ":
            splitted_node = node.text.split()
            splitted_node[0] = " " + splitted_node[0]
        else:
            splitted_node = node.text.split()
        delimiter_occurences = []
        single_delimiter_occurence = False

        for i in range(len(splitted_node)):
            if delimiter in splitted_node[i] and len(delimiter_occurences) > 0:
                delimiter_count_in_word = splitted_node[i].count(delimiter)
                delimiter_occurences.append(i)

                if delimiter_count_in_word == 2:
                    new_nodes.append(TextNode(" " + " ".join(splitted_node[delimiter_occurences[-2]+1:i]) + " ", TextType.TEXT))
                    new_nodes.append(TextNode(splitted_node[i].replace(delimiter, ""), text_type))
                
                elif delimiter_count_in_word == 1 and single_delimiter_occurence == False:
                    new_nodes.append(TextNode(" " + " ".join(splitted_node[delimiter_occurences[-2]+1:i]) + " ", TextType.TEXT))
                    single_delimiter_occurence = True
                
                elif delimiter_count_in_word == 1 and single_delimiter_occurence == True:
                    new_nodes.append(TextNode(" ".join(splitted_node[delimiter_occurences[-2]:i+1]).replace(delimiter, ""), text_type))
                    single_delimiter_occurence = False

            elif delimiter in splitted_node[i] and len(delimiter_occurences) == 0:
                delimiter_count_in_word = splitted_node[i].count(delimiter)
                delimiter_occurences.append(i)

                if delimiter_count_in_word == 2:
                    if i != 0:
                        new_nodes.append(TextNode(" ".join(splitted_node[0:i]) + " ", TextType.TEXT))
                        new_nodes.append(TextNode(splitted_node[i].replace(delimiter, ""), text_type))
                    else:
                        new_nodes.append(TextNode(splitted_node[i].replace(delimiter, ""), text_type))

                
                elif delimiter_count_in_word == 1 and single_delimiter_occurence == False:
                    new_nodes.append(TextNode(" ".join(splitted_node[0:i]) + " ", TextType.TEXT))
                    single_delimiter_occurence = True

            elif (i == len(splitted_node) - 1) and (delimiter not in splitted_node[i]):
                    if delimiter_occurences:
                        new_nodes.append(TextNode(" " + " ".join(splitted_node[delimiter_occurences[-1]+1:]), TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

                
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes 


                










