from sympy.parsing.latex import parse_latex
from sympy import symbols
import numpy as np
from sympy.utilities.lambdify import lambdify
from sympy.abc import x
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from fasthtml.common import *


#функция которая латех выражение делает функцией на отрезке от -пи до пи с разбиением в 1000 точек и считает результат
def partitio(latex_expr):
    latex_expr= parse_latex(latex_expr)
    N = 1000  # Количество точек
    a = np.linspace(-np.pi, np.pi, N, endpoint=False)
    
    numpy_array_of_arguments= a
    func = lambdify(x, latex_expr,'numpy') # returns a numpy-ready function
    numpy_array_of_results = func(numpy_array_of_arguments)
    return a, numpy_array_of_results


# Вычисление Lp-нормы
def lp_norm(func_values, p, dx):
    return (np.sum(np.abs(func_values) ** p) * dx) ** (1 / p)



def graphicLp(latex_expr):
    a, func_values = partitio(latex_expr)
    p_values = np.linspace(1, 10, 500)  # Диапазон значений p
    lp_norms_original = []
    lp_norms_transformed = []
    dx = a[1] - a[0]
    print(func_values)
    for p in p_values:
        # Исходная Lp-норма
        original_norm = lp_norm(func_values, p, dx)
        lp_norms_original.append(original_norm)
    
        # Преобразование Фурье
        fourier_values = fft(func_values)
    
    
        # Фильтрация
        filtered_values = np.abs(fourier_values)
    
        # Обратное преобразование
        reconstructed_values = ifft(filtered_values).real
    
        # Норма после преобразований
        transformed_norm = lp_norm(reconstructed_values, p, dx)
        lp_norms_transformed.append(transformed_norm)
     
    # Шаг 7: Построение графика
    grafig=plt.figure(figsize=(10, 6))
    plt.plot(p_values, lp_norms_original, label="Исходная Lp-норма")
    plt.plot(p_values, lp_norms_transformed, label="Lp-норма после преобразований")
    plt.xlabel("$p$")
    plt.ylabel("$L_p$ норма")
    plt.title("Зависимость $L_p$ нормы от $p$")
    plt.legend()
    plt.grid()    
    return grafig




app, rt = fast_app(pico=True)



@rt
def index():
    return Titled('LaTeX Renderer',
           P('Введите LaTeX-код в поле ниже:'),
           Form(Textarea(placeholder='Введите ваш LaTeX код...', name='latex_input', rows=4, cols=40),
           Button('Рендерить', hx_post='/render', hx_target='#render-output')),
           Div(id='render-output', style="margin-top: 20px;")
    )

@rt('/render')
def post(latex_input:str):
    graphicLp(latex_input)
    # Save the figure to a BytesIO object as a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    import base64
    base64_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    return Div(
        H4('Результат:'),
        Div(Img(src=f"data:image/png;base64,{base64_image}"))
    )


serve()