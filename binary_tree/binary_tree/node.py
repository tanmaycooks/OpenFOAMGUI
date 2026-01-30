from typing import List, Optional, Any

class Node:
    """
    A Node class representing a node in a Binary Tree (extensible to General Tree).
    
    Attributes:
        value (Any): The value stored in the node.
        children (List['Node']): List of child nodes. 
            For Binary Tree: index 0 is Left, index 1 is Right.
            Use None for missing children to maintain index positions if necessary.
    """
    def __init__(self, value: Any, children: Optional[List['Node']] = None):
        self.value = value
        self.children = children if children is not None else []

    @property
    def left(self) -> Optional['Node']:
        """Get the left child (first child)."""
        if len(self.children) > 0:
            return self.children[0]
        return None

    @left.setter
    def left(self, node: Optional['Node']):
        """Set the left child."""
        if not self.children:
            self.children = [node]
        else:
            self.children[0] = node

    @property
    def right(self) -> Optional['Node']:
        """Get the right child (second child)."""
        if len(self.children) > 1:
            return self.children[1]
        return None

    @right.setter
    def right(self, node: Optional['Node']):
        """Set the right child."""
        # Ensure we have a slot for left child even if it's None
        if len(self.children) == 0:
            self.children = [None, node]
        elif len(self.children) == 1:
            self.children.append(node)
        else:
            self.children[1] = node

    def __repr__(self):
        return f"Node({self.value})"
