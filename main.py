import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pyperclip  

def clean_round(value, ndigits=4):
    
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

def back_substitution(ref_matrix, output):
    """
    Løser et lineært ligningssystem ved hjælp af baglæns substitution
    på en matrix i række-echelon-form.

    Args:
        ref_matrix (list of lists): Den udvidede matrix (A|b) i REF.
        output (tk.Text): Tkinter tekstfelt hvor beregningerne vises.

    Returns:
        list: Løsningerne x1, x2, ..., som en liste af tal.
    """
    n = len(ref_matrix)
    m = len(ref_matrix[0]) - 1
    x = [0] * m

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
                symbol_terms.append(f"{sign}{abs(term_coeff)} * x{j+1}")
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
                output.insert(tk.END, f"x{pivot_col+1} = {clean_round(x_val, 4)}\n")
            elif expr_symbol == expr_value:
                output.insert(tk.END, f"x{pivot_col+1} = {expr_value} = {clean_round(x_val, 4)}\n")
            else:
                output.insert(tk.END, f"x{pivot_col+1} = {expr_symbol} = {expr_value} = {clean_round(x_val, 4)}\n")
        else:
            if not symbol_terms:
                output.insert(tk.END, f"x{pivot_col+1} = {clean_round(rhs, 4)} / {clean_round(coeff, 4)} = {clean_round(x_val, 4)}\n")
            else:
                output.insert(tk.END, f"x{pivot_col+1} = ({expr_symbol}) / {clean_round(coeff, 4)} = ({expr_value}) / {clean_round(coeff, 4)} = {clean_round(x_val, 4)}\n")


    return x

def print_matrix_step(matrix, step_description, output):
    output.insert(tk.END, f"\n{step_description}:\n")
    for row in matrix:
        output.insert(tk.END, f"{[clean_round(x, 6) for x in row]}\n")
    output.insert(tk.END, "\n")

def parse_inputs(entries):
    try:
        a_keys = [key for key in entries if key.startswith("a")]
        b_keys = [key for key in entries if key.startswith("b")]

        rows = len(b_keys)
        cols = max(int(key[2:]) for key in a_keys) + 1

        A = [[float(entries[f"a{i}{j}"].get()) for j in range(cols)] for i in range(rows)]
        b = [float(entries[f"b{i}"].get()) for i in range(rows)]

        return A, b
    except ValueError:
        messagebox.showerror("Fejl", "Indtast kun tal i felterne.")
        return None, None

