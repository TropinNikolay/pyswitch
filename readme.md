#pyswitch

What is it?
-----------

This is simple switch-case implementation in python.

Installation
------------

No additional packages needed.

Getting Started
------------

```python
from pyswitch import support_switch
from pyswitch import exec
```
To try a quick use of pyswitch see **example.py**

**_Please note_** that the user must enter their code in the appropriate format (with the correct indent).

For more detailed information see **example of usage**.

Example of usage
------------

#####exec
```python
a, b, c = 2, 4, 5
d = None

exec("""
switch a*a:
    case b:
        print("Foo")
        d = 1
        break
    case c:
        print("Bar")
        d = 2
        break
assert d == 1
""")

assert d == 1
```
**Output:**
```python
Foo
```

#####@support_switch
```python
@support_switch
def my_function_with_switch(a: int, b: int, c: int):
    """
    print("Hello world!")
    switch a:
        case b:
            return True
        case c:
            return False
    """


assert my_function_with_switch(2 * 2, 4, 5) 
```
**Output:**
```python
Hello world!
```

Running the tests
------------

You can also run tests for this project from **testing.py** module.

Contacts
--------

tropinnikolay@gmail.com