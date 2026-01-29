
from flask import Flask, render_template, request, jsonify
import sys
import os
import yaml

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import build_tree_from_yaml, node_to_dict, dict_to_node, tree_to_yaml_string
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_yaml():
    try:
        content = request.json.get('yaml')
        if not content:
            return jsonify({'error': 'No YAML content provided'}), 400
            
        # Parse YAML to dict first to validate and structure
        # We use a temporary file or just parse string directly if the library supports it.
        # The library build_tree_from_yaml takes a file path.
        # We might need to modify the library or write a temp file.
        # Let's check binary_tree_yaml/yaml_handler.py content again.
        # It has build_tree_from_yaml(file_path).
        # But it also has dict_to_node(data). 
        # So we can just yaml.safe_load(string) -> dict -> dict_to_node.
        
        # Parse YAML string
        data = yaml.safe_load(content)
        
        # Handle "root" key if present (matching library logic)
        if isinstance(data, dict) and "root" in data:
            tree_data = data["root"]
        else:
            tree_data = data
            
        # from binary_tree_yaml.yaml_handler import dict_to_node
        
        root = dict_to_node(tree_data)
        # Convert back to dict to ensure we have the processed structure (including any defaults/logic)
        processed_data = node_to_dict(root)
        output_yaml = tree_to_yaml_string(root)
        
        return jsonify({
            'tree': processed_data, 
            'output_yaml': output_yaml,
            'message': 'Tree built successfully'
        })
        
    except yaml.YAMLError as e:
        return jsonify({'error': f"YAML Syntax Error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    url = "http://localhost:5000"
    print(f"\n\033[92m[+] Web App running at: {url}\033[0m")
    print("\033[94m[+] Click the link above or copy it to your browser to visualize.\033[0m\n")
    # Optional: Auto open
    # webbrowser.open_new(url)
    app.run(debug=True, port=5000)
