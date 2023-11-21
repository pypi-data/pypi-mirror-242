# jsonmodipy

[![Python 3.10][python_badge]](https://www.python.org/downloads/release/python-3100/)
[![License: AGPL v3][agpl3_badge]](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black][black_badge]](https://github.com/ambv/black)

Deconstructs Python code into modular JSON format and back. The JSON consists
of the following modular components:

- Docstring of a .py file
- Classes
- Class documentation
- Methods
- Method documentation
- Raw code

Before it outputs a Python file to a `.json` file, it verifies that it is able
to reconstruct the `.json` file back to its original file. It runs `pip`
package `black` to wash out any formatting differences between the original and
reconstructed Python files. This however, does not fix new line spacing.

## Usage

You can use this package with `pip` only, `conda` only, or you can build it
yourself. It requires your openai credentials in a `config.ini` file.

### Credentials

Store your credentials like:

```yml
[chatgpt3.5]
username=<your>@<email>.com
password=your_openai_password
```

in a file named `config.ini`. It is easiest to store this file directly
above/outside the jsonmodipy repository. (Such that that parent folder
contains: `config.ini` and: `jsonmodipy/Readme.md`.) Otherwise you have to
specify the path to that config with every call to this `pip` package
using:`--config-filepath <the path to your config file>`.

## Build with conda

First build and install this pip package with:

```bash
conda env create --file environment.yml
conda activate jsonmodipy
playwright install
```

## Build with pip

Or for a more lightweight installation procedure:

```sh
# Run the code
pip install -r requirements.txt
playwright install
```

## Build from source

```
pip install -r requirements.txt
pip install build setuptools wheel
rm -r dist
rm -r build
python -m build
pip install -e .
playwright install
```

### First Run: Login and Ask Documentation

Run the command below to login and ask a question to chatgpt 3.5.  *After* your
first login to ChatGPT, this python code may not recognise the environment
directly, and fail. If so, please try calling this package once more, it
stores your browser context, so after your first login, it should enter the
expected environment and work.

```sh
python -m jsonmodipy \
  --engine chatgpt3.5 \
  --channel browser \
  --ask docstring \
  --filepath \
  /home/name/git/Hiveminds/Documentation-and-Test-Writing-Bot/testrepos/\
doctestbot/src/pythontemplate/class_and_classmethods.py \
  --func-location .class.MyClass.function.class_method \
  --question-filepath example_questions/function_docstring.txt \
  --config-filepath /home/name/git/config.ini
```

### Get source code

This outputs the source code of a function to the terminal.

```sh
python -m jsonmodipy \
  --engine chatgpt3.5 \
  --channel browser \
  --get src_code \
  --filepath "/home/name/git/Hiveminds/Documentation-and-Test-Writing-Bot\
/testrepos/doctestbot/src/pythontemplate/class_and_classmethods.py" \
  --func-location .class.MyClass.function.class_method \
  --config-filepath /home/name/git/config.ini
```

## Apply

```
python -m jsonmodipy \
  --engine chatgpt3.5 \
  --channel browser \
  --apply docstring \
  --filepath \
  /home/name/git/Hiveminds/Documentation-and-Test-Writing-Bot/testrepos/\
doctestbot/src/pythontemplate/class_and_classmethods.py \
  --func-location .class.MyClass.function.class_method \
  --iteration 0 \
  --config-filepath /home/name/git/config.ini
```

The `--iteration` stands for the solution number given by the LLMs, e.g. `0`
corresponds to `0.json`, and `1` corresponds to `1.json`.

## Get File Structures

This creates a `.json` file, with the structure of the filepaths listed
in `--filepaths`. The structure consists of a json dictionary with:
`<filepath>:{<A list of class and function locations>}` where a location is the
nested position of a function or class. Like:
`class.MyClass.function.class_method` for a function named `class_method` that
is inside class `MyClass`. Note that locations always start with a dot.

```
python -m jsonmodipy --engine chatgpt3.5 \
--channel browser \
--set structure_json \
--structure-json-filepath \
"/home/name/git/Hiveminds/Documentation-and-Test-Writing-Bot/json_structures/\
=home=name=git=Hiveminds=Documentation-and-Test-Writing-Bot=testrepos=\
doctestbot.json" \
--filepaths \
"/home/name/git/Hiveminds/Documentation-and-Test-Writing-Bot/testrepos/\
doctestbot/setup.py;/home/name/git/Hiveminds/Documentation-and-Test-Writing\
-Bot/testrepos/doctestbot/src/pythontemplate/methods.py;/home/name/git/\
Hiveminds/Documentation-and-Test-Writing-Bot/testrepos/doctestbot/src/\
pythontemplate/parses_correctly.py"
```

You can also get the names of the functions in a file with:

```
python -m jsonmodipy \
  --engine chatgpt3.5 \
  --channel browser \
  --get func_names \
  --filepath \
  ../D*/testrepos/doctestbot/src/pythontemplate/\
docstring_documentation_and_class_and_classmethods_and_methods.py \
  --config-filepath /home/name/git/config.ini
```

## Developer

```bash
pre-commit install
pre-commit autoupdate
pre-commit run --all
```

## Publish pip package

Build the pip package with:

```bash
pip install --upgrade pip setuptools wheel
pip install twine
```

Install the pip package locally with:

```bash
pip install build setuptools wheel
rm -r dist
rm -r build
python -m build
pip install -e .
```

Upload the pip package to the world with:

```bash
rm -r dist
rm -r build
python -m build
python3 -m twine upload dist/\*
```

## Sphinx Documentation

To auto-generate the Sphinx documentation for your Python project look into the
`/docs` folder.

- The `conf.py` is the configuration that is used to build your
  Sphinx documentation. Followed by:

```
make html
```

- The index.rst contains the main page and documentation file-structure.
- You can include other `.rst` files that automatically include the
  documentation of a Python file, for example in `docs/source/example.rst`. In
  this `.rst` file, you refer to a "module"=`.py` file in a path relative to the
  root of this project.

### Include .py file example

To add a file in `src/jsonmodipy/helper.py` you
create a `docs/source/some_name.rst` file with content:

```rst
.. _helper-module:

Helper Module
===============

.. automodule:: jsonmodipy.helper
  :members:
  :undoc-members:
  :show-inheritance:

And here you can just type additional text that will be displayed on the site.
```

and to the `index.rst` you add it like:

```rst
.. jsonmodipy documentation master file, created by

Welcome to jsonmodipy's documentation!
=========================================

.. toctree::
   :maxdepth: 2

   example
   some_name
```

### Generate Sphinx Documentation

Then to generate/update the Sphinx documentation you can run from the root dir:

```sh
cd docs
 [ -d "_build" ] && rm -r "_build" ; [ -d "html" ] && rm -r "html" ; \
  clear ; \
  python -m sphinx -T -E -b html -d _build/doctrees -D language=en . html
```

<!-- Un-wrapped URL's below (Mostly for Badges) -->

[agpl3_badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.6-blue.svg
