
Write-Host "--- Verification: Installing binary_tree_yaml from local source ---" -ForegroundColor Cyan

# 1. Create a virtual environment
Write-Host "1. Creating Virtual Environment 'test_env'..."
python -m venv test_env

# 2. Activate and Install
# We run this as a single block to ensure activation persists for the commands
& .\test_env\Scripts\python.exe -m pip install ./task1

# 3. Verify
Write-Host "3. Running Verification Script..."
$script = @"
from binary_tree_yaml import create_tree, add_node, print_tree
import sys
print(f'\n[SUCCESS] Package imported from: {sys.path}')
root = create_tree(100)
add_node(root, 'L', 50)
add_node(root, 'R', 150)
print('Tree created with installed package:')
print_tree(root)
"@
Set-Content -Path "test_installed.py" -Value $script

& .\test_env\Scripts\python.exe test_installed.py

Write-Host "--- Done ---"
