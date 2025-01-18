# JSON Interpolator

## Overview
The JSON Interpolator is a Python package for validating and rendering templates with placeholders in JSON-like strings. It ensures placeholders are correctly formatted and substitutes them with provided values.

## Features
- **Validation**: Ensures placeholders meet naming conventions.
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
from json_interpolator import JSONInterpolator

template = """
    {
        "name": <<name>>,
        "age": <<age>>,
        "roles": <<roles>>,
        "contact_info": <<contact_info>>,
        "is_active": <<is_active>>
    }
"""
params = {
    "name": "Alice",
    "age": 30,
    "roles": ["admin", "support"],
    "contact_info": {"email": "alice@company.com", "phone": "(555) 555-5555"},
    "is_active": True
}

result = JSONInterpolator.render_template(params, template)
print(result)
# Outputs:
# {
#     "name": "Alice",
#     "age": 30,
#     "roles": ["admin", "support"],
#     "contact_info": {"email": "alice@company.com", "phone": "(555) 555-5555"},
#     "is_active": true
# }
```
Please note that there is no need to wrap string placeholders with quotes inside templates. Doing so will lead to an invalid JSON.

## Error Handling
Raises:
- `ValueError` if
    - invalid placeholders are found. Placeholder names are expected to follow the Python variables naming standards.
    - an invalid JSON is generated because of bad template formatting.
- `TypeError` if the template is not a string or if the parameters are not provided in a dictionary.

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

## License
MIT License

