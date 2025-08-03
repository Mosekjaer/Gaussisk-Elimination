/**
 * Gaussisk Elimination algoritme
 * Port fra Python til TypeScript
 */

export interface Step {
  description: string;
  matrix: number[][];
  varNames: string[];
}

export interface Solution {
  type: "unique" | "infinite" | "none";
  values: Record<string, number>;
  backSubstitutionSteps: string[];
}

export interface GaussianResult {
  steps: Step[];
  matrixEquation: {
    A: number[][];
    b: number[];
    varNames: string[];
  };
  solution: Solution;
}

function cleanRound(value: number, ndigits = 4): number {
  const r = Math.round(value * 10 ** ndigits) / 10 ** ndigits;
  return Math.abs(r) < 1e-12 ? 0 : r;
}

function backSubstitution(
  refMatrix: number[][],
  varNames: string[]
): { values: Record<string, number>; steps: string[] } {
  const n = refMatrix.length;
  const m = refMatrix[0].length - 1;
  const x = new Array(m).fill(0);
  const steps: string[] = [];

  for (let i = n - 1; i >= 0; i--) {
    const row = refMatrix[i];
    let pivotCol: number | null = null;
    for (let j = 0; j < m; j++) {
      if (Math.abs(row[j]) > 1e-12) {
        pivotCol = j;
        break;
      }
    }
    if (pivotCol === null) continue;

    const rhs = row[m];
    const coeff = row[pivotCol];

    const symbolTerms: string[] = [];
    const valueTerms: string[] = [];

    for (let j = pivotCol + 1; j < m; j++) {
      const termCoeff = cleanRound(row[j], 4);
      if (Math.abs(termCoeff) > 1e-12) {
        const sign = termCoeff < 0 ? " - " : " + ";
        symbolTerms.push(`${sign}${Math.abs(termCoeff)} \u00b7 ${varNames[j]}`);
        valueTerms.push(`${sign}${Math.abs(termCoeff)} \u00b7 ${cleanRound(x[j], 4)}`);
      }
    }

    const xVal =
      (rhs - row.slice(pivotCol + 1, m).reduce((sum, v, idx) => sum + v * x[pivotCol + 1 + idx], 0)) / coeff;
    x[pivotCol] = xVal;

    const rhsStr = cleanRound(rhs, 4).toString();

    if (Math.abs(coeff - 1.0) < 1e-12) {
      if (symbolTerms.length === 0) {
        steps.push(`${varNames[pivotCol]} = ${cleanRound(xVal, 4)}`);
      } else {
        const exprSymbol = rhsStr + symbolTerms.join("");
        const exprValue = rhsStr + valueTerms.join("");
        if (exprSymbol === exprValue) {
          steps.push(`${varNames[pivotCol]} = ${exprValue} = ${cleanRound(xVal, 4)}`);
        } else {
          steps.push(
            `${varNames[pivotCol]} = ${exprSymbol} = ${exprValue} = ${cleanRound(xVal, 4)}`
          );
        }
      }
    } else {
      if (symbolTerms.length === 0) {
        steps.push(
          `${varNames[pivotCol]} = ${cleanRound(rhs, 4)} / ${cleanRound(coeff, 4)} = ${cleanRound(xVal, 4)}`
        );
      } else {
        const exprSymbol = rhsStr + symbolTerms.join("");
        const exprValue = rhsStr + valueTerms.join("");
        steps.push(
          `${varNames[pivotCol]} = (${exprSymbol}) / ${cleanRound(coeff, 4)} = (${exprValue}) / ${cleanRound(coeff, 4)} = ${cleanRound(xVal, 4)}`
        );
      }
    }
  }

  const values: Record<string, number> = {};
  varNames.forEach((name, i) => {
    if (i < m) values[name] = cleanRound(x[i], 4);
  });

  return { values, steps };
}

