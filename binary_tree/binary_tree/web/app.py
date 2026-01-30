from flask import Flask, render_template, request, jsonify
import sys
import os
import yaml
import webbrowser

# Use relative imports from the package
from ..yaml_handler import dict_to_node, node_to_dict, tree_to_yaml_string
# We don't strictly need build_tree_from_yaml here as we parse string directly, 
# but if needed: from ..yaml_handler import build_tree_from_yaml

app = Flask(__name__)

@app.route('/')
def index():
    initial_yaml = ""
    load_path = request.args.get('load')
    if load_path:
        if os.path.exists(load_path):
            try:
                with open(load_path, 'r') as f:
                    initial_yaml = f.read()
            except Exception as e:
                initial_yaml = f"# Error loading file: {e}"
        else:
             initial_yaml = f"# File not found: {load_path}"
             
    return render_template('index.html', initial_yaml=initial_yaml)

@app.route('/process', methods=['POST'])
def process_yaml():
    try:
        content = request.json.get('yaml')
        if not content:
            return jsonify({'error': 'No YAML content provided'}), 400

        data = yaml.safe_load(content)
        
        if isinstance(data, dict) and "root" in data:
            tree_data = data["root"]
        else:
            tree_data = data
            
        root = dict_to_node(tree_data)
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

def main():
    """Entry point for the CLI."""
    url = "http://localhost:5000"
    print(f"\n\033[92m[+] Web App running at: {url}\033[0m")
    print("\033[94m[+] Click the link above or copy it to your browser to visualize.\033[0m\n")
    # Only open if explicitly requested or let user click. User prefers manual click.
    app.run(debug=False, port=5000) # Debug false for CLI usage usually

if __name__ == '__main__':
    main()
