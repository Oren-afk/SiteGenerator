import unittest

from textnode import TextNode, TextType
from markdown_blocks import BlockType, block_to_block_type, markdown_to_html_node, extract_title

class TestUtility(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Edge cases
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nmulti\nline\ncode\n```"), BlockType.CODE)
        # Edge cases
        self.assertEqual(block_to_block_type("```\nunclosed code block"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("code with ``` in the middle"), BlockType.PARAGRAPH)
    
    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">line 1\n>line 2"), BlockType.QUOTE)
        # Edge case
        self.assertEqual(block_to_block_type(">line 1\nline 2"), BlockType.PARAGRAPH)

    def test_unordered_list_blocks(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.ULIST)
        # Edge case
        self.assertEqual(block_to_block_type("- item 1\ntext"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)
    
    def test_ordered_list_blocks(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.OLIST)
        # Edge cases
        self.assertEqual(block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\ntext"), BlockType.PARAGRAPH)
    
    def test_paragraph_blocks(self):
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Multi-line\nparagraph text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
            # Heading 1

            ## Heading 2

            ### Heading 3
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_quote_blocks(self):
        md = """
            > This is a quote
            > with multiple lines
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
            - Item 1
            - Item 2
            - Item 3
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
            1. First item
            2. Second item
            3. Third item
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_mixed_content(self):
        md = """
            # Main Heading

            This is a paragraph with **bold** and _italic_ text.

            > Here's a quote with `code` inside

            - List item 1
            - List item 2
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><blockquote>Here's a quote with <code>code</code> inside</blockquote><ul><li>List item 1</li><li>List item 2</li></ul></div>"
        )

    def test_empty_document(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_title_extraction(self):
        md = "# Hello"
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, "Hello")

if __name__ == "__main__":
    unittest.main()