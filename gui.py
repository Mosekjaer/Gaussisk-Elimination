import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_inputs
from math_operations import gaussian_elimination

def create_gui():
    root = tk.Tk()
    root.title("Gaussisk Elimination")
    entries = {}

    def update_entries():
        for w in matrix_frame.winfo_children(): w.destroy()
        entries.clear()
        try:
            rows = int(row_entry.get()); cols = int(col_entry.get())
        except ValueError:
            messagebox.showerror("Fejl", "Indtast gyldige tal."); return
        for i in range(rows):
            for j in range(cols):
                e = ttk.Entry(matrix_frame, width=5)
                e.grid(row=i, column=j, padx=2, pady=2)
                entries[f"a{i}{j}"] = e
            ttk.Label(matrix_frame, text="=").grid(row=i, column=cols)
            be = ttk.Entry(matrix_frame, width=5)
            be.grid(row=i, column=cols+1, padx=2, pady=2)
            entries[f"b{i}"] = be

    def solve():
        output.delete("1.0", tk.END)
        A, b = parse_inputs(entries)
        if A is None:
            messagebox.showerror("Fejl", "Indtast kun tal i felterne."); return
        reduced = method.get() == "RREF"
        gaussian_elimination(A, b, output, reduced=reduced)

    left = ttk.Frame(root)
    left.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    ttk.Label(left, text="Matrix Dimensioner").pack(pady=5)
    dim = ttk.Frame(left); dim.pack()
    ttk.Label(dim, text="Rækker:").pack(side="left")
    row_entry = ttk.Entry(dim, width=3); row_entry.insert(0,"3"); row_entry.pack(side="left",padx=5)
    ttk.Label(dim, text="Kolonner:").pack(side="left")
    col_entry = ttk.Entry(dim, width=3); col_entry.insert(0,"3"); col_entry.pack(side="left",padx=5)

    method = tk.StringVar(value="REF")
    ttk.Radiobutton(left, text="Row Echelon Form (REF)", variable=method, value="REF").pack()
    ttk.Radiobutton(left, text="Reduced Row Echelon Form (RREF)", variable=method, value="RREF").pack()
    ttk.Button(left, text="Opdater Matrix", command=update_entries).pack(pady=5)
    matrix_frame = ttk.Frame(left); matrix_frame.pack()
    ttk.Button(left, text="Beregn", command=solve).pack(pady=10)

    right = ttk.Frame(root)
    right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    sb = ttk.Scrollbar(right); sb.pack(side="right", fill="y")
    output = tk.Text(right, height=25, width=50, font=("Consolas",10), yscrollcommand=sb.set)
    output.pack(fill="both", expand=True)
    sb.config(command=output.yview)

    update_entries()
    root.mainloop()
