import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "test", props = {
        "href": "https://www.google.com",
        "target": "_blank",
        })
        
        node2 = HTMLNode("p", "test2", props = {
        "href": "https://www.google.com",
        "target": "_blank",
        })

        node3 = HTMLNode("p", "test")
        self.assertEqual(node3.children, None)
        self.assertEqual(node3.props, None)
        self.assertNotEqual(node, node2)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
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

    def test_parent_with_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><b>bold</b><i>italic</i></div>")

if __name__ == "__main__":
    unittest.main()
