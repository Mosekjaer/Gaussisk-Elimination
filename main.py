#!/usr/bin/env python3
"""
Gaussisk Elimination Calculator
© 2025 Fjederik - Mobilepay endelig et spejlæg.

En interaktiv lommeregner til løsning af lineære ligningssystemer
ved hjælp af Gaussisk elimination med REF og RREF metoder.

Usage:
    python main.py

Modules:
    - gui.py: Brugergrænseflade og hovedlogik
    - math_operations.py: Matematiske funktioner (Gaussian elimination, back substitution)
    - latex_utils.py: LaTeX formatering og kopiering til Word
    - utils.py: Hjælpefunktioner til matrix operationer
"""

from gui import create_gui

if __name__ == "__main__":
    create_gui()
