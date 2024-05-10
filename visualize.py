import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import func
import sympy as sp
import plotly.graph_objects as go

def makeGif(equation, x, f_x, a, b, chat_id):
    x_values = np.arange(-10, 10, 0.1)
    y_values = []
    for v in x_values:
        y_values.append(func.f(v, equation))
    miny = int(min(f_x))
    if miny > 0:
        miny *=-1

    fig, ax = plt.subplots()
    vline_a = ax.axvline(a[0],miny - 10, miny * -1 + 10, color='g')
    vline_b = ax.axvline(b[0],miny - 10, miny * -1 + 10, color='g')
    points, = ax.plot(x[0], f_x[0], "ro")

    ax.plot(x_values, y_values)

    ab = plt.gca()
    ab.spines["left"].set_position('center')
    ab.spines["bottom"].set_position('center')
    ab.spines["top"].set_visible(False)
    ab.spines["right"].set_visible(False)
    ax.set_xlim(-10, 10)
    ax.set_ylim(miny - 10, miny * -1 + 10)


    def update(frame):
        vline_a.set_xdata(a[frame])
        vline_b.set_xdata(b[frame])
        points.set_data(x[frame], f_x[frame])
        return vline_a, vline_b, points
    
    animation = anim.FuncAnimation(fig, update, frames=range(0, len(x)), interval=1000)
    file_path = f'media/{chat_id}_Метод половинного деления.gif'
    animation.save(file_path)

def make3dGif(eq, lim_eq, res):
    print(res)
    x = np.linspace(-5, 5, 20)
    y = np.linspace(-5, 5, 20)
    X, Y1 = np.meshgrid(x, y)
    Z1 = np.zeros_like(X)
    Z2 = np.zeros_like(X)
    Y2 = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z1[i, j] = func.f2(X[i, j], Y1[i, j], eq)
            Z2[i, j] = i*10
            Y2[i, j] = f3(X[i,j], lim_eq)


    surface1 = go.Surface(x=X, y=Y1, z=Z1, opacity=0.5, colorscale='Reds')
    surface2 = go.Surface(x=X, y=Y2, z=Z2, opacity=1, colorscale='Greens')
    scatter1 = go.Scatter3d(x=[res[0]['x1']], y=[res[0]['x2']], z=[res[0]['f(x)']], mode='markers', marker=dict(size=5, color='red'))
    
    frames_data = []
    for i in range(len(res)):
        frames_data.append(go.Frame(data=[
            surface1,
            surface2, 
            go.Scatter3d(x=[res[i]['x1']], y=[res[i]['x2']], z=[res[i]['f(x)']], mode='markers', marker=dict(size=5, color='red'))
        ]))
    
    # Создание фигуры
    fig = go.Figure(data=[surface1, surface2, scatter1])
    fig.frames = frames_data
    # Настройка параметров отображения
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

    # Установка параметров анимации
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])],
                  margin=dict(l=0, r=0, t=0, b=0))

    fig.write_html("./media/index.html")
    # Отображение
    #fig.show()
    

def f3(x, lim_eq):
    x_sym = sp.symbols("x1")
    y_sym = sp.symbols("x2")
    eq = sp.solve(sp.sympify(lim_eq), y_sym)[0]
    return(eq.subs({x_sym: x}))

#make3dGif2("10*x1^2+3*x2^2-19", "3*x1+x2-9", [{'x1': 0.8350515463917526, 'x2': 0.9278350515463918, 'f(x)': -9.44425550005314}, {'x1': 1.5576923076923077, 'x2': 1.7307692307692308, 'f(x)': 14.2507396449704}, {'x1': 1.9877300613496933, 'x2': 2.208588957055215, 'f(x)': 35.1443035116113}, {'x1': 2.1350906095551894, 'x2': 2.372322899505766, 'f(x)': 43.4698669286658}, {'x1': 2.175409148132606, 'x2': 2.4171212757028955, 'f(x)': 45.8514754021571}, {'x1': 2.185727838094234, 'x2': 2.4285864867713713, 'f(x)': 46.4681587933865}, {'x1': 2.1883228240508665, 'x2': 2.431469804500963, 'f(x)': 46.6237040532194}])