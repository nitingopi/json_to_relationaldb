# JSON to Relational Data Extractor

This project provides a Python script that extracts relational data from JSON structures. It can handle various JSON formats and convert them into a relational database-like structure.

## Features

- Converts nested JSON structures into relational tables
- Handles arrays, nested objects, and mixed data types
- Preserves relationships between entities using foreign keys
- Generates unique IDs for each entity
- Provides comprehensive test coverage

## Requirements

To run this project, you need Python 3.12 and the following packages:

```
coverage==7.6.1
iniconfig==2.0.0
markdown-it-py==3.0.0
mdurl==0.1.2
packaging==24.1
pluggy==1.5.0
pprintpp==0.4.0
Pygments==2.18.0
pytest==8.3.3
pytest-clarity==1.0.1
pytest-cov==5.0.0
rich==13.8.1
ruff==0.6.7
```

You can install these dependencies using the provided `requirements.txt` file:

```
pip install -r requirements.txt
```

## Usage

To use the JSON extractor, run the `json_extractor.py` script:

```
python json_extractor.py
```

By default, the script reads from a file named `sample_data.json` in the same directory. You can modify the script to accept command-line arguments for different input files.

## Testing

The project includes a comprehensive test suite using pytest. To run the tests:

```
pytest test_json_extractor.py
```

The test suite covers various scenarios including:
- Simple nested structures
- Arrays of objects
- Complex nested structures with arrays
- Mixed data types and nested arrays

## Project Structure

- `json_extractor.py`: Main script containing the JSON extraction logic
- `test_json_extractor.py`: Test suite for the extractor
- `sample_data.json`: Sample JSON data for testing
- `requirements.txt`: List of Python package dependencies

## Contributing

Contributions to improve the extractor or expand its capabilities are welcome. Please ensure that any pull requests include appropriate tests and maintain the existing code style.

## License

[Insert your chosen license here]