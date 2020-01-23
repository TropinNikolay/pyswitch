import unittest
from pyswitch import parser, support_switch, exec


class ParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.unit1 = """
        switch x:
            case 1:
                print(1)
                break
            case 2:
                print(2)
                break
            case 3:
                switch y:
                    case a:
                        print(a)
                    case b:
                        switch z:
                            case c:
                                print(c)
                                break
                        break
                break
"""
        self.unit2 = """switch x:
            case 1:
                print(1)
                break
            case 2:
                print(2)
                break
            case 3:
                switch y:
                    case a:
                        print(a)
                    case b:
                        switch z:
                            case c:
                                print(c)
                                break
                        break
                break
"""
        self.unit3 = """
        switch x:
            case 1:
                switch y:
                    switch z:
                        switch t:
                            case 2:
                                break
                break        
"""
        self.unit4 = """
        switch x:
            case 1:
                print(1)
                break
        switch x:
            case 1:
                print(1)
                break
        
        switch x:
            case 1:
                print(1)
                break
                
        switch x:
            case 1:
                print(1)
                break
"""
        self.unit5 = """
        print("Hello world!")
        d = 1
        while True:
            print("1")
            break
        switch x:
            case 1:
                print("Goodbye world!")
                break
        print("something else")
        if a == b:
            d += 1
"""
        self.unit1_answer = """
        while True:
            if (x) == (1):
                print(1)
                break
            if (x) == (2):
                print(2)
                break
            if (x) == (3):
                while True:
                    if (y) == (a):
                        print(a)
                    if (y) == (b):
                        while True:
                            if (z) == (c):
                                print(c)
                                break
                            break
                        break
                    break
                break
            break
"""
        self.unit3_answer = """
        while True:
            if (x) == (1):
                while True:
                    while True:
                        while True:
                            if (t) == (2):
                                break
                            break
                        break
                    break
                break        
            break
"""
        self.unit4_answer = """
        while True:
            if (x) == (1):
                print(1)
                break
            break
        while True:
            if (x) == (1):
                print(1)
                break
            break
        
        while True:
            if (x) == (1):
                print(1)
                break
                
            break
        while True:
            if (x) == (1):
                print(1)
                break
            break
"""
        self.unit5_answer = """
        print("Hello world!")
        d = 1
        while True:
            print("1")
            break
        while True:
            if (x) == (1):
                print("Goodbye world!")
                break
            break
        print("something else")
        if a == b:
            d += 1
"""

    def test_only_switch_parsing(self):
        self.assertEqual(self.unit1_answer, parser(self.unit1))

    @unittest.expectedFailure
    def test_inappropriate_indent_parsing(self):
        self.assertEqual(self.unit1_answer, parser(self.unit2))

    def test_nested_switch_parsing(self):
        self.assertEqual(self.unit3_answer, parser(self.unit3))

    def test_consistent_switch_parsing(self):
        self.assertEqual(self.unit4_answer, parser(self.unit4))

    def test_not_only_switch_parsing(self):
        self.assertEqual(self.unit5_answer, parser(self.unit5))


@support_switch
def my_function_with_switch(a: int,
                            b: int,
                            c: int):
    """
    print("hello")
    switch a:
        case b:
            return True
        case c:
            return False
    """


class SupportSwitchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.function = support_switch(my_function_with_switch)

    def test_decorator_execute_new_function(self):
        self.assertTrue(callable(self.function))

    def test_function_return_true(self):
        self.assertTrue(my_function_with_switch(2 * 2, 4, 5))


class ExecTest(unittest.TestCase):
    @staticmethod
    def test_no_switch_executing():
        exec("""
print("hello")
print(2 + 2)
""")

    @staticmethod
    def test_switch_executing():
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


if __name__ == "__main__":
    unittest.main()
