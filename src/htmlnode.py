

class HTMLNode():
    def __init__(self, tag: str|None, value: str|None, children: list|None, props: dict|None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if not self.props:
            return result
        
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f"HTMLNode(TAG={self.tag}, VALUE={self.value}, CHILDREN={self.children}, PROPS={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props = None):
        super().__init__(tag, value, children = None, props = props)

    def to_html(self):
        html_str = ""
        if self.value is None:
            raise ValueError("All leaf nodes MUST have a value")
        if not self.tag:
            return str(self.value)
        if not self.props:
            html_str = f"<{self.tag}>{self.value}</{self.tag}>"
            return html_str
        html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"LeafNode(TAG={self.tag}, VALUE={self.value}, PROPS={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props = None):
        super().__init__(children=children, props=props, tag=tag, value=None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is mandatory")
        if self.children is None:
            raise ValueError("Where are the pitiful children?")
        html_str = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html_str += child.to_html()

        html_str += f"</{self.tag}>"
        return html_str

# def main():
#     node = LeafNode("a", "Im a link!", {"href": "www.boot.dev"})
#     html_node = node.to_html()
#     print(node)
#     print(html_node)

# main()