# lektor-nl2br

[![Run tests](https://github.com/cigar-factory/lektor-nl2br/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-nl2br/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cigar-factory/lektor-nl2br/branch/main/graph/badge.svg?token=0TVXPBzH8j)](https://codecov.io/gh/cigar-factory/lektor-nl2br)
[![PyPI Version](https://img.shields.io/pypi/v/lektor-nl2br.svg)](https://pypi.org/project/lektor-nl2br/)
![License](https://img.shields.io/pypi/l/lektor-nl2br.svg)
![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-nl2br%2Fjson)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

Lektor template filter to convert linebreaks to `<br>` tags

## Installation

```
pip install lektor-nl2br
```

## Usage

```
{{ "a line\nanother line" | nl2br }}
```
