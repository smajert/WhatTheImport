import pytest

from whattheimport import wti

EXPECTED_IMPORTS_STDLIB = {
    "pathlib": 1,
    "random": 1,
    "time": 2,
}

EXPECTED_IMPORTS_NON_STDLIB = {"certainly_not_in_stdlib": 1, "deepdiff": 1, "matplotlib": 1, "numpy": 1}


@pytest.fixture()
def example_project(tmp_path):
    """
    Project structure:
        example_project/
            should_not_be_found.txt
            folder_a/
                stdlib_only.py
            folder_b/
                non_stdlib_only.py
    """
    proj_folder = tmp_path / "example_project"
    folder_a = proj_folder / "folder_a"
    folder_b = proj_folder / "folder_b"
    proj_folder.mkdir()
    folder_a.mkdir()
    folder_b.mkdir()

    # file contents:
    should_not_be_found = "import ast"
    stdlib_only = (
        "from pathlib import Path\n"
        "from random import Random as random_alias\n"
        "import time\n"
        "import time as time_alias\n"
    )
    non_stdlib_only = (
        "from certainly_not_in_stdlib import something as something_else\n"
        "import deepdiff\n"
        "from matplotlib import pyplot\n"
        "import numpy as np\n"
    )

    with open(proj_folder / "should_not_be_found.txt", "w") as should_not_be_found_file:
        should_not_be_found_file.write(should_not_be_found)

    with open(folder_a / "stdlib_only.py", "w") as stdlib_only_file:
        stdlib_only_file.write(stdlib_only)

    with open(folder_b / "non_stdlib_only.py", "w") as non_stdlib_only_file:
        non_stdlib_only_file.write(non_stdlib_only)

    return proj_folder


def test_find_imports_in_file(example_project):
    found_stdlib_imports = wti.find_imports_in_file(example_project / "folder_a/stdlib_only.py")
    found_stdlib_imports |= wti.find_imports_in_file(example_project / "folder_b/non_stdlib_only.py")
    assert found_stdlib_imports == EXPECTED_IMPORTS_STDLIB | EXPECTED_IMPORTS_NON_STDLIB


def test_find_imports_in_project(example_project):
    found_imports = wti.find_imports(example_project, ignore_stdlib=False)
    assert found_imports == EXPECTED_IMPORTS_STDLIB | EXPECTED_IMPORTS_NON_STDLIB


def test_find_non_stdlib_imports_in_project(example_project):
    found_imports = wti.find_imports(example_project, ignore_stdlib=True)
    assert found_imports == EXPECTED_IMPORTS_NON_STDLIB


def test_find_imports_in_specific_file(example_project):
    found_imports = wti.find_imports(example_project / "should_not_be_found.txt", ignore_stdlib=False)
    assert found_imports == {"ast": 1}


def test_exception_if_file_does_not_exist(example_project):
    with pytest.raises(IOError):
        wti.find_imports(example_project / "not_a_file.py", ignore_stdlib=False)
