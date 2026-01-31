import sys
import os

# Ensure we can import the package locally if not installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from binary_tree import build_tree_from_yaml, print_tree, print_range, add_node, delete_node, write_tree_to_yaml

def main():
    yaml_file = "test.yaml"
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found.")
        return

    print("--- Building Tree from YAML ---")
    root = build_tree_from_yaml(yaml_file)
    print_tree(root)

    print("\n--- Printing Range [5, 15] ---")
    print_range(root, 5, 15)

    print("\n--- Adding Node at 'LLR' (Value 3) ---")
    # Note: test.yaml has LL (val 2). LLR means child of 2.
    try:
        add_node(root, "LLR", 3)
        print_tree(root)
    except Exception as e:
        print(f"Failed to add node: {e}")

    print("\n--- Writing Tree to output.yaml ---")
    write_tree_to_yaml(root, "output.yaml")
    print("Done.")

if __name__ == "__main__":
    main()
