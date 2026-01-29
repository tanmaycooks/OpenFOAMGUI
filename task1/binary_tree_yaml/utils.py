from .node import Node
from typing import Optional

def create_tree(root_value) -> Node:
    """Create a new tree with a root value."""
    return Node(root_value)

def add_node(root: Node, path: str, value) -> bool:
    """
    Add a node at the specified path.
    Path matches regex [LR]*. 
    Example: 'LL' means add as left child of left child.
    Creates intermediate nodes if they don't exist? 
    Strict interpretation: 'add node' usually implies the parent must exist.
    However, to be helpful, we will create intermediate nodes with None value or error?
    Let's assume parents must exist to contain values. If not, raises ValueError.
    """
    current = root
    # Traverse to parent
    for i, char in enumerate(path[:-1]):
        if char.upper() == 'L':
            if not current.left:
                # Create intermediate placeholder if missing? Or error?
                # Error is safer for data integrity unless specified.
                raise ValueError(f"Path {path} invalid: Missing parent at step {i} (L)")
            current = current.left
        elif char.upper() == 'R':
            if not current.right:
                 raise ValueError(f"Path {path} invalid: Missing parent at step {i} (R)")
            current = current.right
        else:
            raise ValueError("Path must contain only 'L' or 'R'")
    
    # Add the final node
    direction = path[-1].upper()
    new_node = Node(value)
    if direction == 'L':
        current.left = new_node
    elif direction == 'R':
        current.right = new_node
    else:
        raise ValueError("Path must contain only 'L' or 'R'")
    return True

def delete_node(root: Node, path: str) -> bool:
    """
    Delete the node at specific path (and its subtree).
    """
    if not path:
        # Deleting root? Not possible via this helper without returning new root.
        # We will clear root's children/value or raise error.
        raise ValueError("Cannot delete root using path ''.")

    current = root
    parent = None
    direction = None

    for char in path:
        parent = current
        if char.upper() == 'L':
            current = current.left
            direction = 'left'
        elif char.upper() == 'R':
            current = current.right
            direction = 'right'
        else:
            raise ValueError("Path must contain only 'L' or 'R'")
        
        if not current:
            return False # Node not found

    # Delete
    if direction == 'left':
        parent.left = None
    elif direction == 'right':
        parent.right = None
    
    return True

def edit_node(root: Node, path: str, new_value) -> bool:
    """Edit value of node at path."""
    if not path:
        root.value = new_value
        return True

    current = root
    for char in path:
        if char.upper() == 'L':
            current = current.left
        elif char.upper() == 'R':
            current = current.right
        else:
            raise ValueError("Path must contain only 'L' or 'R'")
        
        if not current:
            return False

    current.value = new_value
    return True

def print_tree(node: Node, level: int = 0, prefix: str = "Root: "):
    """
    Print tree structure. match sample format.
    Format assumption:
    Root: value
      L: value
      R: value
        L: ...
    """
    if not node:
        return
    
    print(f"{'  ' * level}{prefix}{node.value}")
    
    # Handle children generally
    if node.left:
        print_tree(node.left, level + 1, "L: ")
    if node.right:
        print_tree(node.right, level + 1, "R: ")
    
    # For general tree bonus (indices > 1)
    if len(node.children) > 2:
        for i in range(2, len(node.children)):
            child = node.children[i]
            if child:
                print_tree(child, level + 1, f"C{i}: ")

def print_range(node: Node, min_val, max_val):
    """Print values in range [min_val, max_val] (inclusive)."""
    if not node:
        return
    
    # In-order traversal usually gives sorted output if BST, but this is generic BT.
    # Just traverse and check.
    if node.left:
        print_range(node.left, min_val, max_val)
    
    if min_val <= node.value <= max_val:
        print(node.value)
        
    if node.right:
         print_range(node.right, min_val, max_val)
