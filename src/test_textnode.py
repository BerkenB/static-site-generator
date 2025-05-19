import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.LINK, "test")
        node4 = TextNode("This is a text node", TextType.LINK, "sike")
        node5= TextNode("This is a text node", TextType.BOLD, "notNone")
        node6 = TextNode("This is a text node", TextType.LINK, "test")
        self.assertNotEqual(node3, node4)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node5)
        self.assertEqual(node3, node6)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
