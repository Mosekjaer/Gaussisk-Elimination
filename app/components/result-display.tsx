import { useState } from "react";
import type { GaussianResult } from "~/lib/gaussian-elimination";

function fmt(val: number): string {
  const rounded = Math.round(val * 10000) / 10000;
  if (Math.abs(rounded) < 1e-12) return "0";
  if (rounded === Math.trunc(rounded)) return Math.trunc(rounded).toString();
  return rounded.toString();
}

function AugmentedMatrix({
  matrix,
  varNames,
  highlightPivots,
}: {
  matrix: number[][];
  varNames: string[];
  highlightPivots?: boolean;
}) {
  const dataCols = matrix[0]?.length ? matrix[0].length - 1 : 0;

  // Find pivot positions
  const pivotCols = new Set<string>();
  if (highlightPivots) {
    matrix.forEach((row, i) => {
      for (let j = 0; j < dataCols; j++) {
        if (Math.abs(row[j] - 1) < 1e-12) {
          const allZeroAboveBelow = matrix.every(
            (r, ri) => ri === i || Math.abs(r[j]) < 1e-12
          );
          if (allZeroAboveBelow || Math.abs(row[j]) > 1e-12) {
            pivotCols.add(`${i}-${j}`);
            break;
          }
        }
        if (Math.abs(row[j]) > 1e-12) break;
      }
    });
  }

  return (
    <div className="overflow-x-auto">
      <table className="text-sm font-mono tabular-nums">
        <thead>
          <tr>
            <th className="w-8" />
            {varNames.slice(0, dataCols).map((name, j) => (
              <th
                key={j}
                className="px-2.5 py-1 text-[10px] font-medium text-slate-400 text-right uppercase tracking-wider"
              >
                {name}
              </th>
            ))}
            <th className="px-2.5 py-1 text-[10px] font-medium text-slate-400 text-right uppercase tracking-wider border-l-2 border-slate-200">
              b
            </th>
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i} className="group">
              <td className="pr-1.5 text-[10px] text-slate-300 text-right align-middle">
                R{i + 1}
              </td>
              {row.slice(0, dataCols).map((val, j) => {
                const isPivot = pivotCols.has(`${i}-${j}`);
                const isZero = Math.abs(val) < 1e-12;
                return (
                  <td
                    key={j}
                    className={`px-2.5 py-1 text-right align-middle ${
                      isPivot
                        ? "text-blue-600 font-semibold"
                        : isZero
                        ? "text-slate-300"
                        : "text-slate-700"
                    }`}
                  >
                    {fmt(val)}
                  </td>
                );
              })}
              <td className="px-2.5 py-1 text-right align-middle text-slate-700 border-l-2 border-slate-200 font-medium">
                {fmt(row[row.length - 1])}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MatrixEquation({
  A,
  b,
  varNames,
}: {
  A: number[][];
  b: number[];
  varNames: string[];
}) {
  return (
    <div className="flex items-center gap-2 overflow-x-auto py-1 text-sm font-mono">
      {/* A */}
      <div className="inline-flex flex-col border border-slate-200 rounded px-1.5 py-0.5 bg-slate-50/50">
        {A.map((row, i) => (
          <div key={i} className="flex gap-2 justify-end">
            {row.map((val, j) => (
              <span key={j} className="w-8 text-right tabular-nums text-slate-700 py-0.5">
                {fmt(val)}
              </span>
            ))}
          </div>
        ))}
      </div>

      <span className="text-slate-400 text-xs">&middot;</span>

      {/* x */}
      <div className="inline-flex flex-col border border-slate-200 rounded px-2 py-0.5 bg-slate-50/50">
        {varNames.map((name, i) => (
          <span key={i} className="text-center text-blue-600 font-medium py-0.5">
            {name}
          </span>
        ))}
      </div>

      <span className="text-slate-400 text-xs">=</span>

      {/* b */}
      <div className="inline-flex flex-col border border-slate-200 rounded px-2 py-0.5 bg-slate-50/50">
        {b.map((val, i) => (
          <span key={i} className="text-right tabular-nums text-slate-700 py-0.5">
            {fmt(val)}
          </span>
        ))}
      </div>
    </div>
  );
}

function StepCard({
  step,
  index,
  isLast,
}: {
  step: { description: string; matrix: number[][]; varNames: string[] };
  index: number;
  isLast: boolean;
}) {
  const isStart = step.description.startsWith("Startmatrix");
  const isEnd = step.description.startsWith("Slutmatrix");

  return (
    <div className={`relative ${!isLast ? "pb-4" : ""}`}>
      {/* Timeline connector */}
      {!isLast && (
        <div className="absolute left-3 top-8 bottom-0 w-px bg-slate-200" />
      )}

      <div className="flex gap-3">
        {/* Step marker */}
        <div
          className={`mt-1 h-6 w-6 rounded-full flex items-center justify-center flex-shrink-0 text-[10px] font-bold ${
            isStart
              ? "bg-slate-100 text-slate-500"
              : isEnd
              ? "bg-blue-100 text-blue-600"
              : "bg-slate-100 text-slate-400"
          }`}
        >
          {isStart ? "S" : isEnd ? "F" : index}
        </div>

        <div className="flex-1 min-w-0">
          <p
            className={`text-xs leading-snug mb-1.5 ${
              isEnd ? "font-semibold text-blue-700" : "text-slate-600"
            }`}
          >
            {step.description}
          </p>
          <div className="bg-slate-50/80 rounded-md border border-slate-100 p-2.5 overflow-x-auto">
            <AugmentedMatrix
              matrix={step.matrix}
              varNames={step.varNames}
              highlightPivots={isEnd}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export function ResultDisplay({ result }: { result: GaussianResult | null }) {
  const [showAllSteps, setShowAllSteps] = useState(false);

  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-3">
        <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center">
          <span className="text-xl text-slate-300">?</span>
        </div>
        <p className="text-sm text-slate-400">Indtast en matrix og tryk Beregn</p>
      </div>
    );
  }

  const { matrixEquation, steps, solution } = result;

  // Show first, last, and optionally middle steps
  const middleSteps = steps.slice(1, -1);
  const visibleMiddle = showAllSteps ? middleSteps : middleSteps.slice(0, 2);
  const hiddenCount = middleSteps.length - visibleMiddle.length;

  return (
    <div className="space-y-6">
      {/* Matrix equation */}
      <div>
        <h3 className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-2">
          Matrixligning
        </h3>
        <MatrixEquation
          A={matrixEquation.A}
          b={matrixEquation.b}
          varNames={matrixEquation.varNames}
        />
      </div>

      {/* Steps */}
      <div>
        <h3 className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-3">
          Elimination
        </h3>

        <div className="space-y-0">
          {/* First step (start matrix) */}
          {steps.length > 0 && (
            <StepCard step={steps[0]} index={0} isLast={steps.length === 1} />
          )}

          {/* Middle steps */}
          {visibleMiddle.map((step, i) => (
            <StepCard
              key={i + 1}
              step={step}
              index={i + 1}
              isLast={false}
            />
          ))}

          {/* Show more button */}
          {hiddenCount > 0 && (
            <div className="relative pb-4">
              <div className="absolute left-3 top-0 bottom-0 w-px bg-slate-200" />
              <div className="flex gap-3">
                <div className="h-6 w-6 flex-shrink-0" />
                <button
                  onClick={() => setShowAllSteps(true)}
                  className="text-xs text-blue-600 hover:text-blue-700 font-medium py-1"
                >
                  Vis {hiddenCount} flere trin...
                </button>
              </div>
            </div>
          )}

          {/* Last step (final matrix) */}
          {steps.length > 1 && (
            <StepCard
              step={steps[steps.length - 1]}
              index={steps.length - 1}
              isLast={true}
            />
          )}
        </div>
      </div>

      {/* Solution */}
      <div>
        <h3 className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-2">
          L&oslash;sning
        </h3>

        {solution.type === "none" && (
          <div className="bg-red-50 border border-red-100 rounded-lg p-3">
            <p className="text-sm font-medium text-red-700">
              Ingen l&oslash;sning &mdash; systemet er inkonsistent
            </p>
          </div>
        )}

        {solution.type === "infinite" && (
          <div className="bg-amber-50 border border-amber-100 rounded-lg p-3">
            <p className="text-sm font-medium text-amber-700">
              Uendeligt mange l&oslash;sninger
            </p>
          </div>
        )}

        {solution.type === "unique" && (
          <div className="space-y-3">
            {/* Back substitution */}
            {solution.backSubstitutionSteps.length > 0 && (
              <div className="bg-slate-50 border border-slate-100 rounded-lg p-3">
                <p className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-2">
                  Bagl&aelig;ns substitution
                </p>
                <div className="space-y-0.5 font-mono text-sm">
                  {solution.backSubstitutionSteps.map((s, i) => (
                    <p key={i} className="text-slate-600 leading-relaxed">{s}</p>
                  ))}
                </div>
              </div>
            )}

            {/* Final answer */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50/50 border border-blue-200/60 rounded-lg p-4">
              <p className="text-[10px] font-medium text-blue-500 uppercase tracking-wider mb-2">
                Entydig l&oslash;sning
              </p>
              <div className="flex flex-wrap gap-x-6 gap-y-1">
                {Object.entries(solution.values).map(([name, val]) => (
                  <div key={name} className="flex items-baseline gap-1.5 font-mono">
                    <span className="text-blue-600 font-semibold text-base">{name}</span>
                    <span className="text-slate-400">=</span>
                    <span className="text-slate-900 font-semibold text-base">{fmt(val)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
