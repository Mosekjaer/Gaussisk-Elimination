import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_inputs
from math_operations import gaussian_elimination
from latex_utils import copy_latex_format

def solve_system(method, entries, output):
    """
    Løser ligningssystemet baseret på den valgte metode.
    """
    output.delete("1.0", tk.END)
    A, b = parse_inputs(entries)
    if A is None:
        messagebox.showerror("Fejl", "Indtast kun tal i felterne.")
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

    # Opret hovedvindue
    root = tk.Tk()
    root.title("Gaussisk Elimination")
    root.geometry("650x700")    

    entries = {}

    # Kontrolpanel til at definere matrix størrelse
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

    # Område til matrix input
    matrix_frame = tk.Frame(root)
    matrix_frame.pack(pady=10)

    # Metodevælger
    method = tk.StringVar(value="Row Echelon Form (REF)")
    tk.Label(root, text="Vælg metode:").pack()
    ttk.OptionMenu(root, method, method.get(), "Row Echelon Form (REF)", "Reduced Row Echelon Form (RREF)").pack()

    # Output tekstfelt
    output = tk.Text(root, height=25, width=80)
    output.pack(pady=10)

    # Knapper
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Beregn", command=lambda: solve_system(method, entries, output)).pack(side="left", padx=5)
    
    # LaTeX kopierings knap
    copy_frame = tk.Frame(root)
    copy_frame.pack(pady=5)
    
    tk.Button(copy_frame, text="LaTeX Format 📐", command=lambda: copy_latex_format(output), bg="lightgreen", width=20).pack(pady=5)

    # Footer
    footer = tk.Label(root, text="© 2025 Fjederik - Mobilepay endelig et spejlæg.", font=("Arial", 8), fg="gray")
    footer.pack(pady=(0, 10))

    # Initialiser med standard matrix
    update_entries()

    # Start GUI
    root.mainloop() 