
import sys
import os
import time
from binary_tree import create_tree, add_node, print_tree, write_tree_to_yaml, run_viz

def run_demo():
    print("="*60)
    print("   TASK 1: BINARY TREE & VISUALIZATION DEMO")
    print("="*60)

    # 1. Create a Complex Tree
    print("\n[1] Generating Organizational Chart (Binary Tree)...")
    root = create_tree("CEO")
    
    # L = CTO Branch
    add_node(root, "L", "CTO")
    add_node(root, "LL", "VPEngr")
    add_node(root, "LR", "VPProduct")
    add_node(root, "LLL", "DevLead")
    add_node(root, "LLR", "QALead")
    add_node(root, "LRL", "ProdMgr")
    add_node(root, "LRR", "DesignLead")
    
    # R = CFO Branch
    add_node(root, "R", "CFO")
    add_node(root, "RL", "VPFinance")
    add_node(root, "RR", "VPOps")
    add_node(root, "RLL", "Accountant")
    add_node(root, "RLR", "Analyst")
    add_node(root, "RRL", "OpsMgr")
    add_node(root, "RRR", "HRMgr")

    # 2. Print to Console
    print("\n[2] Tree Structure (Console View):")
    print_tree(root)

    # 3. Save to YAML
    output_file = "organization.yaml"
    print(f"\n[3] Saving to '{output_file}'...")
    write_tree_to_yaml(root, output_file)
    print(f"    - Saved successfully.")

    # 4. Launch Visualization
    print("\n[4] Launching Web Visualization Dashboard...")
    print("    - A URL will be generated to visualize this specific tree.")
    print("    - The server will start automatically.")
    print("    - Please click the link below if it doesn't open automatically.")
    
    # Construct URL for auto-loading
    abs_path = os.path.abspath(output_file)
    import urllib.parse
    encoded_path = urllib.parse.quote(abs_path)
    print(f"\n    ---> \033[94mhttp://localhost:5000/?load={encoded_path}\033[0m <---\n")

    print("Press Ctrl+C to stop the server.")
    run_viz()

if __name__ == "__main__":
    run_demo()
