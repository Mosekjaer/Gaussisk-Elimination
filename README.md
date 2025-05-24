# Gaussisk Elimination - Matrix Calculator

Et Python program til løsning af lineære ligningssystemer ved hjælp af Gaussisk elimination.

## Features

- **Grafisk brugergrænseflade** med Tkinter
- **Row Echelon Form (REF)** og **Reduced Row Echelon Form (RREF)**
- **Trin-for-trin visning** af eliminationsprocessen
- **Word-optimeret kopiering** med tre forskellige formater
- **Baglæns substitution** for REF metoden

## Installation

1. Sørg for at have Python 3.x installeret
2. Installer nødvendige pakker:
```bash
pip install -r requirements.txt
```

3. Kør programmet:
```bash
python main.py
```

## Sådan bruges programmet

### Grundlæggende brug
1. Indtast antal ligninger (rækker) og variable (kolonner)
2. Klik "Opdater matrix" for at generere input-felter
3. Udfyld koefficienterne og konstanterne
4. Vælg metode (REF eller RREF)
5. Klik "Beregn" for at løse systemet

### Kopiering til Word

Programmet tilbyder **tre forskellige kopieringsformater** optimeret til Microsoft Word:

#### 1. "Kopier til Word" (Lyseblå knap)
- Bruger ⎡ ⎤ ⎢ ⎥ ⎣ ⎦ symboler for rigtige matematiske paranteser
- Automatisk centrering og formatering af matricer
- Monospace tekst for perfekt alignment

**Sådan bruges det i Word:**
1. Klik "Kopier til Word" knappen
2. Indsæt i Word med Ctrl+V
3. Brug "Courier New" skrifttype for bedst resultat
4. Centrer matricerne (Ctrl+E)

#### 2. "RTF Format" (Lysegrøn knap)
- Rich Text Format som Word direkte kan fortolke
- Automatisk fed tekst på overskrifter
- Centrerede ligninger og matricer
- Professionel typografi

**Sådan bruges det i Word:**
1. Klik "RTF Format" knappen
2. Indsæt i Word med Ctrl+V
3. Word genkender automatisk RTF formatering
4. Alternativt: Paste Special > Rich Text Format

#### 3. "Paste Special" (Lysgul knap)
- Kopierer flere formater samtidig
- Giver adgang til Word's Paste Special menu
- Unicode tekst for bedste kompatibilitet

**Sådan bruges det i Word:**
1. Klik "Paste Special" knappen
2. I Word: Tryk Ctrl+Alt+V (Paste Special)
3. Vælg "Unicode Text" for bedste formatering
4. Eller brug almindelig Ctrl+V

## Eksempel

For ligningssystemet:
```
2x₁ + 3x₂ = 7
1x₁ - 1x₂ = 1
```

Programmet viser:
1. Den oprindelige matrix i udvidet form
2. Hver eliminationstrin med forklaring
3. Den finale matrix i REF/RREF form
4. Løsningen ved baglæns substitution (for REF)

**Matricer formateres som:**
```
⎡  2.0   3.0   7.0  ⎤
⎣  1.0  -1.0   1.0  ⎦
```

## Word Formaterings-tips

### For bedste resultater i Word:
- **RTF Format** giver automatisk den bedste formatering
- **Paste Special** giver dig flere valg og kontrol
- **Standard kopier** kræver manuel skrifttype-ændring
- Brug monospace skrifttyper (Courier New, Consolas) for alignment
- Centrer matricerne for professionelt udseende

### Hvis du vil have endnu bedre matematik-notation:
1. Brug RTF formatet først
2. Eller indsæt via Paste Special med Unicode Text
3. For avanceret matematik: Insert > Equation > Matrix i Word
4. Matricer kan kopieres direkte ind i Word's Equation Editor

## Tekniske detaljer

- **Python**: 3.x
- **GUI**: Tkinter
- **Numerisk beregning**: NumPy
- **Clipboard**: pyperclip + pywin32 (Windows)
- **Understøttede formater**: Plain text, Unicode, RTF
- **Matrix symbols**: ⎡ ⎤ ⎢ ⎥ ⎣ ⎦ (Unicode mathematical brackets)

## Fejlfinding

**Problem**: "ModuleNotFoundError: No module named 'pyperclip'"
**Løsning**: Kør `pip install pyperclip`

**Problem**: Kopiering virker ikke
**Løsning**: Sørg for at have en clipboard manager kørende (standard på Windows/Mac)

**Problem**: Formatering ser forkert ud i Word
**Løsning**: Prøv HTML formatet eller konverter til tabel manuelt

## Copyright

© 2025 Fjederik - Mobilepay endelig et spejlæg.