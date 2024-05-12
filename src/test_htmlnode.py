import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"key1": "value1", "key2": "value2"})
        self.assertEqual(node1.props_to_html(), ' key1="value1" key2="value2"')

    def test_to_html_leaf(self):
        node1 = LeafNode(tag = "t", value = "value", props = {"key1": "value1", "key2": "value2"})
        self.assertEqual(node1.to_html(), '<t key1="value1" key2="value2">value</t>')

    def test_to_html_parent(self):
        node1 = ParentNode(tag = "a", children = [ParentNode(tag="b", children = [LeafNode(tag = "c", value = "value1")]), LeafNode(tag = "d", value="value2")], props = {"key3": "value3", "key4":"value4"})
        self.assertEqual(node1.to_html(), '<a key3="value3" key4="value4"><b><c>value1</c></b><d>value2</d></a>')


if __name__ == "__main__":
    unittest.main()