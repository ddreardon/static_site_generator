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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiter_dict = {'**': "bold", '*': "italic", "`": "code"}
    if delimiter not in delimiter_dict:
        raise KeyError('Unsupported Delimiter')
    new_nodes = []
    for node in old_nodes:
        parts = node.value.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(value=part, text_type="text"))
            else:
                new_nodes.append(TextNode(value=part, text_type=delimiter_dict[delimiter]))
    return [node for node in new_nodes if node.value]

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches 

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    node_lst = []
    for node in old_nodes:
        lst = [node.value]
        image_tups = extract_markdown_images(lst)
        if image_tups != []:
            for image_tup in image_tups:
                cur_split = lst[-1].split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                cur_split.insert(1, image_tup)
                lst = lst[:-1]
                lst.extend(cur_split)
        for element in lst:
            if type(element) == str and element != "":
                node_lst.append(TextNode(value = element, text_type = "text"))
            elif type(element) == tuple:
                node_lst.append(TextNode(value = element[0], text_type = "image", url = element[1]))
    return node_lst

def split_nodes_link(old_nodes):
    node_lst = []
    for node in old_nodes:
        lst = [node.value]
        link_tups = extract_markdown_links(lst)
        if link_tups != []:
            for link_tup in link_tups:
                cur_split = lst[-1].split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                cur_split.insert(1, link_tup)
                lst = lst[:-1]
                lst.extend(cur_split)
        for element in lst:
            if type(element) == str and element != "":
                node_lst.append(TextNode(value = element, text_type = "text"))
            elif type(element) == tuple:
                node_lst.append(TextNode(value = element[0], text_type = "link", url = element[1]))
    return node_lst

def text_to_textnodes(text):
    nodes = TextNode(value=text, text_type=text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, '**', "bold")
    nodes = split_nodes_delimiter(nodes, '*', "italic")
    nodes = split_nodes_delimiter(nodes, '`', "code")
    
            

        

        
