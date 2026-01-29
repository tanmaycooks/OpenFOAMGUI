from setuptools import setup, find_packages

setup(
    name="binary_tree_yaml",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyYAML>=6.0",
    ],
    author="Tanmay Yadav",
    description="A Python package for Binary Tree YAML serialization and manipulation",
    python_requires=">=3.12",
)
