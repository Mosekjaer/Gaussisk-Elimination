import tkinter as tk
from utils import clean_round, print_matrix_step, print_matrix_equation

def gaussian_elimination(A, b, output, reduced=False, var_names=None):
    n = len(A); m = len(A[0])
    aug = [A[i] + [b[i]] for i in range(n)]
    if var_names is None:
        var_names = [f"x{i+1}" for i in range(m)]

    print_matrix_equation(A, b, output, var_names)
    print_matrix_step(aug, "Startmatrix (udvidet)", output, var_names)

    step = 1; row = 0
    for col in range(m):
        pivot_row = None
        for r in range(row, n):
            if abs(aug[r][col]) > 1e-12:
                pivot_row = r; break
        if pivot_row is None: continue
        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
            print_matrix_step(aug, f"Trin {step}: Bytter R{row+1} med R{pivot_row+1}", output, var_names)
            step += 1
        pivot = aug[row][col]
        if abs(pivot - 1.0) > 1e-12:
            factor = clean_round(1/pivot, 6)
            aug[row] = [x/pivot for x in aug[row]]
            print_matrix_step(aug, f"Trin {step}: Normaliserer R{row+1} (ganger med {factor})", output, var_names)
            step += 1
        if reduced:
            for r in range(n):
                if r != row and abs(aug[r][col]) > 1e-12:
                    f = aug[r][col]
                    aug[r] = [aug[r][j] - f*aug[row][j] for j in range(m+1)]
                    print_matrix_step(aug, f"Trin {step}: Eliminer i R{r+1}", output, var_names)
                    step += 1
        else:
            for r in range(row+1, n):
                if abs(aug[r][col]) > 1e-12:
                    f = aug[r][col]
                    aug[r] = [aug[r][j] - f*aug[row][j] for j in range(m+1)]
                    print_matrix_step(aug, f"Trin {step}: Eliminer i R{r+1}", output, var_names)
                    step += 1
        row += 1

    print_matrix_step(aug, "Slutmatrix (RREF)" if reduced else "Slutmatrix (REF)", output, var_names)

    rank = sum(any(abs(c)>1e-12 for c in r[:-1]) for r in aug)
    aug_rank = sum(any(abs(c)>1e-12 for c in r) for r in aug)
    if aug_rank > rank:
        output.insert(tk.END, "\nSystemet har INGEN løsning (inkonsistent).\n")
    elif rank < m:
        output.insert(tk.END, "\nSystemet har UENDELIGT mange løsninger.\n")
    else:
        output.insert(tk.END, "\nSystemet har en ENTYDIG løsning:\n")
        x = [0]*m
        for i in range(n-1,-1,-1):
            x[i] = aug[i][-1] - sum(aug[i][j]*x[j] for j in range(i+1,m))
        for i, val in enumerate(x):
            output.insert(tk.END, f"{var_names[i]} = {clean_round(val,4)}\n")

    output.insert(tk.END, "\n---\n© 2025 Fjederik\n")
