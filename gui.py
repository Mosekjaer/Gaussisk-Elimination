import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_inputs
from math_operations import gaussian_elimination
from latex_utils import copy_latex_format
from equation_parser import parse_raw_equations

def solve_system(method, entries, output, input_mode, raw_equations_text=None, var_names_entry=None):
    """
    Løser ligningssystemet baseret på den valgte metode og input type.
    """
    output.delete("1.0", tk.END)
    
    if input_mode.get() == "matrix":
        A, b = parse_inputs(entries)
        if A is None:
            messagebox.showerror("Fejl", "Indtast kun tal i felterne.")
            return
        
        # Parse variabel navne fra entry
        if var_names_entry:
            var_names = [name.strip() for name in var_names_entry.get().split(',')]
            if len(var_names) != len(A[0]):
                messagebox.showerror("Fejl", f"Antal variable ({len(var_names)}) matcher ikke antal kolonner ({len(A[0])}).")
                return
        else:
            var_names = [f"x{i+1}" for i in range(len(A[0]))]
    else:  # raw_equations
        equations = raw_equations_text.get("1.0", tk.END).strip().split('\n')
        equations = [eq.strip() for eq in equations if eq.strip()]
        if not equations:
            messagebox.showerror("Fejl", "Indtast mindst én ligning.")
            return
        try:
            A, b, var_names = parse_raw_equations(equations, output)
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke parse ligningerne: {str(e)}")
            return

    if method.get() == "Row Echelon Form (REF)":
        gaussian_elimination(A, b, output, reduced=False, var_names=var_names)
    else:
        gaussian_elimination(A, b, output, reduced=True, var_names=var_names)

