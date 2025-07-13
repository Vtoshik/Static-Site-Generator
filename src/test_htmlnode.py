import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.children, None)

    def test_props(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.google.com", "target": "_blank"})
        string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), string)

    def test_props_empty(self):
        node = HTMLNode(tag="p", value="Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        string = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), string)

    def testPleaf_to_html_h1(self):
        node = LeafNode("h1", "Front-end Development is the Worst")
        self.assertEqual(node.to_html(), "<h1>Front-end Development is the Worst</h1>")

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
        


if __name__ == "__main__":
    unittest.main()