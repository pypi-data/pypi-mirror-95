![Python package](https://github.com/BooneAndrewsLab/sgd_chromosomal_features/workflows/Python%20package%20build%20and%20publish/badge.svg)
# SGD Chromosomal Features

Handy tools to work with SGD's chromosomal features

## Dependencies
- [intermine](https://github.com/intermine/intermine-ws-python)

## Installation
```bash
pip install sgd-chromosomal-features
```
or simply download collect_features.py file and run it independently.

## Usage
### Standalone executable
```bash
# If downloaded only the script file:
$ python collect_features.py --help
# If installed via pip or setup.py:
$ collect_features --help
```
### API
```python
from yeast.collect_features import fetch_from_sgd
current_features = fetch_from_sgd()
```
