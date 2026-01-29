import unittest
import os
import shutil
from binary_tree_yaml import Node, create_tree, add_node, delete_node, edit_node, build_tree_from_yaml, write_tree_to_yaml

class TestBinaryTree(unittest.TestCase):
    def setUp(self):
        self.root = create_tree(10)
        self.test_yaml = "test_temp.yaml"

    def tearDown(self):
        if os.path.exists(self.test_yaml):
            os.remove(self.test_yaml)

    def test_node_creation(self):
        node = Node(5)
        self.assertEqual(node.value, 5)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_add_node(self):
        add_node(self.root, "L", 5)
        self.assertEqual(self.root.left.value, 5)
        add_node(self.root, "R", 15)
        self.assertEqual(self.root.right.value, 15)
        add_node(self.root, "LL", 2)
        self.assertEqual(self.root.left.left.value, 2)

    def test_path_error(self):
        with self.assertRaises(ValueError):
            add_node(self.root, "LR", 5) # Missing L parent initially

    def test_delete_node(self):
        add_node(self.root, "L", 5)
        delete_node(self.root, "L")
        self.assertIsNone(self.root.left)

    def test_edit_node(self):
        add_node(self.root, "L", 5)
        edit_node(self.root, "L", 8)
        self.assertEqual(self.root.left.value, 8)

    def test_yaml_io(self):
        add_node(self.root, "L", 5)
        add_node(self.root, "R", 15)
        write_tree_to_yaml(self.root, self.test_yaml)
        
        new_root = build_tree_from_yaml(self.test_yaml)
        self.assertEqual(new_root.value, 10)
        self.assertEqual(new_root.left.value, 5)
        self.assertEqual(new_root.right.value, 15)

if __name__ == '__main__':
    unittest.main()
