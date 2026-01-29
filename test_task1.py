
from binary_tree_yaml import create_tree, add_node, print_tree, write_tree_to_yaml

print("--- Test Task 1 ---")

# 1. Create Tree
print("Creating tree with root 10...")
root = create_tree(10)

# 2. Add Nodes
print("Adding nodes...")
add_node(root, "L", 5)
add_node(root, "R", 15)
add_node(root, "LL", 2)
add_node(root, "LR", 7)

# 3. Print Tree
print("Current Tree Structure:")
print_tree(root)

# 4. Write to YAML
output_file = "test_task1_output.yaml"
print(f"Writing to {output_file}...")
write_tree_to_yaml(root, output_file)

print("Done.")
