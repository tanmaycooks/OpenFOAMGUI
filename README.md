# OpenFOAM GUI Internship Screening Task

This submission contains the solutions for Task 1 (Binary Tree Package) and Task 2 (Blender Addon).

## Structure
- `task1/`: Python package `binary_tree_yaml`.
- `task2/`: Blender addon `cfd_addon`.
- `resume.pdf`: Placeholder.
- `sop.pdf`: Placeholder.

## Task 1: Binary Tree Package

### Installation
Requires Python 3.12+.
```bash
pip install ./task1
```

### Usage
Run the sample test script:
```bash
cd task1
python test.py
```
This will read `test.yaml`, manipulate the tree, print results, and save to `output.yaml`.

### Testing
Run unit tests:
```bash
pytest task1/tests/test_all.py
```

## Task 2: Blender Addon

### Installation
1. Search for generic "addon install" in Blender or:
2. Go to **Edit > Preferences > Add-ons**.
3. Click **Install...** and select the `task2/cfd_addon/__init__.py` file (or zip the specific folder if preferred).
4. Enable **Object: CFD Screening Addon**.

### Features
- **Panel**: Located in 3D View Sidebar > "CFD Task" tab.
- **Distribute Cubes**: Input N (limit 20). Generates grid.
- **Delete Selected**: Deletes selected objects.
- **Merge Selected**: Merges meshes and removes internal faces.

## Author
Candidate Name
