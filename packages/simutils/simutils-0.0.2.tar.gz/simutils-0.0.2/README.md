# simutils

**Note that this package is not yet implemented.**

## Usage

It logs the argument of the function and other relevant information to a JSON file.

```python
>>> from simutils import log_function

>>> @log_function
... def double_val(x):
...    return x * 2
...
>>> double_val(4)
8
```

Then the content of the JSON file will be:

```json
{
    "simulation_name": "double_val_20210216_141001",
    "status": "success",
    "computer_name": "MyComputer",
    "python_version": "3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)]",
    "cwd": "current/working/directory",
    "output_directory": "logs/double_val_20210216_141001",
    "summary_filepath": "path/to/this/file",
    "called_function": "double_val",
    "start_time": "2021-02-16 14:10:02",
    "end_time": "2021-02-16 14:10:03",
    "simulation_time": "0:00:01.012345",
    "args": {
        "x": 4
    }
}
```

You can pass arguments to the decorator, and you can also decorate functions in a Python script.

```python
@log_function(
    git_repo=os.path.join(os.path.dirname(__file__), '..', '..'), # git repository to log
)
def triple_val(x):
    return x * 3
```

## To-Do's

- [ ] Send a notification when a function execution is finished.
- [ ] Integrate with a native Python logger.
- [ ] Reproduce the original environment
