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
        return LeafNode(value = text_node.text, tag = "a", prop = {"href" : text_node.url})
    if text_node.text_type == "image":
        return LeafNode(value = "", tag = "img", props={"src": text_node.url, "alt": text_node.text})
    raise Exception("Unsupported text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiter_dict = {'**': "bold", '*': "italic", "`": "code"}
    if delimiter not in delimiter_dict:
        raise KeyError('Unsupported Delimiter')
    str_lst = []
    for node in old_nodes:
        str_lst.extend(node.value.split(delimiter))
    if len(str_lst) % 2 == 0:
        raise Exception("Invalid markdown syntax - missing closing delimiter")
    node_lst = []
    for i in range(len(str_lst)):
        if i % 2 == 0:
            node_lst.append(TextNode(value = str_lst[i], text_type = text_type))
        else:
            node_lst.append(TextNode(value = str_lst[i], text_type = delimiter_dict[delimiter]))
    return node_lst