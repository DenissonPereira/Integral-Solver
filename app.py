from flask import Flask, request, render_template
from sympy import Symbol, sympify
import numpy as np
import matplotlib.pyplot as plt
import  io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calcular_int():
    if request.method == 'POST': 
        area = 0
        f = request.form['f']
        x = Symbol('x')
        funcao_x = sympify(f)

        limite_inf = float(request.form['limite_inf'])
        limite_sup = float(request.form['limite_sup'])
        n = int(request.form['n'])
        dx = abs(limite_sup - limite_inf) / n

        def funcao(valor):
            return funcao_x.subs(x, valor)
        
        a = limite_inf
        b = limite_sup

        if a < b:
            while a <= b:
                area += funcao(a) * dx
                a = a + dx
        elif a ==b:
            area = '0'
        else:
            while b <= a:
                area += funcao(b) * dx
                b = b + dx

        val_x = np.linspace(limite_inf, limite_sup)
        val_y = [funcao(valor) for valor in val_x]

        # se o valor for real ele vai colocar em float se não vai ser zero
        val_y = [float(val) if val.is_real else 0 for val in val_y]
        plt.plot(val_x, val_y, label='f(X)')
        plt.fill_between(val_x, val_y, 0, color='green', alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend(['f(x) = {}'.format(f)])
        plt.grid(True)
        plt.title('Função \nÁrea = {}'.format(area))

        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_url = base64.b64encode(img_data.read()).decode('utf-8')

        plt.close()

        return render_template('resultado.html', area=area, img_url=img_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()