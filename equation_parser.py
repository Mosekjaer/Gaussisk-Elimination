import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

transformations = standard_transformations + (implicit_multiplication_application,)

def parse_raw_equations(equations, output=None):
    """
    Parser rå ligninger og konverterer dem til matrixform (Ax = b).
    
    Args:
        equations (list): Liste af strenge med ligninger (f.eks. ["3x + 2y = 5", "y - z = 3"])
        output (tk.Text, optional): Tkinter tekstfelt til at vise mellemregninger
    
    Returns:
        tuple: (A, b, var_order) hvor:
            - A er koefficientmatrix
            - b er resultatvektor
            - var_order er liste af variabelnavne i den rækkefølge de bruges
    """
    # Find alle unikke variable og sorter dem
    var_order = sorted(
        {str(s) for eq in equations for s in parse_expr(eq.replace('=', '-(') + ')', 
        transformations=transformations).free_symbols},
        key=lambda x: x
    )
    
    if output:
        output.insert("end", "\nFundne variable (sorteret alfabetisk): " + ", ".join(var_order) + "\n")
    
    syms = sp.symbols(var_order)
    
    # Konverter hver ligning til standardform
    exprs = []
    for eq in equations:
        L, R = eq.split('=')
        exprs.append(parse_expr(L, transformations=transformations) - 
                    parse_expr(R, transformations=transformations))
    
    # Opbyg A-matrix og b-vektor
    n, m = len(exprs), len(syms)
    A = sp.zeros(n, m)
    b = sp.zeros(n, 1)
    
    for i, expr in enumerate(exprs):
        const, _ = expr.as_independent(*syms)
        b[i,0] = -const
        for j, s in enumerate(syms):
            A[i,j] = expr.coeff(s)
    
    # Konverter til Python lister
    A_matrix = [[float(A[i,j]) for j in range(m)] for i in range(n)]
    b_vector = [float(b[i,0]) for i in range(n)]
    
    if output:
        output.insert("end", "\nStandardform:\n")
        for i in range(n):
            line = []
            for j, var in enumerate(var_order):
                coeff = A_matrix[i][j]
                if j == 0:
                    line.append(f"{coeff} {var}" if coeff != 0 else "")
                else:
                    if coeff > 0:
                        line.append(f"+ {coeff} {var}" if coeff != 0 else "")
                    else:
                        line.append(f"- {abs(coeff)} {var}" if coeff != 0 else "")
            line = " ".join(filter(None, line))
            output.insert("end", f"{line} = {b_vector[i]}\n")
    
    return A_matrix, b_vector, var_order 