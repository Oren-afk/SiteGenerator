import unittest

from textnode import TextNode, TextType
from utility import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from utility import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestUtility(unittest.TestCase):
    def test_bold_delimiter(self):
        old_nodes = [
            TextNode("This a **bold** test", TextType.TEXT), 
            TextNode("This is **another bold** test", TextType.TEXT)
            ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 6)

    def test_itealic_delimiter(self):
        old_nodes = [
            TextNode("This an _italic_ test", TextType.TEXT),
            TextNode("This is _another italic_ test", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 6)

    def test_non_text_nodes_preserved(self):
        old_nodes = [
            TextNode("This is **bold**", TextType.BOLD),
            TextNode("Regular text", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)



    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_images(self):
        matches = extract_markdown_images("This text has no images, just a [link](https://link.com)")
        self.assertEqual([], matches)

    def test_images_with_special_characters(self):
        matches = extract_markdown_images(
            "Image with ![special chars!@#](https://special.jpg) and ![numbers 123](https://numbers.png)"
        )
        self.assertEqual([("special chars!@#", "https://special.jpg"), ("numbers 123", "https://numbers.png")], matches)

    def test_image_urls_with_query_parameters(self):
        matches = extract_markdown_images(
            "Image with ![complex url](https://example.com/image.jpg?size=large&format=png)"
        )
        self.assertEqual([("complex url", "https://example.com/image.jpg?size=large&format=png")], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images("Image with ![](https://empty-alt.jpg)")
        self.assertEqual([("", "https://empty-alt.jpg")], matches)

    def test_mixed_content(self):
        matches = extract_markdown_images(
            "Text with a [link](https://link.com) and an ![image](https://image.jpg) mixed together"
        )
        self.assertEqual([("image", "https://image.jpg")], matches)



    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "Here are [two](https://example.com) separate [links](https://example.org) in text"
        )
        self.assertEqual([("two", "https://example.com"), ("links", "https://example.org")], matches)

    def test_links_with_special_characters(self):
        matches = extract_markdown_links(
            "Links with [special chars!@#](https://special.com) and [numbers 123](https://numbers.com)"
        )
        self.assertEqual([("special chars!@#", "https://special.com"), ("numbers 123", "https://numbers.com")], matches)

    def test_no_links(self):
        matches = extract_markdown_links("This text contains no markdown links")
        self.assertEqual([], matches)

    def test_links_with_images(self):
        matches = extract_markdown_links(
            "Text with a ![image](https://img.com) and a [link](https://link.com)"
        )
        self.assertEqual([("link", "https://link.com")], matches)



    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )



    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split_text = text_to_textnodes(text)
        desired_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(split_text, desired_result)

    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()