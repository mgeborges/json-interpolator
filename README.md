# JSON Interpolator

## Overview
The JSON Interpolator is a Python package for validating and rendering templates with placeholders in JSON-like strings. It ensures placeholders are correctly formatted and substitutes them with provided values.

## Features
- **Validation**: Ensures placeholders meet naming conventions and detects duplicates.
- **Rendering**: Dynamically replaces placeholders with values from a dictionary.
- **Object-Oriented Design**: Encapsulated within the `JSONInterpolator` class for easy reuse and extension.

## Placeholder Format
Placeholders should follow the syntax:
```
<<placeholder_name>>
```
Where:
- `placeholder_name` cannot start with a digit.
- `placeholder_name` must include at least one word character (letters, digits, or underscores).

## Installation
Clone the repository and ensure you have Python installed.


## Usage
### Example
```python
from json_interpolator.interpolator import JSONInterpolator

template = '{"key": "<<placeholder_name>>"}'
params = {"placeholder_name": "value"}

result = JSONInterpolator.render_template(params, template)
print(result)  # Outputs: {"key": "value"}
```

## Error Handling
- Raises `ValueError` for duplicate placeholders.
- Raises `ValueError` for placeholders starting with a digit or containing only underscores.

## Testing
The package includes a test suite in the `tests/` directory. To run tests:

### Using `unittest`
Run tests from the root directory:
```bash
python -m unittest discover -s tests
```

### Using `pytest`
If you prefer `pytest`:
```bash
pip install pytest
pytest
```

## Dependencies
This project does not require external dependencies beyond the standard library.

## Directory Structure
```
json_interpolator/
├── json_interpolator/
│   ├── __init__.py
│   ├── interpolator.py
├── tests/
│   ├── __init__.py
│   ├── test_interpolator.py
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.cfg
```

## License
MIT License

