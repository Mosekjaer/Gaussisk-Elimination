import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_inputs
from math_operations import gaussian_elimination
from latex_utils import copy_latex_format
from equation_parser import parse_raw_equations

def create_custom_style():
    """
    Creates a modern custom style for the application
    """
    style = ttk.Style()
    
    # farver
    style.configure(".",
        background="#ffffff",
        foreground="#2c3e50",
        font=("Segoe UI", 10)
    )
    
    # knapper
    style.configure("Accent.TButton",
        padding=(15, 8),
        font=("Segoe UI", 10, "bold")
    )
    
    # secondary knapper
    style.configure("Secondary.TButton",
        padding=(15, 8),
        font=("Segoe UI", 10)
    )
    
    # Vores entry fields
    style.configure("Custom.TEntry",
        padding=8,
        fieldbackground="white",
        relief="solid",
        borderwidth=1
    )
    
    # Configure ramme
    style.configure("Card.TFrame",
        background="#ffffff",
        relief="solid",
        borderwidth=1
    )
    
    # Configure Labels
    style.configure("Header.TLabel",
        font=("Segoe UI", 14, "bold"),
        padding=10,
        background="#ffffff",
        foreground="#2c3e50"
    )
    
    style.configure("Subheader.TLabel",
        font=("Segoe UI", 11, "bold"),
        padding=5,
        background="#ffffff",
        foreground="#34495e"
    )
    
    # Configure Radiobuttons
    style.configure("Custom.TRadiobutton",
        background="#ffffff",
        foreground="#2c3e50",
        padding=8
    )
    
    # Configure Option Menu
    style.configure("TMenubutton",
        padding=8,
        relief="solid",
        borderwidth=1,
        background="#ffffff",
        font=("Segoe UI", 10)
    )

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
        
        if var_names_entry:
            var_names = [name.strip() for name in var_names_entry.get().split(',')]
            if len(var_names) != len(A[0]):
                messagebox.showerror("Fejl", f"Antal variable ({len(var_names)}) matcher ikke antal kolonner ({len(A[0])}).")
                return
        else:
            var_names = [f"x{i+1}" for i in range(len(A[0]))]
    else:
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

class MatrixRow:
    def __init__(self, parent, cols, var_names_entry):
        self.frame = ttk.Frame(parent)
        self.entries = []
        self.labels = []
        self.var_names_entry = var_names_entry  
        self.cols = cols 
        
        for j in range(cols):
            entry = ttk.Entry(self.frame, width=5, style="Custom.TEntry")
            entry.pack(side="left", padx=2)
            self.entries.append(entry)
            
            label_text = tk.StringVar()
            label = ttk.Label(self.frame, textvariable=label_text)
            label.pack(side="left")
            self.labels.append(label_text)
            
            if j < cols - 1:
                ttk.Label(self.frame, text=" + ").pack(side="left")
        
        ttk.Label(self.frame, text=" = ").pack(side="left")
        self.b_entry = ttk.Entry(self.frame, width=5, style="Custom.TEntry")
        self.b_entry.pack(side="left", padx=2)
        
        self.update_labels()  
        self.frame.pack(pady=2)
    
    def update_labels(self, *args):
        """Update the variable labels for this row"""
        var_names = [name.strip() for name in self.var_names_entry.get().split(',')]
        if len(var_names) != self.cols:
            var_names = [f"x{i+1}" for i in range(self.cols)]
        for i, label_var in enumerate(self.labels):
            if i < len(var_names):
                label_var.set(" " + var_names[i])

