#!/usr/bin/env python3
"""Gaussisk Elimination Calculator – prototype"""
import tkinter as tk
from tkinter import ttk, messagebox

def clean_round(v, n=4):
    r = round(v, n)
    return 0.0 if abs(r) < 1e-12 else r

def gaussian_elimination(A, b, output, reduced=False):
    n = len(A)
    m = len(A[0])
    aug = [A[i] + [b[i]] for i in range(n)]

    output.insert(tk.END, "Startmatrix:\n")
    for i, row in enumerate(aug):
        output.insert(tk.END, f"  R{i+1}: " + "  ".join(f"{clean_round(x,4):>8}" for x in row) + "\n")
    output.insert(tk.END, "\n")

    row = 0
    for col in range(m):
        pr = None
        for r in range(row, n):
            if abs(aug[r][col]) > 1e-12:
                pr = r
                break
        if pr is None:
            continue
        if pr != row:
            aug[row], aug[pr] = aug[pr], aug[row]
        pivot = aug[row][col]
        if abs(pivot - 1.0) > 1e-12:
            aug[row] = [x / pivot for x in aug[row]]
        rng = range(n) if reduced else range(row + 1, n)
        for r in rng:
            if r != row and abs(aug[r][col]) > 1e-12:
                f = aug[r][col]
                aug[r] = [aug[r][j] - f * aug[row][j] for j in range(m + 1)]
        row += 1

    output.insert(tk.END, "Slutmatrix:\n")
    for i, row in enumerate(aug):
        output.insert(tk.END, f"  R{i+1}: " + "  ".join(f"{clean_round(x,4):>8}" for x in row) + "\n")
    output.insert(tk.END, "\n")

    rank = sum(any(abs(c) > 1e-12 for c in r[:-1]) for r in aug)
    ar = sum(any(abs(c) > 1e-12 for c in r) for r in aug)
    if ar > rank:
        output.insert(tk.END, "Ingen løsning.\n")
    elif rank < m:
        output.insert(tk.END, "Uendeligt mange løsninger.\n")
    else:
        x = [0]*m
        for i in range(n-1,-1,-1):
            x[i] = aug[i][-1] - sum(aug[i][j]*x[j] for j in range(i+1,m))
        for i,v in enumerate(x):
            output.insert(tk.END, f"x{i+1} = {clean_round(v,4)}\n")

root = tk.Tk()
root.title("Gaussisk Elimination")
entries = {}

def update():
    for w in mf.winfo_children(): w.destroy()
    entries.clear()
    rows = int(re.get()); cols = int(ce.get())
    for i in range(rows):
        for j in range(cols):
            e = ttk.Entry(mf, width=5); e.grid(row=i,column=j,padx=2,pady=2)
            entries[f"a{i}{j}"] = e
        ttk.Label(mf,text="=").grid(row=i,column=cols)
        be = ttk.Entry(mf,width=5); be.grid(row=i,column=cols+1,padx=2,pady=2)
        entries[f"b{i}"] = be

def solve():
    output.delete("1.0",tk.END)
    try:
        rows=int(re.get()); cols=int(ce.get())
        A=[[float(entries[f"a{i}{j}"].get()) for j in range(cols)] for i in range(rows)]
        b=[float(entries[f"b{i}"].get()) for i in range(rows)]
    except:
        messagebox.showerror("Fejl","Indtast kun tal."); return
    gaussian_elimination(A,b,output,reduced=mv.get()=="RREF")

lf = ttk.Frame(root); lf.grid(row=0,column=0,padx=10,pady=10,sticky="n")
ttk.Label(lf,text="Rækker:").pack()
re = ttk.Entry(lf,width=3); re.insert(0,"3"); re.pack()
ttk.Label(lf,text="Kolonner:").pack()
ce = ttk.Entry(lf,width=3); ce.insert(0,"3"); ce.pack()
mv = tk.StringVar(value="REF")
ttk.Radiobutton(lf,text="REF",variable=mv,value="REF").pack()
ttk.Radiobutton(lf,text="RREF",variable=mv,value="RREF").pack()
ttk.Button(lf,text="Opdater",command=update).pack(pady=5)
mf = ttk.Frame(lf); mf.pack()
ttk.Button(lf,text="Beregn",command=solve).pack(pady=10)
rf = ttk.Frame(root); rf.grid(row=0,column=1,padx=10,pady=10)
output = tk.Text(rf,height=25,width=50,font=("Consolas",10)); output.pack()
update()
root.mainloop()