export function gaussianElimination(
  A: number[][],
  b: number[],
  varNames: string[],
  reduced = false
): GaussianResult {
  const n = A.length;
  const m = A[0].length;
  const aug = A.map((row, i) => [...row, b[i]]);
  const steps: Step[] = [];

  // Initial augmented matrix
  steps.push({
    description: "Startmatrix (udvidet)",
    matrix: aug.map((r) => [...r]),
    varNames,
  });

  let step = 1;
  let currentRow = 0;

  for (let col = 0; col < m; col++) {
    let pivotRow: number | null = null;
    for (let r = currentRow; r < n; r++) {
      if (Math.abs(aug[r][col]) > 1e-12) {
        pivotRow = r;
        break;
      }
    }

    if (pivotRow === null) continue;

    if (pivotRow !== currentRow) {
      [aug[currentRow], aug[pivotRow]] = [aug[pivotRow], aug[currentRow]];
      steps.push({
        description: `Trin ${step}: Bytter R${currentRow + 1} med R${pivotRow + 1} (for at f\u00e5 pivot i ${varNames[col]})`,
        matrix: aug.map((r) => [...r]),
        varNames,
      });
      step++;
    }

    const pivot = aug[currentRow][col];
    if (Math.abs(pivot - 1.0) > 1e-12) {
      const factor = cleanRound(1 / pivot, 6);
      aug[currentRow] = aug[currentRow].map((x) => x / pivot);
      steps.push({
        description: `Trin ${step}: G\u00f8r pivot til 1 i ${varNames[col]} ved at gange R${currentRow + 1} med ${factor} (1/${cleanRound(pivot, 6)})`,
        matrix: aug.map((r) => [...r]),
        varNames,
      });
      step++;
    }

    if (reduced) {
      for (let r = 0; r < n; r++) {
        if (r !== currentRow && Math.abs(aug[r][col]) > 1e-12) {
          const factor = aug[r][col];
          aug[r] = aug[r].map((val, j) => val - factor * aug[currentRow][j]);
          const fStr = factor < 0 ? `(${cleanRound(factor, 4)})` : `${cleanRound(factor, 4)}`;
          steps.push({
            description: `Trin ${step}: Eliminer ${varNames[col]} i R${r + 1} ved: R${r + 1} = R${r + 1} - ${fStr}\u00b7R${currentRow + 1}`,
            matrix: aug.map((r) => [...r]),
            varNames,
          });
          step++;
        }
      }
    } else {
      for (let r = currentRow + 1; r < n; r++) {
        if (Math.abs(aug[r][col]) > 1e-12) {
          const factor = aug[r][col];
          aug[r] = aug[r].map((val, j) => val - factor * aug[currentRow][j]);
          const fStr = factor < 0 ? `(${cleanRound(factor, 4)})` : `${cleanRound(factor, 4)}`;
          steps.push({
            description: `Trin ${step}: Eliminer ${varNames[col]} i R${r + 1} ved: R${r + 1} = R${r + 1} - ${fStr}\u00b7R${currentRow + 1}`,
            matrix: aug.map((r) => [...r]),
            varNames,
          });
          step++;
        }
      }
    }

    currentRow++;
  }

  // Final matrix
  steps.push({
    description: reduced ? "Slutmatrix (RREF)" : "Slutmatrix (REF)",
    matrix: aug.map((r) => [...r]),
    varNames,
  });

  // Determine solution type
  const rank = aug.filter((row) => row.slice(0, m).some((cell) => Math.abs(cell) > 1e-12)).length;
  const augRank = aug.filter((row) => row.some((cell) => Math.abs(cell) > 1e-12)).length;

  let solution: Solution;

  if (augRank > rank) {
    solution = { type: "none", values: {}, backSubstitutionSteps: [] };
  } else if (rank < m) {
    solution = { type: "infinite", values: {}, backSubstitutionSteps: [] };
  } else {
    if (reduced) {
      const x = new Array(m).fill(0);
      for (let i = 0; i < n; i++) {
        const leadingCol = aug[i].slice(0, m).findIndex((val) => Math.abs(val - 1) < 1e-12);
        if (leadingCol !== -1 && leadingCol < m) {
          x[leadingCol] = aug[i][m];
        }
      }
      const values: Record<string, number> = {};
      varNames.forEach((name, i) => {
        if (i < m) values[name] = cleanRound(x[i], 4);
      });
      solution = { type: "unique", values, backSubstitutionSteps: [] };
    } else {
      const { values, steps: bsSteps } = backSubstitution(aug, varNames);
      solution = { type: "unique", values, backSubstitutionSteps: bsSteps };
    }
  }

  return {
    steps,
    matrixEquation: { A, b, varNames },
    solution,
  };
}
