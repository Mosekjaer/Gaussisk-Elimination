import tkinter as tk

def clean_round(value, ndigits=4):
    """
    Runder værdi til ndigits decimaler og returnerer 0.0 hvis resultatet er meget tæt på nul.
    """
    r = round(value, ndigits)
    return 0.0 if abs(r) < 1e-12 else r

def print_matrix_equation(A, b, output):
    """
    Viser matrix-ligningen A·x = b i et læsbart format.

    A er en matrix med koefficienter, b er resultatkolonnen.
    Udskriften sendes til et tekstfelt (output), f.eks. en Tkinter Text-boks.

    Args:
        A (list of lists): Koefficientmatrix, f.eks. [[2, 3], [1, -1]]
        b (list): Resultatvektor, f.eks. [5, 1]
        output (tk.Text): Tkinter tekstfelt, hvor matrixen skal vises
    """
    output.insert(tk.END, "Matrixform (A·x = b):\n\n")

    rows = len(A)
    cols = len(A[0]) if A else 0
    b_len = len(b)

    for i in range(rows):
        A_row = "[" + " ".join(f"{clean_round(x, 2):>5}" for x in A[i]) + "]"
        x_row = f"[x{i+1}]"
        
        if i < b_len:
            b_row = f"[{clean_round(b[i], 2):>5}]"
        else:
            b_row = "[  ?  ]"  
        
        line = f"{A_row}   {x_row}   =   {b_row}"
        output.insert(tk.END, line + "\n")

    output.insert(tk.END, "\n")

def print_matrix_step(matrix, step_description, output):
    """
    Viser en matrix med en beskrivelse af trinnet.
    """
    output.insert(tk.END, f"\n{step_description}:\n")
    for row in matrix:
        output.insert(tk.END, f"{[clean_round(x, 6) for x in row]}\n")
    output.insert(tk.END, "\n")

def parse_inputs(entries):
    """
    Parser input fra GUI entries til matrix A og vektor b.
    """
    try:
        a_keys = [key for key in entries if key.startswith("a")]
        b_keys = [key for key in entries if key.startswith("b")]

        rows = len(b_keys)
        cols = max(int(key[2:]) for key in a_keys) + 1

        A = [[float(entries[f"a{i}{j}"].get()) for j in range(cols)] for i in range(rows)]
        b = [float(entries[f"b{i}"].get()) for i in range(rows)]

        return A, b
    except ValueError:
        return None, None 