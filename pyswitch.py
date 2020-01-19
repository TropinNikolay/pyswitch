import inspect
from functools import wraps


def support_switch(function):
    # получаем массив строк исходного кода и собираем новый исходник
    source_code = inspect.getsourcelines(function)[0]
    parameter = None
    new_source_code = ""
    while source_code:
        line = source_code.pop(0)
        if "@" in line or "\"\"\"" in line:
            continue
        if "switch " in line:
            parameter = line[line.index("switch ") + 7: line.index(":\n")]
            continue
        if "return" in line:
            new_source_code += line.replace("    return", "return")
            continue
        new_source_code += line

    new_source_code = new_source_code.replace("    case", f"if {parameter} ==")
    new_source_code = new_source_code.replace(f"def {function.__name__}", "def new_function")

    exec(new_source_code)
    new_func = locals()["new_function"]

    return wraps(function)(new_func)


def exec_switch(string: str):
    """
    SWITCH-CASE in EXEC()
    NOT FUNCTION !
    """
    try:
        string.index("switch ")
    except ValueError:
        exec(string)

    source_code = string.split("\n")
    new_string = "while True:\n"
    while source_code:
        line = source_code.pop(0) + "\n"
        if not line[0] == " ":
            if line != "\n":
                if "switch " not in line:
                    new_string += f"    break\n"
                else:  # тогда считываем параметр в switch строке
                    parameter = string[string.index("switch ") + 7: string.index(":\n")]
                    continue
            else:  # тогда выкидываем эту строчку (она состоит из одного \n)
                continue
        if "case" in line:
            new_string += line.replace("case", f"if {parameter} ==")
            continue
        new_string += line
    return new_string
