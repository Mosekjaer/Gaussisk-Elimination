import pyperclip
from tkinter import messagebox

def copy_latex_format(text_widget):
    try:
        content = text_widget.get("1.0", "end")
        latex_output = ""
        for line in content.split('\n'):
            line = line.strip()
            if not line: continue
            if line.startswith('R') and ':' in line:
                row = line.split(':', 1)[1].strip()
                nums = row.split()
                latex_output += "&".join(nums) + "\\\\\n"
            elif any(kw in line for kw in ['Trin', 'Start', 'Slut', 'System', 'løsning']):
                latex_output += f"\\text{{{line}}}\n"
            elif '=' in line and not 'Matrixform' in line:
                latex_output += f"\\text{{{line}}}\n"
        pyperclip.copy(latex_output.strip())
        messagebox.showinfo("Kopieret", "LaTeX kopieret til udklipsholder!")
    except Exception as e:
        messagebox.showerror("Fejl", f"LaTeX fejl: {str(e)}")
