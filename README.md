# Demoblaze

Playwright Python pytest

## Project structure:

* **tests:** definition of test suites and scenarios

* **conftest.py:** allows you to define fixtures, plugins, and hooks that can be shared across multiple test files in a subdirectories.

* **pytest.ini** is a configuration file for Pytest that allows you to set options and modify the behavior of Pytest for a specific project.

## Installation

Install the Pytest plugin:

    pip install pytest-playwright

Install the required browsers:

    playwright install

#### Running all

To run all the scripts with default setting simply type:

    pytest

#### Running specific test

    pytest tests/test_cases.py::test_login

#### Running tests matching given expression
    
    pytest -k login

#### Generate reporting

    pytest --template=html1/index.html --report=report.html

## GitHub Actions

## Additional links

https://drive.google.com/drive/folders/1PBmEBkONCdK9oGTLp6VAVzTicZOTo-MA?usp=sharing
