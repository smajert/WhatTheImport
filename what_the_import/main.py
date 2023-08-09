import ast
from pathlib import Path
from sys import stdlib_module_names


def union_of_counting_dicts(dict_a: dict[str, int], dict_b: dict[str, int]) -> dict[str, int]:
    dict_union = {}
    for key in dict_a | dict_b:
        dict_union[key] = int(dict_a.get(key) or 0) + int(dict_b.get(key) or 0)
    return dict_union


def find_imported_packages(py_file: Path) -> dict[str, int]:
    with open(py_file) as file:
       root = ast.parse(file.read(), filename=str(py_file))

    imported_packages = {}
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            imported_package = node.names[0].name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            imported_package = node.module.split('.')[0]
        else:
            continue

        if imported_package in imported_packages:
            imported_packages[imported_package] += 1
        else:
            imported_packages[imported_package] = 1

    return imported_packages


if __name__ == "__main__":
    #proj_folder = Path(r"C:\my_files\Projekte\WhatTheImport\example_pys")
    proj_folder = Path(r"C:\my_files\Projekte\FaviconGen")
    ignore_stdblib = True

    found_imports = {}
    for py_file in proj_folder.rglob("*.py"):
        found_imports = union_of_counting_dicts(found_imports, find_imported_packages(py_file))

    if ignore_stdblib:
        found_imports = {module: count for module, count in found_imports.items() if module not in stdlib_module_names}


    import pprint
    pprint.pprint(found_imports)
