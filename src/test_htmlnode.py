import unittest

from htmlnode import *
from textnode import TextNode
import unittest

class TestHTMLNode(unittest.TestCase):

    def test_leaf_node_creation(self):
        node = LeafNode(value="test", tag="p", props={"class": "text"})
        self.assertEqual(node.value, "test")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.props, {"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">test</p>')

    def test_leaf_node_no_tag(self):
        node = LeafNode(value="test")
        self.assertEqual(node.to_html(), "test")

    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(value=None)

    def test_parent_node_creation(self):
        child1 = LeafNode(value="child1", tag="p")
        child2 = LeafNode(value="child2", tag="span")
        node = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.to_html(), '<div><p>child1</p><span>child2</span></div>')

    def test_parent_node_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[LeafNode(value="child")])

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=[])

class TestMarkdownFunctions(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](image_url)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "image_url")])

    def test_extract_markdown_links(self):
        text = "This is a [link](url)"
        self.assertEqual(extract_markdown_links(text), [("link", "url")])

    def test_split_nodes_image(self):
        old_nodes = [TextNode(text="This is an image ![alt text](image_url)", text_type="text")]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is an image ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, "image")
        self.assertEqual(new_nodes[1].url, "image_url")

    def test_split_nodes_link(self):
        old_nodes = [TextNode(text="This is a [link](url)", text_type="text")]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, "link")
        self.assertEqual(new_nodes[1].url, "url")

    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode(text="This is **bold** text", text_type="text")]
        new_nodes = split_nodes_delimiter(old_nodes, '**')
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode(text="This is *italic* text", text_type="text")]
        new_nodes = split_nodes_delimiter(old_nodes, '*')
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, "italic")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode(text="This is `code` text", text_type="text")]
        new_nodes = split_nodes_delimiter(old_nodes, '`')
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, "code")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_text_to_textnodes(self):
        text = "This is **bold** and *italic* text with `code` and a [link](url) and an image ![alt text](image_url)"
        nodes = text_to_textnodes(text)
        expected_values = ["This is ", "bold", " and ", "italic", " text with ", "code", " and a ", "link", " and an image ", "alt text"]
        expected_types = ["text", "bold", "text", "italic", "text", "code", "text", "link", "text", "image"]
        self.assertEqual([node.text for node in nodes], expected_values)
        self.assertEqual([node.text_type for node in nodes], expected_types)
    
class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), 'heading')

    def test_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), 'code')

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), 'quote')

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block), 'unordered-list')

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), 'ordered-list')

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), 'paragraph')
    
    class TestMarkdownToHTMLNode(unittest.TestCase):

        def test_quote_to_html_node(self):
            block = "> This is a quote"
            node = quote_to_html_node(block)
            self.assertEqual(node.to_html(), '<blockquote><p>This is a quote</p></blockquote>')

        def test_unordered_list_to_html_node(self):
            block = "* Item 1\n* Item 2"
            node = unordered_list_to_html_node(block)
            self.assertEqual(node.to_html(), '<ul><li><p>Item 1</p></li><li><p>Item 2</p></li></ul>')

        def test_ordered_list_to_html_node(self):
            block = "1. Item 1\n2. Item 2"
            node = ordered_list_to_html_node(block)
            self.assertEqual(node.to_html(), '<ol><li><p>Item 1</p></li><li><p>Item 2</p></li></ol>')

        def test_paragraph_to_html_node(self):
            block = "This is a paragraph."
            node = paragraph_to_html_node(block)
            self.assertEqual(node.to_html(), '<p>This is a paragraph.</p>')

        def test_heading_to_html_node(self):
            block = "# This is a heading"
            node = heading_to_html_node(block)
            self.assertEqual(node.to_html(), '<h1>This is a heading</h1>')

        def test_code_to_html_node(self):
            block = "```\nThis is a code block\n```"
            node = code_to_html_node(block)
            self.assertEqual(node.to_html(), '<pre><code>This is a code block</code></pre>')

        def test_markdown_to_html_node(self):
            markdown = "# Heading\n> Quote\n```\nCode\n```\n* Unordered\n1. Ordered\nParagraph"
            node = markdown_to_html_node(markdown)
            self.assertEqual(node.to_html(), '<div><h1>Heading</h1><blockquote><p>Quote</p></blockquote><pre><code>Code</code></pre><ul><li><p>Unordered</p></li></ul><ol><li><p>Ordered</p></li></ol><p>Paragraph</p></div>')

if __name__ == "__main__":
    unittest.main()
