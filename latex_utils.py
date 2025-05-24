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
        
        while i < len(lines):
            line = lines[i]
            
            # Tjek for matrixligning
            if 'Matrixform' in line and 'A·x = b' in line:
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                
                # Fortolk den viste matrixligning
                A_matrix, b_vector, var_count = parse_displayed_matrix_equation(lines, i)
                if A_matrix and b_vector:
                    latex_output += create_proper_matrix_equation_latex(A_matrix, b_vector, var_count) + "\n"
                    found_matrix_equation = True
                
                # Spring over matrixligningens linjer
                while i < len(lines) and (line.strip() == "" or ("[" in line and "]" in line and "=" in line)):
                    i += 1
                continue
            
            # Tjek for trinbeskrivelser
            elif line.strip().startswith('Trin') or 'Startmatrix' in line or 'Slutmatrix' in line:
                latex_output += f"\\text{{{line.strip()}}}\n"
                i += 1
                continue
            
            # Tjek for matrixdata
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
            
            # Tjek for løsningsvariable
            elif line.strip().startswith('x') and '=' in line:
                solution = line.strip().replace('x', 'x_')
                latex_output += f"{solution}\n"
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

def parse_displayed_matrix_equation(lines, start_idx):
    """
    Fortolker den viste matrixligningsformat for at udtrække A, x og b komponenter.
    Håndterer række-for-række format: [A_række] [x_i] = [b_i]
    """
    A_matrix = []
    b_vector = []
    var_count = 0
    
    i = start_idx
    
    # Spring over tomme linjer
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    
    # Fortolk matrixligningens linjer
    while i < len(lines):
        line = lines[i]
        
        # Kig efter linjer med matrixformat: [A] [x] = [b]
        if '[' in line and ']' in line and '=' in line and any(char.isdigit() or char in '.-' for char in line):
            parts = line.split('=')
            if len(parts) == 2:
                left_part = parts[0].strip()
                right_part = parts[1].strip()
                
                # Udtræk A matrix række
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
                
                # Udtræk b vektor element
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
    Opretter matrixligningen [A] × [x] = [b] med korrekt formatering.
    """
    # Opret A matrix LaTeX
    A_latex = create_matrix_latex_content(A_matrix)
    
    # Opret x vektor LaTeX
    num_variables = len(A_matrix[0]) if A_matrix else var_count
    x_latex_rows = []
    for i in range(num_variables):
        x_latex_rows.append(f"x_{{{i+1}}}")
    x_matrix_content = " \\\\ ".join(x_latex_rows) + " \\\\"  
    x_latex = f"\\matrix{{{x_matrix_content}}}"
    
    # Opret b vektor LaTeX
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
    
    # Kombiner til ligning
    equation = f"\\left[{A_latex}\\right] \\times \\left[{x_latex}\\right] = \\left[{b_latex}\\right]"
    
    return equation

def create_augmented_matrix_latex(matrix_rows):
    """
    Opretter LaTeX for udvidede matricer uden \\vline (Word understøtter det ikke).
    """
    if not matrix_rows:
        return ""
    
    # Fortolk matrixrækkerne
    parsed_rows = []
    for row in matrix_rows:
        # Remove brackets and commas
        row_clean = row.replace('[', '').replace(']', '').replace(',', '')
        numbers = row_clean.split()
        parsed_rows.append(numbers)
    
    if not parsed_rows:
        return ""
    
    # Opret LaTeX format
    latex_rows = []
    for row in parsed_rows:
        # Formater tal
        formatted_nums = []
        for num in row:
            if '.' in str(num) and str(num).endswith('.0'):
                formatted_nums.append(str(num)[:-2])
            else:
                formatted_nums.append(str(num))
        
        # Sammenføj med &
        row_str = " & ".join(formatted_nums)
        latex_rows.append(row_str)
    
    # Kombiner rækker
    matrix_content = " \\\\ ".join(latex_rows)
    
    return f"\\left[\\matrix{{{matrix_content}}}\\right]"

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
        
        row_str = " & ".join(formatted_nums)
        latex_rows.append(row_str)
    
    # Kombiner med korrekt matrixformatering
    matrix_content = " \\\\ ".join(latex_rows) + " \\\\"
    
    return f"\\matrix{{{matrix_content}}}"
