import tkinter as tk

def clean_round(value, ndigits=4):
    r = round(value, ndigits)
    return 0.0 if abs(r) < 1e-12 else r

def print_matrix_step(matrix, step_description, output, var_names=None):
    output.insert(tk.END, f"\n{step_description}:\n")
    if var_names:
        header = "    " + "".join(f"{name:>10}" for name in var_names) + "     RHS"
        output.insert(tk.END, header + "\n")
    for i, row in enumerate(matrix):
        formatted_row = [f"{clean_round(x, 6):>10}" for x in row[:-1]]
        formatted_row.append(f"{clean_round(row[-1], 6):>10}")
        output.insert(tk.END, f"R{i+1}: " + "  ".join(formatted_row) + "\n")
    output.insert(tk.END, "\n")

def parse_inputs(entries):
    try:
        a_keys = [k for k in entries if k.startswith("a")]
        b_keys = [k for k in entries if k.startswith("b")]
        rows = len(b_keys)
        cols = max(int(k[2:]) for k in a_keys) + 1
        A = [[float(entries[f"a{i}{j}"].get()) for j in range(cols)] for i in range(rows)]
        b = [float(entries[f"b{i}"].get()) for i in range(rows)]
        return A, b
    except ValueError:
        return None, None

def print_matrix_equation(A, b, output, var_names=None):
    output.insert(tk.END, "Matrixform (A·x = b):\n\n")
    rows = len(A); cols = len(A[0]) if A else 0
    if var_names is None:
        var_names = [f"x{i+1}" for i in range(cols)]
    for i in range(max(rows, cols)):
        A_row = "[" + "  ".join(f"{clean_round(x,2):>6}" for x in A[i]) + " ]" if i < rows else ""
        x_row = f"[ {var_names[i]:^6} ]" if i < cols else ""
        b_row = f"   =   [ {clean_round(b[i],2):>6} ]" if i < rows else ""
        output.insert(tk.END, f"{A_row}   {x_row}{b_row}\n")
    output.insert(tk.END, "\n")
