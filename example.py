from pyswitch import support_switch
from pyswitch import exec_switch as exec


@support_switch
def my_function_with_switch(a: int, b: int, c: int):
    """
    switch a:
        case b:
            return True
        case c:
            return False
    """
    print("hello")


assert my_function_with_switch(2 * 2, 4, 5)
print(my_function_with_switch(2 * 2, 4, 5))
print(my_function_with_switch)
print(my_function_with_switch.__doc__)

exec("""print("hello")
print(2 + 2)""")

a, b, c = 2, 4, 5
d = None

string = """
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
"""
exec(string)
