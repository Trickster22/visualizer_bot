from sympy import Eq, solve, symbols, sympify
import sympy as sp

def f(x, equation_str):
    xvar = sp.symbols('x')
    equation = sp.sympify(equation_str)
    return equation.subs(xvar, x)

def f2(x1, x2, equation_str):
    x1var = sp.symbols('x1')
    x2var = sp.symbols('x2')
    equation = sp.sympify(equation_str)
    return equation.subs({x1var: x1, x2var: x2})