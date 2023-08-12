import argparse
import ast
import json
from pathlib import Path
from pprint import pprint
from sys import stdlib_module_names
import warnings


def _union_of_counting_dicts(dict_a: dict[str, int], dict_b: dict[str, int]) -> dict[str, int]:
    dict_union = {}
    for key in dict_a | dict_b:
        dict_union[key] = int(dict_a.get(key) or 0) + int(dict_b.get(key) or 0)
    return dict_union


def find_imports_in_file(py_file: Path) -> dict[str, int]:
    """
    Find packages imported in a python file.

    :param py_file: Location of the python file.
    :return: Package names and amount of times they are imported in `py_file`.
    """

    with open(py_file, "r", encoding="utf-8") as file:
        root = ast.parse(file.read(), filename=str(py_file))

    imported_packages: dict[str, int] = {}
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            imported_package = node.names[0].name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                warnings.warn(f"Unknown module in 'import from' statement in file {py_file}, listing as 'unknown' ...")
                imported_package = "unknown"
            else:
                imported_package = node.module.split(".")[0]
        else:
            continue

        if imported_package in imported_packages:
            imported_packages[imported_package] += 1
        else:
            imported_packages[imported_package] = 1

    return imported_packages


def find_imports(py_file_or_dir: Path, *, ignore_stdlib: bool) -> dict[str, int]:
    """
    Find packages imported in a python file or a python project.

    :param py_file_or_dir: Location of python file or project folder. If project folder, only *.py files will
        be searched for imports.
    :param ignore_stdlib: Whether to ignore all imports from the python standard library.
    :return: Package names and amount of times they are imported.
    """
    found_imports: dict[str, int] = {}
    if py_file_or_dir.is_dir():
        for py_file in py_file_or_dir.rglob("*.py"):
            found_imports = _union_of_counting_dicts(found_imports, find_imports_in_file(py_file))
    elif py_file_or_dir.is_file():  # also look into file not ending in *.py if asked directly
        found_imports = find_imports_in_file(py_file_or_dir)
    else:
        raise OSError(f"Provided path {py_file_or_dir} is neither file nor directory.")

    if ignore_stdlib:
        found_imports = {module: count for module, count in found_imports.items() if module not in stdlib_module_names}

    return found_imports


def main() -> None:
    parser = argparse.ArgumentParser(description="List all python imports in a file or in all *.py files of a project.")
    parser.add_argument("target", help="File or directory to list imports from", type=Path)
    parser.add_argument(
        "--ignore_stdlib", action="store_true", help="Ignore all imports from the python standard library."
    )
    parser.add_argument("--json_out", type=Path, default=None, help="Optional json-file to output found packages to")
    args = parser.parse_args()

    imports = find_imports(args.target, ignore_stdlib=args.ignore_stdlib)
    pprint(imports)
    if args.json_out is not None:
        with open(args.json_out, "w", encoding="utf-8") as json_file:
            json.dump(imports, json_file, indent=3)


if __name__ == "__main__":
    main()
