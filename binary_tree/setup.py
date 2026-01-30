from setuptools import setup, find_packages

setup(
    name="binary-tree",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "PyYAML>=6.0",
        "Flask",
    ],
    author="Tanmay Yadav",
    description="A Python package for Binary Tree YAML serialization and manipulation",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'binary-tree-viz=binary_tree.web.app:main',
        ],
    },
    python_requires=">=3.12",
)
