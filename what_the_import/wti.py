import ast
from pathlib import Path
from sys import stdlib_module_names


def union_of_counting_dicts(dict_a: dict[str, int], dict_b: dict[str, int]) -> dict[str, int]:
    dict_union = {}
    for key in dict_a | dict_b:
        dict_union[key] = int(dict_a.get(key) or 0) + int(dict_b.get(key) or 0)
    return dict_union


def find_imports_in_file(py_file: Path) -> dict[str, int]:
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


def find_imports(py_file_or_dir: Path, *, ignore_stdlib: bool) -> dict[str, int]:
    found_imports = {}
    if py_file_or_dir.is_dir():
        for py_file in py_file_or_dir.rglob("*.py"):
            found_imports = union_of_counting_dicts(found_imports, find_imports_in_file(py_file))
    elif py_file_or_dir.is_file():  # also look into file not ending in *.py if asked directly
        found_imports = find_imports_in_file(py_file_or_dir)
    else:
        raise OSError(f"Provided path {py_file_or_dir} is neither file nor directory.")

    if ignore_stdlib:
        found_imports = {module: count for module, count in found_imports.items() if module not in stdlib_module_names}

    return found_imports



if __name__ == "__main__":
    #proj_folder = Path(r"C:\my_files\Projekte\WhatTheImport\example_pys")
    proj_folder = Path(r"C:\my_files\Projekte\FaviconGen")

    found_imports = find_imports(proj_folder, ignore_stdlib=True)


    import pprint
    pprint.pprint(found_imports)
