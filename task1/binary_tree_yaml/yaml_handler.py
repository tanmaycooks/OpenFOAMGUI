import yaml
from .node import Node
from .utils import create_tree

def node_to_dict(node: Node) -> dict:
    """Convert Node to dictionary for YAML."""
    if not node:
        return None
    
    data = {"value": node.value}
    
    # Check if has children
    if node.left:
        data["left"] = node_to_dict(node.left)
    if node.right:
        data["right"] = node_to_dict(node.right)
        
    # Bonus: general children
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
    """Convert dictionary to Node."""
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
            if len(node.children) < 2:
                # Pad with None if needed? 
                # If we have extra children, we assume left/right might be filled or None.
                # Just append.
                while len(node.children) < 2:
                    node.children.append(None)
            node.children.append(dict_to_node(child_data))
            
    return node

def build_tree_from_yaml(file_path: str) -> Node:
    """Parse YAML file to Tree."""
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Expect root key? Or direct object? 
    # Usually defaults to direct object if root starts data, 
    # or "root: ..." key. 
    # Let's support "root" key or top-level.
    if "root" in data:
        return dict_to_node(data["root"])
    return dict_to_node(data)

def write_tree_to_yaml(root: Node, file_path: str):
    """Write Tree to YAML file."""
    data = {"root": node_to_dict(root)}
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
