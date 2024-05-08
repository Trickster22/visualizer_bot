import sympy as sp
import func
import visualizer


def penalty(user_data):
    eq = user_data['equation']
    lim_eq = user_data['lim']
    epsilon = float(user_data['e'])
    k = 0
    r = float(user_data['r'])
    c = int(user_data['c'])
    x = []
    while True:
        x.append(find_x(eq, lim_eq, r))
        x1 = x[k]['x1']
        x2 = x[k]['x2']
        x[k]['f(x)'] = func.f2(x1, x2, eq)
        if p(lim_eq, r, x1, x2) <= epsilon:
            visualizer.make3dGif(eq, lim_eq, x)
            return (f'x1: {x1}\nx2: {x2}\nf(x): {func.f2(x1, x2, eq)}')
        r *= c
        k += 1
        
    
    
def find_x(eq, lim_eq, r):
    x1 = sp.symbols('x1')
    x2 = sp.symbols('x2')
    r_sym = sp.symbols('r')
    function = sp.sympify(f'{eq} + (r/2) * ({lim_eq}) ^ 2')
    res = sp.solve([function.diff(x1), function.diff(x2)], (x1, x2))
    x = {}
    x['x1'] = float(res[x1].subs(r_sym, r))
    x['x2'] = float(res[x2].subs(r_sym, r))
    return x


def p(lim_eq, r, x1, x2):
    x1_sym = sp.symbols('x1')
    x2_sym = sp.symbols('x2')
    r_sym = sp.symbols('r')
    equation = sp.sympify(f'(r/2) * ({lim_eq}) ^ 2')
    return equation.subs({x1_sym: x1, x2_sym: x2, r_sym: r})