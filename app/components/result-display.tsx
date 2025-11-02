import type { GaussianResult } from "~/lib/gaussian-elimination";
import { Badge } from "~/components/ui/badge";
import { Separator } from "~/components/ui/separator";

function formatNum(val: number): string {
  const rounded = Math.round(val * 10000) / 10000;
  if (Math.abs(rounded) < 1e-12) return "0";
  if (rounded === Math.trunc(rounded)) return Math.trunc(rounded).toString();
  return rounded.toString();
}

function MatrixDisplay({
  matrix,
  varNames,
  showRHS,
}: {
  matrix: number[][];
  varNames: string[];
  showRHS?: boolean;
}) {
  const cols = matrix[0]?.length ?? 0;
  const dataColCount = showRHS !== false ? cols - 1 : cols;

  return (
    <div className="overflow-x-auto">
      <table className="font-mono text-sm">
        <thead>
          <tr>
            <th className="pr-3 text-right text-xs text-muted-foreground" />
            {varNames.slice(0, dataColCount).map((name, j) => (
              <th
                key={j}
                className="px-2 text-center text-xs font-medium text-muted-foreground"
              >
                {name}
              </th>
            ))}
            {showRHS !== false && (
              <th className="px-2 text-center text-xs font-medium text-muted-foreground">
                RHS
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i}>
              <td className="pr-3 text-right text-xs text-muted-foreground">
                R{i + 1}:
              </td>
              {row.map((val, j) => (
                <td
                  key={j}
                  className={`px-2 py-0.5 text-right tabular-nums ${
                    j === dataColCount && showRHS !== false
                      ? "border-l border-border pl-3"
                      : ""
                  }`}
                >
                  {formatNum(val)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MatrixEquationDisplay({
  A,
  b,
  varNames,
}: {
  A: number[][];
  b: number[];
  varNames: string[];
}) {
  return (
    <div className="space-y-1">
      <p className="text-sm font-medium text-muted-foreground mb-2">
        Matrixform (A·x = b):
      </p>
      <div className="flex items-center gap-3 overflow-x-auto py-2">
        {/* A matrix */}
        <div className="border rounded px-2 py-1">
          <table className="font-mono text-sm">
            <tbody>
              {A.map((row, i) => (
                <tr key={i}>
                  {row.map((val, j) => (
                    <td key={j} className="px-2 py-0.5 text-right tabular-nums">
                      {formatNum(val)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <span className="text-muted-foreground font-medium">·</span>

        {/* x vector */}
        <div className="border rounded px-2 py-1">
          <table className="font-mono text-sm">
            <tbody>
              {varNames.map((name, i) => (
                <tr key={i}>
                  <td className="px-2 py-0.5 text-center">{name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <span className="text-muted-foreground font-medium">=</span>

        {/* b vector */}
        <div className="border rounded px-2 py-1">
          <table className="font-mono text-sm">
            <tbody>
              {b.map((val, i) => (
                <tr key={i}>
                  <td className="px-2 py-0.5 text-right tabular-nums">
                    {formatNum(val)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export function ResultDisplay({ result }: { result: GaussianResult | null }) {
  if (!result) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <p>Tryk &quot;Beregn&quot; for at se resultater.</p>
      </div>
    );
  }

  const { matrixEquation, steps, solution } = result;

  return (
    <div className="space-y-4 pb-4">
      {/* Matrix equation */}
      <MatrixEquationDisplay
        A={matrixEquation.A}
        b={matrixEquation.b}
        varNames={matrixEquation.varNames}
      />

      <Separator />

      {/* Steps */}
      {steps.map((step, i) => (
        <div key={i} className="space-y-1">
          <p className="text-sm font-medium">{step.description}:</p>
          <div className="bg-muted/50 rounded-md p-3">
            <MatrixDisplay
              matrix={step.matrix}
              varNames={step.varNames}
              showRHS={true}
            />
          </div>
        </div>
      ))}

      <Separator />

      {/* Solution */}
      <div className="space-y-2">
        {solution.type === "none" && (
          <Badge variant="destructive" className="text-sm">
            Systemet har INGEN l&oslash;sning (inkonsistent)
          </Badge>
        )}
        {solution.type === "infinite" && (
          <Badge variant="secondary" className="text-sm">
            Systemet har UENDELIGT mange l&oslash;sninger
          </Badge>
        )}
        {solution.type === "unique" && (
          <>
            <Badge className="text-sm bg-green-600 hover:bg-green-700">
              Systemet har en ENTYDIG l&oslash;sning
            </Badge>

            {solution.backSubstitutionSteps.length > 0 && (
              <div className="space-y-1 mt-3">
                <p className="text-sm font-medium">Bagl&aelig;ns substitution:</p>
                <div className="bg-muted/50 rounded-md p-3 font-mono text-sm space-y-1">
                  {solution.backSubstitutionSteps.map((s, i) => (
                    <p key={i}>{s}</p>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-3 space-y-1">
              <p className="text-sm font-medium">L&oslash;sning:</p>
              <div className="bg-muted/50 rounded-md p-3 font-mono text-sm space-y-1">
                {Object.entries(solution.values).map(([name, val]) => (
                  <p key={name}>
                    <span className="font-semibold">{name}</span> = {formatNum(val)}
                  </p>
                ))}
              </div>
            </div>
          </>
        )}
      </div>

      <Separator />

      <p className="text-xs text-muted-foreground text-center">
        &copy; 2025 Fjederik - Mobilepay endelig et spejl&aelig;g.
      </p>
    </div>
  );
}
