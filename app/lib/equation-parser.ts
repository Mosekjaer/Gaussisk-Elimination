/**
 * Parser til rå ligninger
 * Konverterer ligninger som "3x + 2y = 5" til matrixform
 */

interface ParseResult {
  A: number[][];
  b: number[];
  varNames: string[];
}

/**
 * Tokenizer: splits an equation side into coefficient-variable pairs
 */
function parseSide(expr: string): { coeffs: Map<string, number>; constant: number } {
  const coeffs = new Map<string, number>();
  let constant = 0;

  // Normalize: remove spaces around +/-, add + before leading negative
  let normalized = expr.replace(/\s+/g, "");

  // Split into terms, keeping the sign
  const terms = normalized.match(/[+-]?[^+-]+/g) || [];

  for (const term of terms) {
    const trimmed = term.trim();
    if (!trimmed) continue;

    // Check if this term has a variable (letter)
    const varMatch = trimmed.match(/^([+-]?\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)$/);
    if (varMatch) {
      let coeffStr = varMatch[1];
      const varName = varMatch[2];

      let coeff: number;
      if (coeffStr === "" || coeffStr === "+") coeff = 1;
      else if (coeffStr === "-") coeff = -1;
      else coeff = parseFloat(coeffStr);

      coeffs.set(varName, (coeffs.get(varName) || 0) + coeff);
    } else {
      // Try variable first (e.g., just "x")
      const pureVar = trimmed.match(/^([+-]?)([a-zA-Z]\w*)$/);
      if (pureVar) {
        const sign = pureVar[1] === "-" ? -1 : 1;
        const varName = pureVar[2];
        coeffs.set(varName, (coeffs.get(varName) || 0) + sign);
      } else {
        // Pure number
        const num = parseFloat(trimmed);
        if (!isNaN(num)) {
          constant += num;
        }
      }
    }
  }

  return { coeffs, constant };
}

export function parseRawEquations(equations: string[]): ParseResult {
  // Filter out comments and empty lines
  const filtered = equations
    .map((eq) => eq.trim())
    .filter((eq) => eq && !eq.startsWith("#"));

  if (filtered.length === 0) {
    throw new Error("Ingen ligninger fundet.");
  }

  // Collect all variable names
  const allVars = new Set<string>();
  const parsedEquations: { lhsCoeffs: Map<string, number>; lhsConst: number; rhsCoeffs: Map<string, number>; rhsConst: number }[] = [];

  for (const eq of filtered) {
    const parts = eq.split("=");
    if (parts.length !== 2) {
      throw new Error(`Ugyldig ligning: "${eq}". Forventet format: "3x + 2y = 5"`);
    }

    const lhs = parseSide(parts[0]);
    const rhs = parseSide(parts[1]);

    for (const v of lhs.coeffs.keys()) allVars.add(v);
    for (const v of rhs.coeffs.keys()) allVars.add(v);

    parsedEquations.push({
      lhsCoeffs: lhs.coeffs,
      lhsConst: lhs.constant,
      rhsCoeffs: rhs.coeffs,
      rhsConst: rhs.constant,
    });
  }

  // Sort variables alphabetically
  const varNames = Array.from(allVars).sort();

  if (varNames.length === 0) {
    throw new Error("Ingen variable fundet i ligningerne.");
  }

  // Build A matrix and b vector
  // For each equation: lhsCoeffs * vars + lhsConst = rhsCoeffs * vars + rhsConst
  // => (lhsCoeffs - rhsCoeffs) * vars = rhsConst - lhsConst
  const A: number[][] = [];
  const b: number[] = [];

  for (const eq of parsedEquations) {
    const row: number[] = [];
    for (const v of varNames) {
      const lc = eq.lhsCoeffs.get(v) || 0;
      const rc = eq.rhsCoeffs.get(v) || 0;
      row.push(lc - rc);
    }
    A.push(row);
    b.push(eq.rhsConst - eq.lhsConst);
  }

  return { A, b, varNames };
}
