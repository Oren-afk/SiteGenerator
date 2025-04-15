import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("Some bold text", TextType.BOLD)
        node2 = TextNode("Some italic text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("Same text", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("Same text", TextType.ITALIC, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        node1 = TextNode("Some bold text", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("Some bold text", TextType.BOLD, "https://www.youtube.com/")
        self.assertNotEqual(node1, node2)

    def test_none_url(self):
        node1 = TextNode("Some bold text", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("Some bold text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == None
        assert html_node.value == "This is a text node"

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, url="http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props.get("href"), "http://example.com")

    def test_image(self):
        node = TextNode("Picture", TextType.IMAGE, url="http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props.get("src"), "http://example.com")
        self.assertEqual(html_node.props.get("alt"), "Picture")

    def test_invalid_type(self):
        node = TextNode("Invalid text", "NOT_A_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_link_no_url(self):
        node = TextNode("Click me", TextType.LINK, url=None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_no_url(self):
        node = TextNode("Picture", TextType.IMAGE, url=None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()