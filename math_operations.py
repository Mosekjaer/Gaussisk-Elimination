import tkinter as tk
from utils import clean_round, print_matrix_equation, print_matrix_step

def back_substitution(ref_matrix, output, var_names=None):
    """
    Løser et lineært ligningssystem ved hjælp af baglæns substitution
    på en matrix i række-echelon-form.

    Args:
        ref_matrix (list of lists): Den udvidede matrix (A|b) i REF.
        output (tk.Text): Tkinter tekstfelt hvor beregningerne vises.
        var_names (list): Liste af variabelnavne. Hvis None bruges x1, x2, osv.

    Returns:
        list: Løsningerne x1, x2, ..., som en liste af tal.
    """
    n = len(ref_matrix)
    m = len(ref_matrix[0]) - 1
    x = [0] * m

    if var_names is None:
        var_names = [f"x{i+1}" for i in range(m)]

    output.insert(tk.END, "\nBaglæns substitution:\n\n")

    for i in range(n - 1, -1, -1):
        row = ref_matrix[i]
        pivot_col = next((j for j, val in enumerate(row[:-1]) if abs(val) > 1e-12), None)
        if pivot_col is None:
            continue

        rhs = row[-1]
        coeff = row[pivot_col]

        symbol_terms = []
        value_terms = []
        for j in range(pivot_col + 1, m):
            term_coeff = clean_round(row[j], 4)
            if abs(term_coeff) > 1e-12:
                sign = " - " if term_coeff < 0 else " + "
                symbol_terms.append(f"{sign}{abs(term_coeff)} * {var_names[j]}")
                value_terms.append(f"{sign}{abs(term_coeff)} * {clean_round(x[j], 4)}")

        if symbol_terms:
            expr_symbol = f"{clean_round(rhs, 4)}" + "".join(symbol_terms)
            expr_value = f"{clean_round(rhs, 4)}" + "".join(value_terms)
        else:
            expr_symbol = f"{clean_round(rhs, 4)}"
            expr_value = f"{clean_round(rhs, 4)}"

        x_val = (rhs - sum(row[j] * x[j] for j in range(pivot_col + 1, m))) / coeff
        x[pivot_col] = x_val

        if abs(coeff - 1.0) < 1e-12:
            if not symbol_terms:
                output.insert(tk.END, f"{var_names[pivot_col]} = {clean_round(x_val, 4)}\n")
            elif expr_symbol == expr_value:
                output.insert(tk.END, f"{var_names[pivot_col]} = {expr_value} = {clean_round(x_val, 4)}\n")
            else:
                output.insert(tk.END, f"{var_names[pivot_col]} = {expr_symbol} = {expr_value} = {clean_round(x_val, 4)}\n")
        else:
            if not symbol_terms:
                output.insert(tk.END, f"{var_names[pivot_col]} = {clean_round(rhs, 4)} / {clean_round(coeff, 4)} = {clean_round(x_val, 4)}\n")
            else:
                output.insert(tk.END, f"{var_names[pivot_col]} = ({expr_symbol}) / {clean_round(coeff, 4)} = ({expr_value}) / {clean_round(coeff, 4)} = {clean_round(x_val, 4)}\n")

    return x

def gaussian_elimination(A, b, output, reduced=False, var_names=None):
    """
    Udfører Gaussisk elimination på matrix A og vektor b.
    Understøtter både almindelig række-echelon-form (REF)
    og reduceret form (RREF) afhængigt af 'reduced'-parameteren.

    Args:
        A (list of lists): Koefficientmatrix.
        b (list): Resultatvektor.
        output (tk.Text): Tkinter tekstfelt til visning af trinene.
        reduced (bool): Hvis True bruges RREF, ellers kun REF.
        var_names (list): Liste af variabelnavne. Hvis None bruges x1, x2, osv.
    """
    n = len(A)
    m = len(A[0])
    aug = [A[i] + [b[i]] for i in range(n)]

    if var_names is None:
        var_names = [f"x{i+1}" for i in range(m)]

    print_matrix_equation(A, b, output, var_names)
    print_matrix_step(aug, "Startmatrix (udvidet)", output, var_names)

    step = 1
    row = 0
    for col in range(m):
        pivot_row = None
        for r in range(row, n):
            if abs(aug[r][col]) > 1e-12:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
            print_matrix_step(aug, f"Trin {step}: Bytter R{row+1} med R{pivot_row+1} (for at få pivot i {var_names[col]})", output, var_names)
            step += 1

        pivot = aug[row][col]
        if abs(pivot - 1.0) > 1e-12:
            factor = clean_round(1 / pivot, 6)
            aug[row] = [x / pivot for x in aug[row]]
            print_matrix_step(aug, f"Trin {step}: Gør pivot til 1 i {var_names[col]} ved at gange R{row+1} med {factor} (1/{clean_round(pivot, 6)})", output, var_names)
            step += 1

        if reduced:
            for r in range(n):
                if r != row and abs(aug[r][col]) > 1e-12:
                    factor = aug[r][col]
                    aug[r] = [aug[r][j] - factor * aug[row][j] for j in range(m + 1)]
                    f_str = f"({clean_round(factor, 4)})" if factor < 0 else f"{clean_round(factor, 4)}"
                    print_matrix_step(aug, f"Trin {step}: Eliminer {var_names[col]} i R{r+1} ved: R{r+1} = R{r+1} - {f_str}·R{row+1}", output, var_names)
                    step += 1
        else:
            for r in range(row + 1, n):
                if abs(aug[r][col]) > 1e-12:
                    factor = aug[r][col]
                    aug[r] = [aug[r][j] - factor * aug[row][j] for j in range(m + 1)]
                    f_str = f"({clean_round(factor, 4)})" if factor < 0 else f"{clean_round(factor, 4)}"
                    print_matrix_step(aug, f"Trin {step}: Eliminer {var_names[col]} i R{r+1} ved: R{r+1} = R{r+1} - {f_str}·R{row+1}", output, var_names)
                    step += 1

        row += 1

    print_matrix_step(aug, "Slutmatrix (REF)" if not reduced else "Slutmatrix (RREF)", output, var_names)

    rank = sum(any(abs(cell) > 1e-12 for cell in row[:-1]) for row in aug)
    aug_rank = sum(any(abs(cell) > 1e-12 for cell in row) for row in aug)

    if aug_rank > rank:
        output.insert(tk.END, "\nSystemet har INGEN løsning (inkonsistent).\n")
    elif rank < m:
        output.insert(tk.END, "\nSystemet har UENDELIGT mange løsninger.\n")
    else:
        output.insert(tk.END, "\nSystemet har en ENTYDIG løsning:\n")
        if reduced:
            x = [0] * m
            for i in range(n):
                leading_col = next((j for j, val in enumerate(aug[i][:-1]) if abs(val - 1) < 1e-12), None)
                if leading_col is not None and leading_col < m:
                    x[leading_col] = aug[i][m]
        else:
            x = back_substitution(aug, output, var_names)

        for i, val in enumerate(x):
            output.insert(tk.END, f"{var_names[i]} = {clean_round(val, 4)}\n")

    output.insert(tk.END, "\n---\n© 2025 Fjederik - Mobilepay endelig et spejlæg.\n") 