import unittest

from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"key1": "value1", "key2": "value2"})
        self.assertEqual(node1.props_to_html(), ' key1="value1" key2="value2"')

    def test_to_html_leaf(self):
        node1 = LeafNode(tag = "t", value = "value", props = {"key1": "value1", "key2": "value2"})
        self.assertEqual(node1.to_html(), '<t key1="value1" key2="value2">value</t>')



if __name__ == "__main__":
    unittest.main()