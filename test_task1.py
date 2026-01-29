
from binary_tree_yaml import create_tree, add_node, print_tree, write_tree_to_yaml
import time

print("--- Test Task 1: Complex Tree Generation ---")

# 1. Create Root
print("Creating complex tree...")
root = create_tree("Boss")

# Level 1: Departments
add_node(root, "L", "Engineering")
add_node(root, "R", "Sales")

# Level 2: Teams
add_node(root, "LL", "Backend")
add_node(root, "LR", "Frontend")
add_node(root, "RL", "Domestic")
add_node(root, "RR", "International")

# Level 3: Leads/Members
add_node(root, "LLL", "Dev_Lead")
add_node(root, "LLR", "Dev_Intern")

add_node(root, "LRL", "Design_Lead")
add_node(root, "LRR", "UI_Dev")

add_node(root, "RLL", "Sales_Manager_A")
add_node(root, "RLR", "Sales_Rep_1")

add_node(root, "RRL", "Global_Head")
add_node(root, "RRR", "Regional_VP")

# Level 4: Specific projects (Deep Logic)
add_node(root, "LLLL", "Database_Opt")
add_node(root, "LLLR", "API_V2")
add_node(root, "RRRL", "Europe_Market")
add_node(root, "RRRR", "Asia_Market")

# 3. Print Tree
print("\nGenerated Large Tree Structure:")
print_tree(root)

# 4. Write to YAML
output_file = "test_task1_large.yaml"
print(f"\nWriting to {output_file}...")
write_tree_to_yaml(root, output_file)

print(f"\n[Done] Tree saved to {output_file}")

# --- Visualization Integration ---
import webbrowser
import os
import urllib.parse

# Construct Absolute Path for the App to load
# Current working directory + filename
abs_path = os.path.abspath(output_file)
encoded_path = urllib.parse.quote(abs_path)

visualize_url = f"http://localhost:5000/?load={encoded_path}"

print("\n" + "="*50)
print("       VISUALIZE THIS TREE IN WEB DASHBOARD")
print("="*50)
print(f"Click to Open: {visualize_url}")
print("="*50)

# try:
#     webbrowser.open(visualize_url)
# except:
#     pass

