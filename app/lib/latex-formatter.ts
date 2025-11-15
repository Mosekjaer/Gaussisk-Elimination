/**
 * LaTeX formatering til Word's formeleditor
 */

import type { GaussianResult } from "./gaussian-elimination";

function formatNumber(num: number): string {
  const rounded = Math.round(num * 10000) / 10000;
  if (rounded === Math.trunc(rounded)) {
    return Math.trunc(rounded).toString();
  }
  return rounded.toString();
}

function matrixToLatex(matrix: number[][]): string {
  const rows = matrix.map((row) => row.map(formatNumber).join("&"));
  return rows.join("\\\\");
}

export function generateLatex(result: GaussianResult): string {
  const { matrixEquation, steps, solution } = result;
  const { A, b, varNames } = matrixEquation;
  let output = "";

  // Matrix equation A·x = b
  output += "\\text{Matrixform (A·x = b):}\n";

  const aLatex = matrixToLatex(A);
  const xLatex = varNames.join("\\\\") + "\\\\";
  const bLatex = b.map(formatNumber).join("\\\\") + "\\\\";

  output += `\\left[\\matrix{${aLatex}}\\right] \\times \\left[\\matrix{${xLatex}}\\right] = \\left[\\matrix{${bLatex}}\\right]\n`;

  // Steps
  for (const step of steps) {
    output += `\\text{${step.description}:}\n`;
    const augLatex = matrixToLatex(step.matrix);
    output += `\\left[\\matrix{${augLatex}}\\right]\n`;
  }

  // Solution
  if (solution.type === "none") {
    output += "\\text{Systemet har INGEN løsning (inkonsistent).}\n";
  } else if (solution.type === "infinite") {
    output += "\\text{Systemet har UENDELIGT mange løsninger.}\n";
  } else {
    output += "\\text{Systemet har en ENTYDIG løsning:}\n";
    if (solution.backSubstitutionSteps.length > 0) {
      output += "\\text{Baglæns substitution:}\n";
      for (const s of solution.backSubstitutionSteps) {
        output += `\\text{${s}}\n`;
      }
    }
    for (const [name, val] of Object.entries(solution.values)) {
      output += `\\text{${name} = ${formatNumber(val)}}\n`;
    }
  }

  return output.trim();
}