def create_gui():
    """
    Opretter og starter hele GUI'en med Tkinter.
    """
    root = tk.Tk()
    root.title("Gaussisk Elimination")
    root.configure(bg="#ffffff")
    
    # Lav custom styling
    create_custom_style()
    
    # Lav vinduet responsive
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    # Main container ramme med increased spacing
    left_panel = ttk.Frame(root, style="Card.TFrame")
    left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
    
    right_panel = ttk.Frame(root, style="Card.TFrame")
    right_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
    
    entries = {}
    matrix_rows = []  

    def update_all_labels(*args):
        """Update variable labels in all matrix rows"""
        for row in matrix_rows:
            row.update_labels()

    def update_entries(*args):
        """
        Opdaterer input felterne baseret på antal rækker og kolonner.
        """
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        entries.clear()
        matrix_rows.clear() 

        try:
            rows = int(row_entry.get())
            cols = int(col_entry.get())
        except ValueError:
            messagebox.showerror("Fejl", "Indtast gyldige tal for rækker og kolonner.")
            return

        # Vi tager nuværende variabel navne fra entry
        var_names = [name.strip() for name in var_names_entry.get().split(',')]
        if len(var_names) != cols:
            var_names = [f"x{i+1}" for i in range(cols)]
            var_names_entry.delete(0, tk.END)
            var_names_entry.insert(0, ", ".join(var_names))
        
        entries["var_names"] = var_names_entry
        
        # lav matrice rows
        for i in range(rows):
            matrix_row = MatrixRow(matrix_frame, cols, var_names_entry)
            matrix_rows.append(matrix_row)
            
            for j, entry in enumerate(matrix_row.entries):
                entries[f"a{i}{j}"] = entry
            entries[f"b{i}"] = matrix_row.b_entry

    def toggle_input_mode(*args):
        """
        Switches between matrix input and raw equations input modes
        """
        matrix_control_frame.pack_forget()
        matrix_frame.pack_forget()
        var_names_frame.pack_forget()
        raw_equations_frame.pack_forget()
        
        if input_mode.get() == "matrix":
            matrix_control_frame.pack(fill="x", padx=15, pady=5)
            var_names_frame.pack(fill="x", padx=15, pady=5)
            matrix_frame.pack(fill="both", expand=True, padx=15, pady=5)
        else:
            raw_equations_frame.pack(fill="both", expand=True, padx=15, pady=5)
            raw_equations_text.delete(1.0, tk.END)
            raw_equations_text.insert(tk.END, "# Eksempel:\n3x + 2y = 5\ny - z = 3")

    # Venstre Panel Content
    ttk.Label(left_panel, text="Input Settings", style="Header.TLabel").pack(fill="x")
    
    input_frame = ttk.Frame(left_panel)
    input_frame.pack(fill="x", padx=15, pady=10)
    ttk.Label(input_frame, text="Input Type", style="Subheader.TLabel").pack(fill="x", pady=(0,5))
    
    radio_frame = ttk.Frame(input_frame)
    radio_frame.pack(fill="x", padx=10, pady=5)
    input_mode = tk.StringVar(value="matrix")
    ttk.Radiobutton(radio_frame, text="Matrix", variable=input_mode, value="matrix", 
                    style="Custom.TRadiobutton").pack(side="left", padx=10)
    ttk.Radiobutton(radio_frame, text="Rå ligninger", variable=input_mode, value="raw", 
                    style="Custom.TRadiobutton").pack(side="left", padx=10)
    
    method_frame = ttk.Frame(left_panel)
    method_frame.pack(fill="x", padx=15, pady=10)
    ttk.Label(method_frame, text="Vælg Metode", style="Subheader.TLabel").pack(fill="x", pady=(0,5))
    method = tk.StringVar(value="Row Echelon Form (REF)")
    method_menu = ttk.OptionMenu(method_frame, method, method.get(),
                               "Row Echelon Form (REF)",
                               "Reduced Row Echelon Form (RREF)")
    method_menu.pack(fill="x", padx=10, pady=5)
    
    matrix_control_frame = ttk.Frame(left_panel)
    matrix_frame = ttk.Frame(left_panel)
    
    ttk.Label(matrix_control_frame, text="Matrix Dimensioner", style="Subheader.TLabel").pack(fill="x", pady=(10,5))
    
    dim_frame = ttk.Frame(matrix_control_frame)
    dim_frame.pack(fill="x", padx=15, pady=10)
    
    row_frame = ttk.Frame(dim_frame)
    row_frame.pack(side="left", padx=5)
    ttk.Label(row_frame, text="Rækker:").pack(side="left")
    row_entry = ttk.Entry(row_frame, width=3, style="Custom.TEntry")
    row_entry.insert(0, "3")
    row_entry.pack(side="left", padx=5)
    
    col_frame = ttk.Frame(dim_frame)
    col_frame.pack(side="left", padx=5)
    ttk.Label(col_frame, text="Kolonner:").pack(side="left")
    col_entry = ttk.Entry(col_frame, width=3, style="Custom.TEntry")
    col_entry.insert(0, "3")
    col_entry.pack(side="left", padx=5)
    
    update_btn = ttk.Button(dim_frame, text="Opdater Matrix", 
                          command=update_entries, 
                          style="Accent.TButton")
    update_btn.pack(side="left", padx=15)
    
    var_names_frame = ttk.Frame(left_panel)
    var_names_frame.pack(fill="x", padx=15, pady=(0,10))
    ttk.Label(var_names_frame, text="Variable (kommasepareret):").pack(side="left")
    var_names_entry = ttk.Entry(var_names_frame, style="Custom.TEntry")
    var_names_entry.pack(side="left", padx=5, fill="x", expand=True)
    var_names_entry.insert(0, "x1, x2, x3") 
    
    var_names_entry.bind('<KeyRelease>', update_all_labels)
    
    raw_equations_frame = ttk.Frame(left_panel)
    ttk.Label(raw_equations_frame, text="Indtast Ligninger", style="Subheader.TLabel").pack(fill="x", pady=(10,5))
    
    raw_equations_text = tk.Text(raw_equations_frame, height=10, width=40,
                               relief="solid", borderwidth=1,
                               font=("Segoe UI", 10))
    raw_equations_text.pack(pady=10, padx=15, fill="both", expand=True)
    
    input_mode.trace_add("write", toggle_input_mode)
    
    ttk.Label(right_panel, text="Resultater", style="Header.TLabel").pack(fill="x")
    
    output_frame = ttk.Frame(right_panel)
    output_frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    scrollbar = ttk.Scrollbar(output_frame)
    scrollbar.pack(side="right", fill="y")
    
    output = tk.Text(output_frame, height=25, width=60, 
                    yscrollcommand=scrollbar.set,
                    font=("Consolas", 10),
                    relief="solid",
                    borderwidth=1,
                    padx=10,
                    pady=10)
    output.pack(fill="both", expand=True)
    scrollbar.config(command=output.yview)
    
    button_frame = ttk.Frame(right_panel)
    button_frame.pack(fill="x", padx=15, pady=10)
    
    calculate_btn = ttk.Button(button_frame, text="Beregn", 
                             command=lambda: solve_system(method, entries, output, input_mode, 
                                                       raw_equations_text, 
                                                       entries.get("var_names")),
                             style="Accent.TButton")
    calculate_btn.pack(side="left", padx=5)
    
    latex_btn = ttk.Button(button_frame, text="LaTeX Format 📐",
                          command=lambda: copy_latex_format(output),
                          style="Secondary.TButton")
    latex_btn.pack(side="left", padx=5)
    
    footer = ttk.Label(right_panel, 
                      text="© 2025 Fjederik - Mobilepay endelig et spejlæg.",
                      font=("Segoe UI", 8),
                      foreground="#6c757d")
    footer.pack(pady=10)
    
    update_entries()
    toggle_input_mode()
    
    root.update()
    root.minsize(1000, 700)
    
    # Start GUI
    root.mainloop() 