# LMEK Gaussisk Elimination
*Din (måske) bedste ven til eksamen i Lineær Matematisk Analyse og Elektriske Kredsløb*

## Hvad er det her?

En web-applikation der hjælper dig med at løse lineære ligningssystemer med Gaussisk elimination – uden at du selv skal bøvle med 1'ere, 0'ere og frustrerede brøker.

Lavet til **LMEK-forberedelse (Forår 2025, Aarhus Universitet)**, men virker også udenfor eksamenslokalet.

## Funktioner

- Indtast matrix og højreside
- Tager rå ligninger som input og sætter dem selv på standardform
- Vælg mellem REF og RREF
- Se ALLE udregningstrin
- Valgfrie variabelnavne
- Kopiér LaTeX til Word's formeleditor
- Responsivt design – virker på mobil og desktop

## Tech Stack

- **React Router v7** (Remix)
- **shadcn/ui** + Tailwind CSS
- **TypeScript**
- **Docker** til deployment

## Kør lokalt

```bash
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

Appen kører på `http://localhost:3000`.

## Deploy med Coolify

1. Opret nyt projekt i Coolify
2. Tilslut dit Git repository
3. Vælg "Docker Compose" som build pack
4. Deploy

## Udvikler

**Frederik Pedersen – aka. Fjederik**
*Aarhus Universitet – Forår 2025*
> _MobilePay endelig et spejlæg_