def gaussian_elimination(A, b, output, reduced=False):
    """
    Udfører Gaussisk elimination på matrix A og vektor b.
    Understøtter både almindelig række-echelon-form (REF)
    og reduceret form (RREF) afhængigt af 'reduced'-parameteren.

    Viser hvert trin i processen og konkluderer med løsningstype.

    Args:
        A (list of lists): Koefficientmatrix.
        b (list): Resultatvektor.
        output (tk.Text): Tkinter tekstfelt til visning af trinene.
        reduced (bool): Hvis True bruges RREF, ellers kun REF.
    """
    n = len(A)
    m = len(A[0])
    aug = [A[i] + [b[i]] for i in range(n)]

    print_matrix_equation(A, b, output)
    print_matrix_step(aug, "Startmatrix (udvidet)", output)

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

        var_name = f"x{col+1}"

        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
            print_matrix_step(aug, f"Trin {step}: Bytter R{row+1} med R{pivot_row+1} (for at få pivot i {var_name})", output)
            step += 1

        pivot = aug[row][col]
        if abs(pivot - 1.0) > 1e-12:
            factor = clean_round(1 / pivot, 6)
            aug[row] = [x / pivot for x in aug[row]]
            print_matrix_step(aug, f"Trin {step}: Gør pivot til 1 i {var_name} ved at gange R{row+1} med {factor} (1/{clean_round(pivot, 6)})", output)
            step += 1

        if reduced:
            for r in range(n):
                if r != row and abs(aug[r][col]) > 1e-12:
                    factor = aug[r][col]
                    aug[r] = [aug[r][j] - factor * aug[row][j] for j in range(m + 1)]
                    f_str = f"({clean_round(factor, 4)})" if factor < 0 else f"{clean_round(factor, 4)}"
                    print_matrix_step(aug, f"Trin {step}: Eliminer {var_name} i R{r+1} ved: R{r+1} = R{r+1} - {f_str}·R{row+1}", output)
                    step += 1
        else:
            for r in range(row + 1, n):
                if abs(aug[r][col]) > 1e-12:
                    factor = aug[r][col]
                    aug[r] = [aug[r][j] - factor * aug[row][j] for j in range(m + 1)]
                    f_str = f"({clean_round(factor, 4)})" if factor < 0 else f"{clean_round(factor, 4)}"
                    print_matrix_step(aug, f"Trin {step}: Eliminer {var_name} i R{r+1} ved: R{r+1} = R{r+1} - {f_str}·R{row+1}", output)
                    step += 1

        row += 1

    print_matrix_step(aug, "Slutmatrix (REF)" if not reduced else "Slutmatrix (RREF)", output)

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
            x = back_substitution(aug, output)

        for i, val in enumerate(x):
            output.insert(tk.END, f"x{i+1} = {clean_round(val, 4)}\n")

    output.insert(tk.END, "\n---\n© 2025 Fjederik - Mobilepay endelig et spejlæg.\n")

def solve_system(method, entries, output):
    output.delete("1.0", tk.END)
    A, b = parse_inputs(entries)
    if A is None:
        return

    if method.get() == "Row Echelon Form (REF)":
        gaussian_elimination(A, b, output, reduced=False)
    else:
        gaussian_elimination(A, b, output, reduced=True)

def create_gui():
    """
    Opretter og starter hele GUI'en med Tkinter.
    Brugeren kan indtaste et lineært ligningssystem og vælge løsningstype.
    Viser matrixen og trinene for løsningen i et tekstfelt.
    """
    def update_entries():
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        entries.clear()
        try:
            rows = int(row_entry.get())
            cols = int(col_entry.get())
        except ValueError:
            messagebox.showerror("Fejl", "Indtast gyldige tal for rækker og kolonner.")
            return

        for i in range(rows):
            row_frame = tk.Frame(matrix_frame)
            row_frame.pack()
            for j in range(cols):
                key = f"a{i}{j}"
                entries[key] = tk.Entry(row_frame, width=5)
                entries[key].pack(side="left")
                tk.Label(row_frame, text=f" x{j+1}").pack(side="left")
                if j < cols - 1:
                    tk.Label(row_frame, text=" + ").pack(side="left")
            tk.Label(row_frame, text=" = ").pack(side="left")
            b_key = f"b{i}"
            entries[b_key] = tk.Entry(row_frame, width=5)
            entries[b_key].pack(side="left")

    root = tk.Tk()
    root.title("Gaussisk Elimination")
    root.geometry("650x700")    

    entries = {}

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)
    tk.Label(control_frame, text="Antal ligninger (rækker):").pack(side="left")
    row_entry = tk.Entry(control_frame, width=3)
    row_entry.insert(0, "3")
    row_entry.pack(side="left", padx=5)

    tk.Label(control_frame, text="Antal variable (kolonner):").pack(side="left")
    col_entry = tk.Entry(control_frame, width=3)
    col_entry.insert(0, "3")
    col_entry.pack(side="left", padx=5)

    tk.Button(control_frame, text="Opdater matrix", command=update_entries).pack(side="left", padx=10)

    matrix_frame = tk.Frame(root)
    matrix_frame.pack(pady=10)

    method = tk.StringVar(value="Row Echelon Form (REF)")
    tk.Label(root, text="Vælg metode:").pack()
    ttk.OptionMenu(root, method, method.get(), "Row Echelon Form (REF)", "Reduced Row Echelon Form (RREF)").pack()

    output = tk.Text(root, height=25, width=80)
    output.pack(pady=10)

    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Beregn", command=lambda: solve_system(method, entries, output)).pack(side="left", padx=5)
    
    
    copy_frame = tk.Frame(root)
    copy_frame.pack(pady=5)
    
    tk.Button(copy_frame, text="LaTeX Format 📐", command=lambda: copy_latex_format(output), bg="lightgreen", width=20).pack(pady=5)

    footer = tk.Label(root, text="© 2025 Fjederik - Mobilepay endelig et spejlæg.", font=("Arial", 8), fg="gray")
    footer.pack(pady=(0, 10))

    
    update_entries()

    root.mainloop()

