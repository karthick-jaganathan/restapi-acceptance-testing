# Rest API - Acceptance Tests (Behave) - Demo

This repository demo's the acceptance tests for the REST API. The acceptance tests are written in Python and uses the `behave` package and `behavex` library to run the tests.

---

## Pre-requisites

1. `Python 3.6` or above
4. Install `flask` using `pip install flask`
3. Install `requests` using `pip install requests`
2. Install `behave` using `pip install behave`
5. Install `behavex` using `pip install behavex`

To install all the dependencies, you can use the following command:

```bash
  pip install -r requirements.txt
```

**Note:** create a virtual environment and install the above packages if you don't want to install them globally.

---

## How to run the tests

Navigate to the repository:

```bash
  cd restapi-acceptance-testing
```

Start the demo `flask` application:

```bash
  python app.py
```

To run the tests using the `python` command, you can use the following command:

```bash
  python -m behave tests/features
```

This will run the acceptance tests and output the results to the console.

---

To run tests in parallel, you can use the behavex's `--parallel-scheme` and `--parallel-processes` options:

```bash
  python -m behavex tests/features --parallel-scheme=scenario --parallel-processes=4
```

This will run the tests in parallel using the `scenario` scheme with `4` processes.

---

You can use the `--tags` option to run tests with specific tags:

```bash
  python -m behave tests/features --tags=<your-tag-goes-here>
```

---

## Running tests using `behavex`

To run the tests with `behavex` command, you can use the following command:

```bash
  behavex <your-feature-file-path-goes-here> <any-addtional-arguments>
```

> **Note:** use `behavex` command instead of `python -m restapis.tests.acceptance` to run the tests with `behavex`.

---

## Running tests using `behave`

`behave` is a BDD test framework for Python that is used by `behavex`. You can use `behave` to run the tests if you prefer.

```bash
  behave <your-feature-file-path-goes-here> <any-addtional-arguments>
```

---

For more information on how to write and run acceptance tests, please refer to the following documentation:

- [behavex documentation](https://pypi.org/project/behavex/)
- [behave documentation](https://behave.readthedocs.io/en/latest/)

## Coverage

To generate coverage report, you can use the following command:

```bash
  coverage run -m behave tests/features
  coverage report
```

This will generate a coverage report for the acceptance tests.

If you want to generate an HTML report, you can use the following command:

```bash
  coverage html
```

---

If ran using parallel processes, you can use the following command to generate the coverage report:

```bash
  coverage combine
  coverage report
```

This will generate a coverage report for the acceptance tests ran in parallel. However, the report may not be accurate due to the parallel execution.

---

For more information on how to use the `coverage` tool, please refer to the [coverage documentation](https://coverage.readthedocs.io/en/coverage-6.2/).
