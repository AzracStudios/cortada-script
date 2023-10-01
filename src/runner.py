from os import path
from main import *

with open(path.abspath('examples/pattern.cortada'), "r") as src:
    code = src.readlines()
    code_str = ""
    for line in code:
        code_str += line
    
    val, error = run(code_str, False, "fib.cortada")
    
    if error:
        print(error.generate_error_text())



