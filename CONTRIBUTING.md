NLPretext
==============================

# How to contribute

## Dependencies

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you dont have `poetry` installed, you should run the command below.

```bash
make download-poetry; export PATH="$HOME/.local/bin:$PATH"
```

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run `install` command:

```bash
make install
```

To activate your `virtualenv` run `poetry shell`.

## Codestyle

After you run `make install` you can execute the automatic code formatting.

```bash
make format-code
```

### Checks

Many checks are configured for this project. Command `make check-style` will run black diffs, darglint docstring style and mypy.
The `make check-safety` command will look at the security of your code.

You can also use `STRICT=1` flag to make the check be strict.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Run `make format-code` to format your changes.
1. Run `STRICT=1 make check-style` to ensure that types and docs are correct
1. Run `STRICT=1 make check-safety` to ensure that security of your code is correct

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.

# Docstring format

We chose to use **Numpydoc** over the several [standards](https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format)

```
"""
My numpydoc description of a kind
of very exhautive numpydoc format docstring.

Parameters
----------
first : array_like
    the 1st param name `first`
second :
    the 2nd param
third : {'value', 'other'}, optional
    the 3rd param, by default 'value'

Returns
-------
string
    a value in a string

Raises
------
KeyError
    when a key error
OtherError
    when an other error
"""
```
