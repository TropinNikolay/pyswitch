import inspect
from functools import wraps


def switch_loop(line: str, source_code: list):
    """
    This function changing only one switch-case statement
    :param line: line of source code with switch statement
    :param source_code: lines of source code (either from exec statement or function docstring)
    :return: str, modified switch-case part of source code (in terms of if-else statement)
    """
    left_parameter = line[line.index("switch") + 7: line.index(":")]
    code = ""
    insert_from = line.index("switch")
    code += " " * insert_from + "while True:\n"
    indent = insert_from + 4
    while True:
        try:
            line = source_code.pop(0)
            if line.startswith(" " * indent) and "switch" in line:
                code += switch_loop(line, source_code)
            elif line.startswith(" " * indent):
                try:
                    right_parameter = line[line.index("case") + 5: line.index(":")]
                    code += line.replace(f"case {right_parameter}", f"if ({left_parameter}) == ({right_parameter})") + "\n"
                except ValueError:
                    code += line + "\n"
            else:
                code += " " * indent + "break\n"
                source_code.insert(0, line)
                indent -= 4
                break
        except IndexError:
            code += " " * indent + "break\n"
            break
    return code


def parser(string: str):
    """
    This function parse source code and replace switch-case statement on if-else
    :param string: source code from exec or function docstring
    :return: modified source code with if-else statement instead of switch-case
    """
    source_code = string.split("\n")
    source_code = list(filter(None, source_code))

    new_string = "\n"
    while source_code:
        line = source_code.pop(0)
        if "switch" in line:
            try:
                code = switch_loop(line, source_code)
                new_string += code
            except ValueError:
                print("So far, I can not process your code correctly... Sorry :(")
        else:
            new_string += line + "\n"
    return new_string


def support_switch(function):
    """
    This function changing source code of function
    :param function: function to be decorated
    :return: decorated function with modified source code from docstring
    """
    source_code_lines = inspect.getsourcelines(function)[0]
    indent = source_code_lines[0].index("@")

    source_code = ""
    for line in source_code_lines:
        if line.startswith(f"{' ' * indent}def {function.__name__}"):
            function_def = line[indent:]
        elif not line.startswith(" " * indent + "@") and not line.startswith(" " * (indent + 4) + "\"\"\""):
            source_code += line[indent:]

    parsed_source_code = parser(source_code)

    new_source_code = function_def + parsed_source_code
    new_source_code = new_source_code.replace(f"def {function.__name__}", "def new_function")

    __builtins__["exec"](new_source_code)
    new_func = locals()["new_function"]

    return wraps(function)(new_func)


def exec(string: str, globals_arg=None, locals_arg=None):
    """
    This function accurately reproduce the built-in function exec,
    except that it also supports switch-case statement
    :param string: string to be executed
    :param globals_arg: global arguments
    :param locals_arg: local arguments
    :return: None
    """
    new_string = parser(string)

    globals_ = inspect.stack()[1][0].f_globals
    locals_ = inspect.stack()[1][0].f_locals

    if globals_arg is None and locals_arg is not None:
        raise ValueError
    if globals_arg is None:
        globals_arg = globals_
    if locals_arg is None:
        locals_arg = locals_

    __builtins__["exec"](new_string, globals_arg, locals_arg)
