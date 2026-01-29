
import sys
import os

# Ensure we can import the package locally
sys.path.insert(0, os.path.abspath(os.getcwd()))

try:
    import binary_tree_yaml
    print("Package imported successfully.")
except ImportError:
    print("Failed to import package.")
    sys.exit(1)

from binary_tree_yaml import (
    Node, create_tree, add_node, delete_node, edit_node, 
    print_tree, print_range, build_tree_from_yaml, write_tree_to_yaml
)

def test_feature_set_1():
    print("\n--- Testing Feature Set 1 ---")
    
    # 1. Create a new binary tree
    print("1. Creating Tree (Root=10)")
    root = create_tree(10)
    print_tree(root)
    
    # 2. Add a node
    print("\n2. Adding nodes (L=5, R=15, LL=2)")
    add_node(root, "L", 5)
    add_node(root, "R", 15)
    add_node(root, "LL", 2)
    print_tree(root)
    
    # 3. Edit the value
    print("\n3. Editing node 'L' value to 8")
    edit_node(root, "L", 8)
    print_tree(root)
    
    # 4. Print range
    print("\n4. Printing Range [8, 15]")
    print_range(root, 8, 15)
    
    # 5. Delete a node
    print("\n5. Deleting node 'LL' (value 2)")
    delete_node(root, "LL")
    print_tree(root)

def test_feature_set_2():
    print("\n--- Testing Feature Set 2 ---")
    
    yaml_file = "features_test.yaml"
    yaml_out = "features_out.yaml"
    
    # Create a dummy YAML
    with open(yaml_file, "w") as f:
        f.write("root:\n  value: 100\n  left:\n    value: 50\n  right:\n    value: 150\n")
    
    # 1. Parse YAML
    print("1. Building Tree from YAML")
    root = build_tree_from_yaml(yaml_file)
    print_tree(root)
    
    # 2. Write to YAML
    print("\n2. Writing Tree to YAML")
    write_tree_to_yaml(root, yaml_out)
    
    # Check if file exists
    if os.path.exists(yaml_out):
        print(f"Success: {yaml_out} created.")
        with open(yaml_out, 'r') as f:
            print("Content:")
            print(f.read())
    else:
        print("Error: Output YAML not found.")

    # Cleanup
    if os.path.exists(yaml_file): os.remove(yaml_file)
    if os.path.exists(yaml_out): os.remove(yaml_out)

if __name__ == "__main__":
    test_feature_set_1()
    test_feature_set_2()
