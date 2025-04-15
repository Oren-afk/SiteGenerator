import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node =HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')

    def test_multiple_props(self):
        node = HTMLNode("a", "link", None, {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.props_to_html()
        self.assertTrue(' href="https://www.google.com"' in result)
        self.assertTrue(' target="_blank"' in result)

    def test_no_props(self):
        node = HTMLNode("p", "text", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr(self):
        node = HTMLNode("div", "content", None, {"class": "container"})
        repr_result = repr(node)
        self.assertTrue("div" in repr_result)
        self.assertTrue("content" in repr_result)
        self.assertTrue("container" in repr_result)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a children value")

    def test_parent_node_with_none_child(self):
        child_nodes = [LeafNode("span", "child"), None]  # One valid child, one `None`
        node = ParentNode("div", child_nodes)
        with self.assertRaises(AttributeError):
            node.to_html()

    def test_parent_node_with_multiple_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, "Normal"),
                LeafNode("i", "Italic"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><b>Bold</b>Normal<i>Italic</i></div>"
        )


if __name__ == "__main__":
    unittest.main()