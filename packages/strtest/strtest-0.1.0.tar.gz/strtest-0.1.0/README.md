# Python String Test Runner

Unittest wrapper that runs tests contained in strings.

## Setup

    pip install strtest

## Running tests

    run_str_test.py [-f function_name] file_with_the_function.py test_file.py

There is an example [here](#example)

## Test files

Test files must contain a class called `TestCase` that inherits from `str_test.TestCaseWrapper`. All methods with names starting with `test_` will be considered tests.

```python
from strtest import str_test

class TestCase(str_test.TestCaseWrapper):
    TIMEOUT = 1  # In seconds

    def test_1(self):
        result = self.function(1, 2)
        self.assertEqual(3, result, msg=f'Results are not equal. Expected: 3. Got: {result}')

    def test_2(self):
        self.assertTrue(False, msg='This will always fail')
```

## Example

Assume you have the test file `all_tests.py` with the code above and want to test the file `my_implementation.py` containing the following code:

```python
def add_numbers(a, b):
    return a + b
```

You can run the tests with:

    run_str_test.py -f add_numbers my_implementation.py all_tests.py
