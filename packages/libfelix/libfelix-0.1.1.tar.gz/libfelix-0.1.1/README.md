# flx
Felix without ei. 😁

Felix' library of snippets.

- few dependencies
- keep it simple


## Installation
```
pip install libfelix
```


## flx.git
```python
>>> from flx.git import Repo
>>> r = Repo('.')
>>> r.head
'9e260ece8558ba9a6c4ad6a9c89905630fe0140b'
```


## Development
```
pyenv virtualenv 3.10.11 flx
pyenv local flx
pip install -U pip
pip install -e .[dev]
```
