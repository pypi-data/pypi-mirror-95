# Kved finder

A tool that allows you to find a kved tree for the specific kved.

## Installation

```bash
pip install kved_finder
```

## Usage

### Run from terminal
```bash
python3 -m kved_finder.kved_finder <kved>
```
The results will be saved to kved_result.json
<hr>

### Import as package

```python3
from kved_finder import kved_finder
result = kved_finder.parse_kved('01.11')
```

## Example


Example output for kved 01.11
```json
{
  "name": "Вирощування зернових культур (крім рису), бобових культур і насіння олійних культур",
  "type": "class",
  "parent": {
    "name": "Вирощування однорічних і дворічних культур",
    "type": "group",
    "num_children": 7,
    "parent": {
      "name": "Сільське господарство, мисливство та надання пов'язаних із ними послуг",
      "type": "division",
      "num_children": 7,
      "parent": {
        "name": "Сільське господарство, лісове господарство та рибне господарство",
        "type": "section",
        "num_children": 3
      }
    }
  }
}
```
