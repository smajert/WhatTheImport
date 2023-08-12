# What the import?

## Introduction
Did this ever happen to you? You get handed an old, sprawling python repo
without any indication of what packages you would need to install to
even get it running? 

Fear not, for `whattheimport` can help. It is a small cli-tool that uses
python's `ast` (abstract syntax trees) package to parse all *.py-files in
a project and extract the names of all imported packages.

## Installation
Note: For `whattheimport` to work, python >= 3.10 is required.
1. Use git to clone the repo.
2. Navigate to the folder `WhatTheImport` and run the command
   ```python -m pip install .```
   
## Usage
After installation, the command `whattheimport` should be available in
your terminal (you can check with `where whattheimport` in the windows
command prompt or `which whattheimport` in bash).

Simply run `whattheimport <project_root>` to find all imports.
E.g. `whattheimport .` should return 
```
{'argparse': 2,
 'ast': 2,
 'json': 2,
 'pathlib': 2,
 'pprint': 2,
 'pytest': 1,
 'sys': 2,
 'warnings': 2,
 'whattheimport': 1}
```
if you run it in the `WhatTheImport` directory.

The key is the name of the import and the following integer shows how often this import is requested
in the `*.py` files. You can also pass the `--ignore_stdlib` flag to
`whattheimport` to ignore imports from the python standard library.


## References
I used  GaretJax's answer to [this](https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module)
stackoverflow question as a basis for extracting the python imports
via `ast`.