def copy_latex_format(text_widget):
    """
    Creates clean LaTeX with proper matrix equations, steps and results for Word's equation editor.
    """
    try:
        content = text_widget.get("1.0", tk.END)
        
        latex_output = ""
        lines = content.split('\n')
        
        i = 0
        found_matrix_equation = False
        
        while i < len(lines):
            line = lines[i]
            
            
            if 'Matrixform' in line and 'A·x = b' in line:
                
                latex_output += f"\\text{{{line.strip()}}}\n"
                
                i += 1
                
                
                A_matrix, b_vector, var_count = parse_displayed_matrix_equation(lines, i)
                if A_matrix and b_vector:
                    latex_output += create_proper_matrix_equation_latex(A_matrix, b_vector, var_count) + "\n"
                    found_matrix_equation = True
                
                
                while i < len(lines) and (line.strip() == "" or ("[" in line and "]" in line and "=" in line)):
                    i += 1
                continue
            
            
            elif line.strip().startswith('Trin') or 'Startmatrix' in line or 'Slutmatrix' in line:
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                continue
            
            
            elif '[' in line and any(char.isdigit() or char in '.-' for char in line) and ',' in line:
                matrix_rows = []
                j = i
                while j < len(lines) and '[' in lines[j] and ',' in lines[j]:
                    matrix_rows.append(lines[j])
                    j += 1
                
                if len(matrix_rows) > 1:
                    latex_output += create_augmented_matrix_latex(matrix_rows) + "\n"
                    i = j
                    continue
            
            
            elif line.strip().startswith('x') and '=' in line:
                solution = line.strip().replace('x', 'x_')
                latex_output += f"{solution}\n"
                i += 1
                continue
            
            
            elif line.strip().startswith('Systemet har'):
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                continue
            
            i += 1
        
        
        latex_output = latex_output.strip()
        
        pyperclip.copy(latex_output)
        messagebox.showinfo("LaTeX Kopieret! 📐", 
                          "Komplet LaTeX med korrekte matrix ligninger kopieret!\n\n" +
                          "Indsæt i Word's equation editor.")
        
    except Exception as e:
        messagebox.showerror("Fejl", f"LaTeX fejl: {str(e)}")

def parse_displayed_matrix_equation(lines, start_idx):
    """
    Parses the displayed matrix equation format to extract A, x, and b components.
    Handles row-by-row format: [A_row] [x_i] = [b_i]
    """
    A_matrix = []
    b_vector = []
    var_count = 0
    
    i = start_idx
    
    
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    
    
    while i < len(lines):
        line = lines[i]
        
        
        if '[' in line and ']' in line and '=' in line and any(char.isdigit() or char in '.-' for char in line):
            parts = line.split('=')
            if len(parts) == 2:
                left_part = parts[0].strip()
                right_part = parts[1].strip()
                
                
                a_start = left_part.find('[')
                a_end = left_part.find(']', a_start)
                if a_start != -1 and a_end != -1:
                    a_content = left_part[a_start+1:a_end].strip()
                    try:
                        a_row = [float(x) for x in a_content.split()]
                        A_matrix.append(a_row)
                        
                        if var_count == 0:
                            var_count = len(a_row)
                    except ValueError:
                        break
                
                
                b_start = right_part.find('[')
                b_end = right_part.find(']', b_start)
                if b_start != -1 and b_end != -1:
                    b_content = right_part[b_start+1:b_end].strip()
                    if b_content and b_content != '?':  
                        try:
                            b_value = float(b_content)
                            b_vector.append(b_value)
                        except ValueError:
                            pass
        else:
            break
        
        i += 1
    
    return A_matrix, b_vector, var_count