def create_gui():
    """
    Opretter og starter hele GUI'en med Tkinter.
    """
    class MatrixRow:
        def __init__(self, parent, cols, var_names_var):
            self.frame = tk.Frame(parent)
            self.entries = []
            self.labels = []
            
            for j in range(cols):
                entry = tk.Entry(self.frame, width=5)
                entry.pack(side="left")
                self.entries.append(entry)
                
                # Create dynamic label that updates with var_names_var
                label_text = tk.StringVar()
                label = tk.Label(self.frame, textvariable=label_text)
                label.pack(side="left")
                self.labels.append(label_text)
                
                if j < cols - 1:
                    tk.Label(self.frame, text=" + ").pack(side="left")
            
            tk.Label(self.frame, text=" = ").pack(side="left")
            self.b_entry = tk.Entry(self.frame, width=5)
            self.b_entry.pack(side="left")
            
            # Update function for this row
            def update_labels(*args):
                var_names = [name.strip() for name in var_names_var.get().split(',')]
                if len(var_names) != cols:
                    var_names = [f"x{i+1}" for i in range(cols)]
                for i, label_var in enumerate(self.labels):
                    if i < len(var_names):
                        label_var.set(" " + var_names[i])
            
            # Bind to changes in var_names_var
            var_names_var.trace_add("write", update_labels)
            update_labels()  # Initial update
            
            self.frame.pack()

    def update_entries():
        """
        Opdaterer input felterne baseret på antal rækker og kolonner.
        """
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        entries.clear()

        try:
            rows = int(row_entry.get())
            cols = int(col_entry.get())
        except ValueError:
            messagebox.showerror("Fejl", "Indtast gyldige tal for rækker og kolonner.")
            return

        # Variabel navne entry med StringVar
        var_names_frame = tk.Frame(matrix_frame)
        var_names_frame.pack(pady=(0, 10))
        tk.Label(var_names_frame, text="Variable (kommasepareret):").pack(side="left")
        
        var_names_var = tk.StringVar()
        var_names_entry = tk.Entry(var_names_frame, width=40, textvariable=var_names_var)
        default_vars = ", ".join(f"x{i+1}" for i in range(cols))
        var_names_var.set(default_vars)
        var_names_entry.pack(side="left", padx=5)
        
        entries["var_names"] = var_names_var
        matrix_rows = []
        
        # Create matrix rows
        for i in range(rows):
            matrix_row = MatrixRow(matrix_frame, cols, var_names_var)
            matrix_rows.append(matrix_row)
            
            # Gem entries i et entries dictionary
            for j, entry in enumerate(matrix_row.entries):
                entries[f"a{i}{j}"] = entry
            entries[f"b{i}"] = matrix_row.b_entry

    def toggle_input_mode(*args):
        # Skjul begge input områder først
        matrix_control_frame.pack_forget()
        matrix_frame.pack_forget()
        raw_equations_frame.pack_forget()
        
        # Vis det valgte input område
        if input_mode.get() == "matrix":
            matrix_control_frame.pack(after=method_frame)
            matrix_frame.pack(after=matrix_control_frame)
        else:
            raw_equations_frame.pack(after=method_frame)

    # Opret hovedvindue
    root = tk.Tk()
    root.title("Gaussisk Elimination")
    root.geometry("650x700")    

    entries = {}

    # Input type vælger
    input_mode = tk.StringVar(value="matrix")
    input_frame = tk.Frame(root)
    input_frame.pack(pady=5)
    tk.Label(input_frame, text="Input type:").pack(side="left")
    ttk.Radiobutton(input_frame, text="Matrix", variable=input_mode, value="matrix").pack(side="left")
    ttk.Radiobutton(input_frame, text="Rå ligninger", variable=input_mode, value="raw").pack(side="left")
    input_mode.trace("w", toggle_input_mode)

    # Metodevælger
    method_frame = tk.Frame(root)
    method_frame.pack(pady=5)
    method = tk.StringVar(value="Row Echelon Form (REF)")
    tk.Label(method_frame, text="Vælg metode:").pack()
    ttk.OptionMenu(method_frame, method, method.get(), 
                  "Row Echelon Form (REF)", 
                  "Reduced Row Echelon Form (RREF)").pack()

    # Matrix input kontrol
    matrix_control_frame = tk.Frame(root)
    tk.Label(matrix_control_frame, text="Antal ligninger (rækker):").pack(side="left")
    row_entry = tk.Entry(matrix_control_frame, width=3)
    row_entry.insert(0, "3")
    row_entry.pack(side="left", padx=5)

    tk.Label(matrix_control_frame, text="Antal variable (kolonner):").pack(side="left")
    col_entry = tk.Entry(matrix_control_frame, width=3)
    col_entry.insert(0, "3")
    col_entry.pack(side="left", padx=5)

    tk.Button(matrix_control_frame, text="Opdater matrix", command=update_entries).pack(side="left", padx=10)

    # Matrix input område
    matrix_frame = tk.Frame(root)

    # Rå ligninger input område
    raw_equations_frame = tk.Frame(root)
    tk.Label(raw_equations_frame, text="Indtast ligninger (én per linje), f.eks.:").pack()
    tk.Label(raw_equations_frame, text="3x + 2y = 5").pack()
    tk.Label(raw_equations_frame, text="y - z = 3").pack()
    raw_equations_text = tk.Text(raw_equations_frame, height=10, width=40)
    raw_equations_text.pack(pady=5)

    # Output tekstfelt
    output = tk.Text(root, height=25, width=80)
    output.pack(pady=10)

    # Knapper
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Beregn", 
              command=lambda: solve_system(method, entries, output, input_mode, 
                                         raw_equations_text, 
                                         entries.get("var_names"))).pack(side="left", padx=5)
    
    # LaTeX kopierings knap
    copy_frame = tk.Frame(root)
    copy_frame.pack(pady=5)
    
    tk.Button(copy_frame, text="LaTeX Format 📐",
              command=lambda: copy_latex_format(output), 
              bg="lightgreen", width=20).pack(pady=5)

    # Footer
    footer = tk.Label(root, text="© 2025 Fjederik - Mobilepay endelig et spejlæg.", 
                     font=("Arial", 8), fg="gray")
    footer.pack(pady=(0, 10))

    # Initialiser med standard matrix
    update_entries()
    toggle_input_mode()

    # Start GUI
    root.mainloop() 