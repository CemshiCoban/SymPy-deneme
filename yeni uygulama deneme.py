from flask import Flask, render_template, request

from sympy import symbols
from sympy.parsing.latex import parse_latex

app = Flask(__name__)

def get_symbols_from_latex(latex_eq):
    parsed_expr = parse_latex(latex_eq)
    variable_names = parsed_expr.free_symbols
    symbols_dict = {str(var): symbols(str(var)) for var in variable_names}
    return symbols_dict

def convert_latex_to_sympy(latex_eq):
    symbols_dict = get_symbols_from_latex(latex_eq)
    sympy_expr = parse_latex(latex_eq)
    for var, sym in symbols_dict.items():
        sympy_expr = sympy_expr.subs(parse_latex(var), sym)
    return sympy_expr, list(symbols_dict.keys())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        latex_code = request.form['latex_code']
        sympy_expression, variable_list = convert_latex_to_sympy(latex_code)
        return render_template('result.html', latex_code=latex_code, sympy_expression=sympy_expression, variable_list=variable_list)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)