# Transcribe API

Transcribe API is a high-performance FastAPI backend application designed to provide a robust and scalable backend solution for AWS Transcription. It uses an OpenAPI spec and Swagger utilizing JSON Schema to ensure easy integration and high performance.

![Screenshot 2024-06-03 at 2 35 57 PM](https://github.com/bastosmichael/transcribe-api/assets/1518708/3894219c-2013-4f3e-a421-1ea7e19e4afc)


## Features

- **FastAPI Backend**: Offers a high-performance backend solution that incorporates a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.

- **Swagger Compatibility**: Supports Swagger, a powerful interface for REST APIs that allows both developers and non-developers to interact with the API’s resources. It provides insightful information about the operations, parameters, responses, and the direct testing of API endpoints within its UI.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You'll need to install the following items before you can use Transcribe API:

- Python 3.6 or later
- Poetry (Python dependency management)
- Docker (for containerization)

### Installation

#### Installing Poetry

To install Poetry, you can use the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installing Poetry, make sure it's available in your PATH. You may need to add the following line to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

#### Setting Up the Application

Clone the repository:

```bash
git clone https://github.com/bastosmichael/transcribe-api.git
```

Navigate to the project directory:

```bash
cd transcribe-api
```

Install the required dependencies using Poetry:

```bash
poetry install
```

Run the application:

```bash
poetry run transcribe
```

The server should be running and the API can be accessed at `localhost:8000`.

### API Documentation

The API documentation can be viewed at `localhost:8000/docs` when the server is running. The documentation is interactive, so you can test out API calls directly in your browser.

### Running Tests

After installing the necessary dependencies, you can run the test suite using `pytest`. The command `poetry run pytest` runs `pytest` within the project's virtual environment:

```bash
poetry run pytest
```

This command will discover all test cases in your project (i.e., all files matching the pattern `test_*.py` or `*_test.py` in the current directory and subdirectories) and run them.

If you want to run a specific test file, you can specify it directly. For example, to only run the tests in `test_main.py`, you can use the following command:

```bash
poetry run pytest tests/test_main.py
```

For more advanced usage, please refer to the [`pytest` documentation](https://docs.pytest.org/en/latest/).

## Contributing

We welcome contributions to Transcribe API! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE.md) file for details.

## Contact

If you have any questions, feel free to reach out to us at [bastosmichael@gmail.com](mailto:bastosmichael@gmail.com).

## Acknowledgments

We would like to thank the creators and contributors of FastAPI, Swagger, and Poetry for their amazing tools that have helped make this project possible.
