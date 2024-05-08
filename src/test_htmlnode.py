import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"key1": "value1", "key2": "value2"})
        self.assertEqual(node1.props_to_html(), ' key1="value1" key2="value2"')

if __name__ == "__main__":
    unittest.main()