import re
from textnode import TextNode

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str = ""
        for k, v in self.props.items():
            str += ' ' + f'{k}="{v}"'
        return str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        if props is None:
            props = {}
        super().__init__(tag=tag, value=value, children=None, props=props)
        if self.value == None:
            raise ValueError('Leaf Nodes require a Value')

    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if props is None:
            props = {}
        super().__init__(tag=tag, value=None, children=children, props=props)
        if self.tag == None:
            raise ValueError('Parent Nodes require a tag')
        if self.children == None or self.children == []:
            raise ValueError('Parent Nodes require at least one child')
        
    def to_html(self):
        string = ""
        for node in self.children:
            string += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{string}</{self.tag}>"
            
def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(value = text_node.text)
    if text_node.text_type == "bold":
        return LeafNode(value = text_node.text, tag = "b")
    if text_node.text_type == "italic":
        return LeafNode(value = text_node.text, tag="i")
    if text_node.text_type == "code":
        return LeafNode(value = text_node.text, tag = "code")
    if text_node.text_type == "link":
        return LeafNode(value = text_node.text, tag = "a", props = {"href" : text_node.url})
    if text_node.text_type == "image":
        return LeafNode(value = "", tag = "img", props={"src": text_node.url, "alt": text_node.text})
    raise Exception("Unsupported text type")

def split_nodes_delimiter(old_nodes, delimiter):
    delimiter_dict = {'**': "bold", '*': "italic", "`": "code"}
    if delimiter not in delimiter_dict:
        raise KeyError('Unsupported Delimiter')
    new_nodes = []
    for node in old_nodes:
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(text=part, text_type=node.text_type))
            else:
                new_nodes.append(TextNode(text=part, text_type=delimiter_dict[delimiter]))
    return [node for node in new_nodes if node.text]

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches 

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    node_lst = []
    for node in old_nodes:
        lst = [node.text]
        image_tups = extract_markdown_images(lst[0])
        if image_tups != []:
            for image_tup in image_tups:
                cur_split = lst[-1].split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                cur_split.insert(1, image_tup)
                lst = lst[:-1]
                lst.extend(cur_split)
        for element in lst:
            if type(element) == str and element != "":
                node_lst.append(TextNode(text = element, text_type = node.text_type))
            elif type(element) == tuple:
                node_lst.append(TextNode(text = element[0], text_type = "image", url = element[1]))
    return node_lst

def split_nodes_link(old_nodes):
    node_lst = []
    for node in old_nodes:
        lst = [node.text]
        link_tups = extract_markdown_links(lst[0])
        if link_tups != []:
            for link_tup in link_tups:
                cur_split = lst[-1].split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                cur_split.insert(1, link_tup)
                lst = lst[:-1]
                lst.extend(cur_split)
        for element in lst:
            if type(element) == str and element != "":
                node_lst.append(TextNode(text = element, text_type = node.text_type))
            elif type(element) == tuple:
                node_lst.append(TextNode(text = element[0], text_type = "link", url = element[1]))
    return node_lst

def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type="text")]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**')
    nodes = split_nodes_delimiter(nodes, '*')
    nodes = split_nodes_delimiter(nodes, '`')
    return nodes

#function takes a raw Markdown string and returns a list of "block" strings
#Split the input string into distinct blocks and strip any leading or trailing whitespace from each block, as well as remove
#any "empty blocks" due to unneccesary newlines
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks

#function takes a single block of markdown text and returns the type of block it is
#headings start with 1-6 '#', a space, then heading text
#code blocks must start and end with 3 ```
#every line in a quote block must start with a > 
#every line in an unordered list must start with either a * or a -, followed by a space
#every line in an ordered list must start with a number, followed by a . and a space. 
#That number must start at one and increment by one each line
#otherwise, its a normal paragraph
def block_to_block_type(block):
    for i in range(7):
        if block[:i] == '#' and block[i] == ' ':
            return 'heading'
    if block[:3] == '```' and block[-3:] == '```':
        return 'code'
    line_split = block.split('\n')
    if all([line[0] == '>' for line in line_split]):
        return 'quote'
    if all(line[:2] == '* ' or line[:2] == '- ' for line in line_split):
        return 'unordered-list'
    if all(line.split('.', 1)[0][0] == str(i) and line.split('.', 1)[1][0] == ' ' for i, line in enumerate(line_split, 1)):
        return 'ordered-list'
    return 'paragraph'
    
#function for converting a blockquote to an htmlnode
def quote_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag='blockquote', children=children)

#function for converting an unordered list to an htmlnode
def unordered_list_to_html_node(block):
    lines = block.split('\n')
    children = []
    for line in lines:
        text_nodes = text_to_textnodes(line[2:])
        children.append(ParentNode(tag='li', children=[text_node_to_html_node(node) for node in text_nodes]))
    return ParentNode(tag='ul', children=children)

#function for converting an ordered list to an htmlnode
def ordered_list_to_html_node(block):
    lines = block.split('\n')
    children = []
    for line in lines:
        text_nodes = text_to_textnodes(line.split('.', 1)[1])
        children.append(ParentNode(tag='li', children=[text_node_to_html_node(node) for node in text_nodes]))
    return ParentNode(tag='ol', children=children)

#function for converting a paragraph to an htmlnode
def paragraph_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag='p', children=children)

#function for converting a heading to an htmlnode
def heading_to_html_node(block):
    level = 0
    for i in range(7):
        if block[i] == '#':
            level += 1
        else:
            break
    text_nodes = text_to_textnodes(block[level+1:])
    children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag=f'h{level}', children=children)

#function for converting a code block to an htmlnode
def code_to_html_node(block):
    return ParentNode(tag = "pre", children=LeafNode(value=block[3:-3], tag='code'))

#overarching master function, takes a full markdown document, creates a "div" with document's blocks as children
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block_to_block_type(block) == 'heading':
            children.append(heading_to_html_node(block))
        if block_to_block_type(block) == 'quote':
            children.append(quote_to_html_node(block))
        if block_to_block_type(block) == 'code':
            children.append(code_to_html_node(block))
        if block_to_block_type(block) == 'ordered-list':
            children.append(ordered_list_to_html_node(block))
        if block_to_block_type(block) == 'unordered-list':
            children.append(unordered_list_to_html_node(block))
        if block_to_block_type(block) == 'paragraph':
            children.append(paragraph_to_html_node(block))
    return ParentNode(tag='div', children=children)


        

        