def create_proper_matrix_equation_latex(A_matrix, b_vector, var_count):
    """
    Creates the matrix equation [A] × [x] = [b] with proper formatting.
    """
    
    A_latex = create_matrix_latex_content(A_matrix)
    
    
    
    num_variables = len(A_matrix[0]) if A_matrix else var_count
    x_latex_rows = []
    for i in range(num_variables):
        x_latex_rows.append(f"x_{{{i+1}}}")
    x_matrix_content = " \\\\ ".join(x_latex_rows) + " \\\\"  
    x_latex = f"\\matrix{{{x_matrix_content}}}"
    
    
    b_latex_rows = []
    for b in b_vector:
        if isinstance(b, float) and b.is_integer():
            b_latex_rows.append(str(int(b)))
        elif '.' in str(b) and str(b).endswith('.0'):
            b_latex_rows.append(str(b)[:-2])
        else:
            rounded_b = round(float(b), 4)
            if rounded_b == int(rounded_b):
                b_latex_rows.append(str(int(rounded_b)))
            else:
                b_latex_rows.append(str(rounded_b))
    b_matrix_content = " \\\\ ".join(b_latex_rows) + " \\\\"  
    b_latex = f"\\matrix{{{b_matrix_content}}}"
    
    
    equation = f"\\left[{A_latex}\\right] \\times \\left[{x_latex}\\right] = \\left[{b_latex}\\right]"
    
    return equation

def create_augmented_matrix_latex(matrix_rows):
    """
    Creates LaTeX for augmented matrices without \vline (Word doesn't support it).
    """
    if not matrix_rows:
        return ""
    
    
    parsed_rows = []
    for row in matrix_rows:
        
        row_clean = row.replace('[', '').replace(']', '').replace(',', '')
        numbers = row_clean.split()
        parsed_rows.append(numbers)
    
    if not parsed_rows:
        return ""
    
    
    latex_rows = []
    for row in parsed_rows:
        
        formatted_nums = []
        for num in row:
            if '.' in str(num) and str(num).endswith('.0'):
                formatted_nums.append(str(num)[:-2])
            else:
                formatted_nums.append(str(num))
        
        
        row_str = " & ".join(formatted_nums)
        latex_rows.append(row_str)
    
    
    matrix_content = " \\\\ ".join(latex_rows)
    
    return f"\\left[\\matrix{{{matrix_content}}}\\right]"

def create_matrix_latex_content(matrix_data):
    """
    Creates matrix content using Word's LaTeX syntax.
    """
    latex_rows = []
    for row in matrix_data:
        
        formatted_nums = []
        for num in row:
            if isinstance(num, float) and num.is_integer():
                formatted_nums.append(str(int(num)))
            elif '.' in str(num) and str(num).endswith('.0'):
                formatted_nums.append(str(num)[:-2])
            else:
                
                rounded_num = round(float(num), 4)
                if rounded_num == int(rounded_num):
                    formatted_nums.append(str(int(rounded_num)))
                else:
                    formatted_nums.append(str(rounded_num))
        
        row_str = " & ".join(formatted_nums)
        latex_rows.append(row_str)
    
    
    matrix_content = " \\\\ ".join(latex_rows) + " \\\\"
    
    return f"\\matrix{{{matrix_content}}}"

if __name__ == "__main__":
    create_gui()
