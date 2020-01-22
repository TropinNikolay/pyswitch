"""
This is a quick example of using pyswitch module
"""

from pyswitch import support_switch
from pyswitch import exec


@support_switch
def my_function_with_switch(a: int, b: int, c: int):
    """
    print("hello")
    switch a:
        case b:
            return True
        case c:
            return False
    """


assert my_function_with_switch(2 * 2, 4, 5)
print(my_function_with_switch(2 * 2, 4, 5))
print(my_function_with_switch)
print(my_function_with_switch.__doc__)
print(my_function_with_switch.__name__)

exec("""
print("hello")
print(2 + 2)
""")

a, b, c = 2, 4, 4
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
