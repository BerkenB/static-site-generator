class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_str = ""

        for key in self.props:
            html_str += f' {key}="{self.props[key]}"'

        return html_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leave nodes must have a value")
        if self.tag == None:
            return self.value
        
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        child_html = ""
        for child in self.children:
            child_html +=  child.to_html()
        
        return f"<{self.tag}>" + child_html + f"</{self.tag}>"

       

        
        


        

    
        
        
        

    
        


        