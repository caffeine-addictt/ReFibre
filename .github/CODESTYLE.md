# Code Style
The following is a general guide on how to style your code so that the
project remains consistent throughout all files

<br />


## General Guidelines
Listed is a example class used demonstrate general rules you should follow throughout the development of your contribution.

- Docstrings are to follow reST (reStructuredText Docstring Format) as specified in [PEP 287](https://peps.python.org/pep-0287/)
- Private attributes are to be prefixed with an underscore
- Use of [typing](https://docs.python.org/3/library/typing.html) type hints
- All files are to use 2 space indenting

```python
class ExampleClass:
  """
  ExampleClass
  ------------
  Example class for CODESTYLE.md
  """
  # ^^^ reST Docstring Format

  _private_attribute : int # private attributes begin with a lowercase
  public_attribute   : int # type hint for integer is defined here

  def __init__(
    self,
    public_attribute: int # type hint for parameters
  ) -> None: # the expected return value of method
    """
    Initializes a ExampleClass

    Parameters
    ----------
    :param public_attribute: example attribute
    """
    self.public_attribute = public_attribute
    self.private_attribute = square(public_attribute)

  def square(self, value: int) -> int:
    """
    Example method that square roots a value

    Parameters
    ----------
    :param value: value that you want squared
    """
    return value**2
```
