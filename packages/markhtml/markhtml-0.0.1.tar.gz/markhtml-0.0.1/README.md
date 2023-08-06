[![CircleCI](https://circleci.com/gh/AumitLeon/markdown_html_converter.svg?style=svg)](https://circleci.com/gh/AumitLeon/markdown_html_converter) [![PyPI version](https://badge.fury.io/py/markhtml.svg)](https://badge.fury.io/py/markhtml)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Documentation Status](https://readthedocs.org/projects/markdown-html-converter/badge/?version=latest)](https://markhtml.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://pepy.tech/badge/markhtml)](https://pepy.tech/project/markhtml)

Markdown to HTML
====================

Markdown to HTML converter. Converts a Markdown file into an HTML file
formed of two columns:

- TOC (left-column)
  - An auto generated Table of Contents based in the markdown headings
- Markdown content (right-column)

![example](https://raw.githubusercontent.com/marcanuy/markhtml/main/example.png)


# Install

1. Create virtualenv.

~~~
python3 -m venv ~/.virtualenvs/markhtml
~~~

2. Activate venv.

~~~
source ~/.virtualenvs/markhtml/bin/activate
~~~

3. Install requirements.
   
~~~
pip install -r requirements.txt
~~~

# Usage

To convert
[example.md](https://raw.githubusercontent.com/marcanuy/markhtml/main/examples/example.md)
using `src/markhtml.py path-to-markdown-file.md` generates [example.html](https://github.com/marcanuy/markhtml/blob/main/examples/example.html)

~~~
src/markhtml.py examples/example.md
Generated file: examples/example.html
~~~

# Notes

Uses
[python-markdown](https://python-markdown.github.io/reference/index.html)
with [TOC](https://python-markdown.github.io/extensions/toc/#usage) extension.
