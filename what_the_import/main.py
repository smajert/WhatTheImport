import ast
from collections import namedtuple
from pathlib import Path

Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
    with open(path) as fh:
       root = ast.parse(fh.read(), path)

    imports = []
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            imports.append(Import(module, n.name.split('.'), n.asname))

    return imports


if __name__ == "__main__":
    proj_folder = Path(r"C:\my_files\Projekte\WhatTheImport\example_pys")
    import pprint
    for py_file in proj_folder.rglob("*.py"):
        pprint.pprint(get_imports(py_file))
