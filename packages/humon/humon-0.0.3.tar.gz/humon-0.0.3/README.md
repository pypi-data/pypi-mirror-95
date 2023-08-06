# humon-py

This is a Python3 package for reading [Humon|https://github.com/spacemeat/humon] token streams.

# Installing humon-py

To install and use in python:

```bash
$ pip install humon
```

## Usage

```python
from humon import humon
t = humon.Trove.fromString('{foo:bar}')
print (t.root['foo'])
```

# Developing humon-py

To install humon-py and the tools needed to develop and run tests, run the following:

```bash
$ pip install -e .[dev]
```
