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
            
            