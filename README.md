# Information 🐍
- Version: `1.0.0`
- Author: pyautoml
- Github: https://github.com/pyautoml
- Name: `Checkpoints`
- License: CC BY-NC. This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
- Description: Track and verify the order of method calls using Python decorators, with automatic path and file management for saving call history as JSON.

# Start here 🔥
## Why to use?


To make sure that decorated methods will be called in particular order. Why it is important:
- it helps to avoid missing or skipping important steps in data processing,
- tests do not cover sequentional method calls, and some can be skipped,
- in bigger codebases, flow might be intimidating to track,
- allows to generate tracking history to precisely verify which methods were called,
- allows to re-assign given methos calls multiple times,
- decorators can be easily removed or added which doesn't contaminate the core code.

Happy coding! 🎉

## First steps
1. Using python 3.12 is advised to run this code. Please install `pytest` if you'd like to run tests.
2. To check how to use this code, run `playground.py` file.

## Decorators by example
The main idea is to wrap methods to create a strict order of calls. For example:
```python
@checkpoint([3, 1, 2])
def dummy_method():
    ...
```
will be expected to be called as the first, second, and third in the main code. The numeric order passed via decorator **doesn't matter**.


✅ Different example:
```python
@checkpoint([1, 3])
def calculate(a: int, b: int) -> int:
    return a + b

@checkpoint([4])
def say_hello() -> None:
    print("Hello!")

@checkpoint([2])
def greet(name: str) -> None:
    print(f"Hi, {name}!")
```

In such case, the Checkpoint class expects methods to be invoked in the following order:
- calculate()
- checkpoint()
- calculate()
- say_hello()


✅ Not all methods must be decorated. Wrap only the methods you'd like to track. For example:
```python
@checkpoint([1, 3])
def calculate(a: int, b: int) -> int:
    return a + b

@checkpoint()
def say_hello() -> None:
    print("Hello!")

@checkpoint([2])
def greet(name: str) -> None:
    print(f"Hi, {name}!")
```

✅ Invoking methods in this order will **NOT** cause any error:
- calculate()
- say_hello()
- checkpoint()
- calculate()


❌ Skipping any decorated method results in an IndexError (as the expected index of the invoked method doesn't match the reigstered one):
```python
@checkpoint([1, 3])
def calculate(a: int, b: int) -> int:
    return a + b

@checkpoint([4])
def say_hello() -> None:
    print("Hello!")

@checkpoint([2])
def greet(name: str) -> None:
    print(f"Hi, {name}!")
```

In such case, the Checkpoint class expects methods to be invoked in the following order:
- calculate()
- say_hello()       # should be called as 4th, not 2nd.
- checkpoint()
- calculate()

# Files 📁
1. Structure
```bash
.
├── checkpoint
│   ├── __init__.py
│   ├── playground.py               # run to check usecases
│   ├── README.md                   # you are here
│   ├── requirements.txt            # install libraries
│   ├── models                      # object models
│   │   ├── __init__.py             
│   │   ├── abstract_path_model.py  # PathModel contract
│   │   ├── path_model.py           # defines how to access and manage paths
│   │   ├── file_model.py           # defines how to process files
│   │   └── checkpoint_model.py     # the main model for tracking methods calling order
│   └── test                        # general unit tests
│       ├── __init__.py
│       ├── test_file_model.py
│       └── test_path_model.py
└──
```

# Bugs 🐛
Please report bugs directly via dedicated `Issues`: https://github.com/pyautoml/checkpoints/issues

# Tests ⚗️
Run all tests from the main directory: ./checkpoint to properly refer to paths:
```bash
# ./checkpoint
pytest
```
