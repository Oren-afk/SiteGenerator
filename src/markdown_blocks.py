from enum import Enum
import os
import shutil
from utility import markdown_to_blocks, split_nodes_delimiter, text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        split_block = block.split("\n")
        for line in split_block:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        split_block = block.split("\n")
        for line in split_block:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        split_block = block.split("\n")
        counter = 1
        for line in split_block:
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
            counter += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [], None)
    if not blocks:
        return parent_node
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                normalized_paragraph = block.replace("\n", " ").strip()
                children = text_to_children(normalized_paragraph)
                p_node = ParentNode("p", children, None)
                parent_node.children.append(p_node)
            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == '#':
                        level += 1
                    else:
                        break
                heading_text = block[level+1:] if level < len(block) else ""
                children = text_to_children(heading_text)
                if 1 <= level <= 6:
                    h_node = ParentNode(f"h{level}", children, None)
                    parent_node.children.append(h_node)
            case BlockType.CODE:
                lines = block.split("\n")
                if len(lines) >= 3:
                    code_content = "\n".join(lines[1:-1]) + "\n"
                else:
                    code_content = ""
                text_node = TextNode(code_content, TextType.CODE)
                code_node = text_node_to_html_node(text_node)
                pre_node = ParentNode("pre", [code_node], None)
                parent_node.children.append(pre_node)
            case BlockType.QUOTE:
                lines = block.split("\n")
                processed_lines = []
                for line in lines:
                    if line.startswith("> "):
                        processed_lines.append(line[2:])
                    else:
                        processed_lines.append(line)
                quote_text = " ".join(processed_lines)
                children = text_to_children(quote_text)
                blockquote_node = ParentNode("blockquote", children, None)
                parent_node.children.append(blockquote_node)
            case BlockType.ULIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    if len(line) <= 2:
                        continue
                    processed_line = text_to_children(line[2:].strip())
                    li_node = ParentNode("li", processed_line, None)
                    children.append(li_node)
                ul_node = ParentNode("ul", children, None)
                parent_node.children.append(ul_node)
            case BlockType.OLIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    if len(line) <= 3:
                        continue
                    processed_line = text_to_children(line[3:].strip())
                    li_node = ParentNode("li", processed_line, None)
                    children.append(li_node)
                ol_node = ParentNode("ol", children, None)
                parent_node.children.append(ol_node)
    return parent_node

def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("The header must start with a single #")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    revised_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(revised_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            rel_path = os.path.relpath(item_path, dir_path_content)
            dest_file_path = os.path.join(dest_dir_path, rel_path.replace(".md", ".html"))
            generate_page(item_path, template_path, dest_file_path)
        elif os.path.isdir(item_path):
            sub_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, sub_dest_dir_path)