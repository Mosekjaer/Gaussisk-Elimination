import pyperclip
from tkinter import messagebox

def copy_latex_format(text_widget):
    """
    Opretter ren LaTeX med korrekte matrixligninger, trin og resultater til Words formeleditor.
    """
    try:
        content = text_widget.get("1.0", "end")
        
        latex_output = ""
        lines = content.split('\n')
        
        i = 0
        found_matrix_equation = False
        var_names = None
        solutions_seen = set()
        
        while i < len(lines):
            line = lines[i]
            
            # Tjek for matrixligning
            if 'Matrixform' in line and 'A·x = b' in line:
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                
                # Find første matrix efter dette
                while i < len(lines) and not lines[i].strip().startswith('R1:'):
                    i += 1
                
                if i < len(lines):
                    matrix_rows = []
                    while i < len(lines) and lines[i].strip().startswith('R'):
                        row = lines[i].strip()
                        if ':' in row:
                            row = row.split(':', 1)[1].strip()
                        matrix_rows.append(row)
                        i += 1
                    
                    if matrix_rows:
                        # del hver row ind i coefficients og RHS
                        A_matrix = []
                        b_vector = []
                        for row in matrix_rows:
                            nums = [float(x) for x in row.split()]
                            A_matrix.append(nums[:-1])  
                            b_vector.append(nums[-1])   
                        
                        # Lav variabel navne
                        var_count = len(A_matrix[0])
                        var_names = ['x', 'y', 'z'][:var_count] 
                        if var_count > 3:
                            var_names.extend([f'x_{i+4}' for i in range(var_count - 3)])
                        
                        # Create matrix equation
                        A_latex = create_matrix_latex_content(A_matrix)
                        
                        # Lav x vector med \\ for sidste variable
                        x_latex_rows = []
                        for var in var_names:
                            x_latex_rows.append(var)
                        x_matrix_content = "\\\\".join(x_latex_rows) + "\\\\"
                        x_latex = f"\\matrix{{{x_matrix_content}}}"
                        
                        # lav b vector med \\ til sidste nummer
                        b_latex_rows = []
                        for b in b_vector:
                            if float(b).is_integer():
                                b_latex_rows.append(str(int(b)))
                            else:
                                b_latex_rows.append(str(float(b)))
                        b_matrix_content = "\\\\".join(b_latex_rows) + "\\\\"
                        b_latex = f"\\matrix{{{b_matrix_content}}}"
                        
                        # fortsæt med ligningen
                        latex_output += f"\\left[\\matrix{{{A_latex}}}\\right] \\times \\left[{x_latex}\\right] = \\left[{b_latex}\\right]\n"
                continue
            
            # Tjek for trinbeskrivelser
            elif line.strip().startswith('Trin') or 'Startmatrix' in line or 'Slutmatrix' in line:
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                
                if i < len(lines) and any(var in lines[i] for var in ['x', 'y', 'z', 'RHS']):
                    i += 1
    
                matrix_rows = []
                while i < len(lines) and lines[i].strip().startswith('R'):
                    row = lines[i].strip()
                    if ':' in row:
                        row = row.split(':', 1)[1].strip()
                    matrix_rows.append(row)
                    i += 1
                
                if matrix_rows:
                    latex_output += create_augmented_matrix_latex(matrix_rows) + "\n"
                continue
            
            # Tjek for løsningsvariable
            elif line.strip() and '=' in line and not line.strip().startswith('Matrixform'):
                solution = line.strip()
                if var_names:
                    # Find hvilket variabelnavn der matcher starten af linjen
                    for var in var_names:
                        if solution.startswith(var + ' ='):
                            # spring over hvis vi allerede har set løsningen
                            if var in solutions_seen:
                                break
                            solutions_seen.add(var)
                            latex_output += f"{solution}\n"
                            break
                i += 1
                continue
            
            # Tjek for systembeskrivelser
            elif line.strip().startswith('Systemet har'):
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                continue
            
            i += 1
        
        # Ryd op i outputtet
        latex_output = latex_output.strip()
        
        pyperclip.copy(latex_output)
        messagebox.showinfo("LaTeX Kopieret! 📐", 
                          "Komplet LaTeX med korrekte matrix ligninger kopieret!\n\n" +
                          "Indsæt i Word's equation editor.")
        
    except Exception as e:
        messagebox.showerror("Fejl", f"LaTeX fejl: {str(e)}")

def create_matrix_latex_content(matrix_data):
    """
    Opretter matrixindhold ved hjælp af Words LaTeX-syntaks.
    """
    latex_rows = []
    for row in matrix_data:
        # Formater tal korrekt
        formatted_nums = []
        for num in row:
            if isinstance(num, float) and num.is_integer():
                formatted_nums.append(str(int(num)))
            elif '.' in str(num) and str(num).endswith('.0'):
                formatted_nums.append(str(num)[:-2])
            else:
                # Round to avoid floating point precision issues
                rounded_num = round(float(num), 4)
                if rounded_num == int(rounded_num):
                    formatted_nums.append(str(int(rounded_num)))
                else:
                    formatted_nums.append(str(rounded_num))
        
        # Join with & between elements
        row_str = "&".join(formatted_nums)
        latex_rows.append(row_str)
    
    # Join with \\ without extra \\ at the end
    return "\\\\".join(latex_rows)

def create_augmented_matrix_latex(matrix_rows):
    """
    Opretter LaTeX for udvidede matricer uden \\vline (Word understøtter det ikke).
    """
    if not matrix_rows:
        return ""
    
    # Fortolk matrixrækkerne
    parsed_rows = []
    for row in matrix_rows:
        # Split on whitespace and filtrer ud tomme strings
        numbers = [x for x in row.split() if x.strip()]
        if numbers:
            parsed_rows.append(numbers)
    
    if not parsed_rows:
        return ""
    
    # Opret LaTeX format
    latex_rows = []
    for row in parsed_rows:
        # Formater tal
        formatted_nums = []
        for num in row:
            try:
                value = float(num)
                if value.is_integer():
                    formatted_nums.append(str(int(value)))
                else:
                    formatted_nums.append(f"{value:.4f}".rstrip('0').rstrip('.'))
            except ValueError:
                formatted_nums.append(num)
        
        # Join with & between elements
        row_str = "&".join(formatted_nums)
        latex_rows.append(row_str)
    
    # Join with \\ without extra \\ at the end
    matrix_content = "\\\\".join(latex_rows)
    
    return f"\\left[\\matrix{{{matrix_content}}}\\right]"
