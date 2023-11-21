# Ipyllogger
[SCHOOL PROJECT - PYTHON BASICS] | Minimum Python package to write logs in a file

## Installation

```bash
pip install ipyllogger
```

## Tests

```bash
make test
```

## Usage

```python
from ipyllogger import Logger
from ipyllogger import level

logger = Logger()

# Log an error
logger.log("Hello World", level.ERROR)

# Log a warning
logger.log("Hello World", level.WARNING)

# Get all errors logs
print(logger.get_logs(level.ERROR))

# Get all warnings logs
print(logger.get_logs(level.WARNING))

```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contributors
- [Makendy ALEXIS](https://github.com/RagnarBob)
- [Louis Midson LAJEANTY](https://github.com/midsonlajeanty)

## Project Director
- [Lub Lorry Lamisère](https://github.com/lemayzeur)