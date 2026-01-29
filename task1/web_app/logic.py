
import yaml
from typing import List, Optional, Any

# --- Node Class ---
class Node:
    """
    A Node class representing a node in a Binary Tree.
    """
    def __init__(self, value: Any, children: Optional[List['Node']] = None):
        self.value = value
        self.children = children if children is not None else []

    @property
    def left(self) -> Optional['Node']:
        if len(self.children) > 0:
            return self.children[0]
        return None

    @left.setter
    def left(self, node: Optional['Node']):
        if not self.children:
            self.children = [node]
        else:
            self.children[0] = node

    @property
    def right(self) -> Optional['Node']:
        if len(self.children) > 1:
            return self.children[1]
        return None

    @right.setter
    def right(self, node: Optional['Node']):
        if len(self.children) == 0:
            self.children = [None, node]
        elif len(self.children) == 1:
            self.children.append(node)
        else:
            self.children[1] = node

    def __repr__(self):
        return f"Node({self.value})"

# --- Utils ---
def create_tree(root_value) -> Node:
    return Node(root_value)

def node_to_dict(node: Node) -> dict:
    if not node:
        return None
    
    data = {"value": node.value}
    
    if node.left:
        data["left"] = node_to_dict(node.left)
    if node.right:
        data["right"] = node_to_dict(node.right)
        
    if len(node.children) > 2:
        other_children = []
        for i in range(2, len(node.children)):
            child = node.children[i]
            if child:
                other_children.append(node_to_dict(child))
        if other_children:
            data["children_extra"] = other_children
    return data

def dict_to_node(data: dict) -> Node:
    if not data:
        return None
    
    value = data.get("value")
    node = Node(value)
    
    if "left" in data:
        node.left = dict_to_node(data["left"])
    
    if "right" in data:
        node.right = dict_to_node(data["right"])
        
    if "children_extra" in data:
        for child_data in data["children_extra"]:
            while len(node.children) < 2:
                node.children.append(None)
            node.children.append(dict_to_node(child_data))
            
    return node

def build_tree_from_yaml(file_path: str) -> Node:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    if "root" in data:
        return dict_to_node(data["root"])
    return dict_to_node(data)

def tree_to_yaml_string(root: Node) -> str:
    """Convert Tree to YAML string."""
    data = {"root": node_to_dict(root)}
    return yaml.dump(data, default_flow_style=False, sort_keys=False)
