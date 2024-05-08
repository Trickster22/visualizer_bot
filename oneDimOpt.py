from sympy import Eq, solve, symbols, sympify
import math
import visualizer
import func

def golden(equation, epsilon, a0, b0, chat_id):
    a = [a0]
    b = [b0]
    y = []
    z = []
    f_y = []
    f_z = []
    k = 0
    while True:
        y.append(a[k] + ((3 - math.sqrt(5)) / 2) * (b[k] - a[k]))
        z.append(a[k] + b[k] - y[k])
        f_y.append(func.f(y[k], equation))
        f_z.append(func.f(z[k], equation))
        if f_y[k] <= f_z[k]:
            a.append(a[k])
            b.append(z[k])
            y.append(a[k + 1] + b[k + 1] - y[k])
            z.append(y[k])
        else:
            a.append(y[k])
            b.append(b[k])
            y.append(z[k])
            z.append(a[k + 1] + b[k + 1] - z[k])
        delta = math.fabs(a[k + 1] - b[k + 1])
        if delta <= epsilon:
            x = (a[k + 1] + b[k + 1])/2
            f_x = func.f(x, equation)
            return (f'Минимум - \'{x}\'\nФункция - \'{f_x}\'')
        else:
            k += 1

def HalfDivision(equation, epsilon, a0, b0, chat_id):
    a = [a0]
    b = [b0]
    x = []
    interval_length = []
    f_x = []
    f_y = []
    f_z = []
    y=[]
    z=[]
    k = 0
    x.append((a[k] + b[k]) / 2)
    while True:
        interval_length.append(abs(a[k] - b[k]))
        f_x.append(func.f(x[k], equation))
        y.append(a[k] + interval_length[k] / 4)
        z.append(b[k] - interval_length[k] / 4)
        f_y.append(func.f(y[k], equation))
        f_z.append(func.f(z[k], equation))
        if (f_y[k] < f_x[k]):
            b.append(x[k])
            a.append(a[k])
            x.append(y[k])
        elif (f_z[k] < f_x[k]):
            a.append(x[k])
            b.append(b[k])
            x.append(z[k])
        else:
            a.append(y[k])
            b.append(z[k])
            x.append(x[k])
        if (abs(b[k + 1] - a[k + 1]) <= epsilon):
            break
        k += 1
    f_x.append(func.f(x[k + 1], equation))
    visualizer.makeGif(equation, x, f_x, a, b, chat_id)
    return (f'Минимум - \'{x[k + 1] }\'\nФункция - \'{f_x[k + 1]}\'')