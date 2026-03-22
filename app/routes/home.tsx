import { useState, useCallback } from "react";
import type { Route } from "./+types/home";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import { MatrixInput } from "~/components/matrix-input";
import { EquationInput } from "~/components/equation-input";
import { ResultDisplay } from "~/components/result-display";
import {
  gaussianElimination,
  type GaussianResult,
} from "~/lib/gaussian-elimination";
import { parseRawEquations } from "~/lib/equation-parser";
import { generateLatex } from "~/lib/latex-formatter";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Gaussisk Elimination" },
    {
      name: "description",
      content: "Løs lineære ligningssystemer med Gaussisk elimination - REF og RREF metoder",
    },
  ];
}

function createEmptyMatrix(rows: number, cols: number): number[][] {
  return Array.from({ length: rows }, () => new Array(cols).fill(0));
}

function createEmptyVector(rows: number): number[] {
  return new Array(rows).fill(0);
}

export default function Home() {
  const [rows, setRows] = useState(3);
  const [cols, setCols] = useState(3);
  const [method, setMethod] = useState<"ref" | "rref">("ref");
  const [inputMode, setInputMode] = useState<"matrix" | "raw">("matrix");
  const [varNamesStr, setVarNamesStr] = useState("x1, x2, x3");
  const [matrix, setMatrix] = useState<number[][]>(createEmptyMatrix(3, 3));
  const [bVector, setBVector] = useState<number[]>(createEmptyVector(3));
  const [rawEquations, setRawEquations] = useState("");
  const [result, setResult] = useState<GaussianResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [latexCopied, setLatexCopied] = useState(false);

  const varNames = varNamesStr
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  const updateDimensions = useCallback(
    (newRows: number, newCols: number) => {
      setRows(newRows);
      setCols(newCols);
      const newMatrix = createEmptyMatrix(newRows, newCols);
      for (let i = 0; i < Math.min(newRows, matrix.length); i++) {
        for (let j = 0; j < Math.min(newCols, matrix[i]?.length ?? 0); j++) {
          newMatrix[i][j] = matrix[i][j];
        }
      }
      setMatrix(newMatrix);
      const newB = createEmptyVector(newRows);
      for (let i = 0; i < Math.min(newRows, bVector.length); i++) {
        newB[i] = bVector[i];
      }
      setBVector(newB);
      const defaultNames = Array.from({ length: cols }, (_, i) => `x${i + 1}`).join(", ");
      if (varNamesStr === defaultNames || varNames.length !== newCols) {
        setVarNamesStr(Array.from({ length: newCols }, (_, i) => `x${i + 1}`).join(", "));
      }
    },
    [matrix, bVector, cols, varNamesStr, varNames.length]
  );

  const handleMatrixChange = useCallback(
    (row: number, col: number, value: number) => {
      setMatrix((prev) => {
        const next = prev.map((r) => [...r]);
        next[row][col] = value;
        return next;
      });
    },
    []
  );

  const handleBChange = useCallback((row: number, value: number) => {
    setBVector((prev) => {
      const next = [...prev];
      next[row] = value;
      return next;
    });
  }, []);

  const handleSolve = useCallback(() => {
    setError(null);
    try {
      let A: number[];
      let b: number[];
      let names: string[];

      if (inputMode === "matrix") {
        A = matrix.map((r) => [...r]) as any;
        b = [...bVector];
        names =
          varNames.length === cols
            ? [...varNames]
            : Array.from({ length: cols }, (_, i) => `x${i + 1}`);
      } else {
        const equations = rawEquations
          .split("\n")
          .map((s) => s.trim())
          .filter((s) => s && !s.startsWith("#"));
        if (equations.length === 0) {
          setError("Indtast mindst én ligning.");
          return;
        }
        const parsed = parseRawEquations(equations);
        A = parsed.A as any;
        b = parsed.b;
        names = parsed.varNames;
      }

      const res = gaussianElimination(A as any, b, names, method === "rref");
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ukendt fejl");
      setResult(null);
    }
  }, [inputMode, matrix, bVector, varNames, cols, rawEquations, method]);

  const handleCopyLatex = useCallback(() => {
    if (!result) return;
    const latex = generateLatex(result);
    navigator.clipboard.writeText(latex).then(() => {
      setLatexCopied(true);
      setTimeout(() => setLatexCopied(false), 2000);
    });
  }, [result]);

  return (
    <div className="min-h-screen bg-[#fafbfc]">
      {/* Header */}
      <header className="bg-white border-b border-slate-200/80 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
              <span className="text-white text-sm font-bold">G</span>
            </div>
            <div>
              <h1 className="text-base font-semibold text-slate-900 leading-tight">
                Gaussisk Elimination
              </h1>
              <p className="text-[11px] text-slate-400 leading-tight hidden sm:block">
                LMEK &middot; Aarhus Universitet
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-5">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left panel */}
          <div className="lg:col-span-4 space-y-4">
            {/* Method */}
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setMethod("ref")}
                className={`group relative rounded-lg border p-3 text-left transition-all ${
                  method === "ref"
                    ? "bg-white border-blue-300 shadow-sm shadow-blue-100/50"
                    : "bg-white/60 border-slate-200 hover:bg-white hover:border-slate-300"
                }`}
              >
                <div className={`text-xs font-bold tracking-wide ${method === "ref" ? "text-blue-600" : "text-slate-400"}`}>
                  REF
                </div>
                <div className="text-[10px] text-slate-400 mt-0.5 leading-tight">
                  Row Echelon Form
                </div>
                {method === "ref" && (
                  <div className="absolute top-2 right-2 h-2 w-2 rounded-full bg-blue-500" />
                )}
              </button>
              <button
                onClick={() => setMethod("rref")}
                className={`group relative rounded-lg border p-3 text-left transition-all ${
                  method === "rref"
                    ? "bg-white border-blue-300 shadow-sm shadow-blue-100/50"
                    : "bg-white/60 border-slate-200 hover:bg-white hover:border-slate-300"
                }`}
              >
                <div className={`text-xs font-bold tracking-wide ${method === "rref" ? "text-blue-600" : "text-slate-400"}`}>
                  RREF
                </div>
                <div className="text-[10px] text-slate-400 mt-0.5 leading-tight">
                  Reduced Row Echelon
                </div>
                {method === "rref" && (
                  <div className="absolute top-2 right-2 h-2 w-2 rounded-full bg-blue-500" />
                )}
              </button>
            </div>

            {/* Input card */}
            <div className="bg-white rounded-lg border border-slate-200 shadow-sm">
              <Tabs
                value={inputMode}
                onValueChange={(v) => setInputMode(v as "matrix" | "raw")}
              >
                <div className="px-3 pt-2.5 pb-0">
                  <TabsList className="bg-slate-100/80 h-8 w-full">
                    <TabsTrigger
                      value="matrix"
                      className="flex-1 text-xs data-[state=active]:bg-white data-[state=active]:shadow-sm"
                    >
                      Matrix
                    </TabsTrigger>
                    <TabsTrigger
                      value="raw"
                      className="flex-1 text-xs data-[state=active]:bg-white data-[state=active]:shadow-sm"
                    >
                      Ligninger
                    </TabsTrigger>
                  </TabsList>
                </div>

                <TabsContent value="matrix" className="px-3 pb-3 pt-3 space-y-3 mt-0">
                  <div className="flex items-center gap-2 text-sm">
                    <Label className="text-[11px] text-slate-400 uppercase tracking-wider font-medium">Dim</Label>
                    <Input
                      type="number"
                      min={1}
                      max={10}
                      className="w-12 h-7 text-center text-xs px-1"
                      value={rows}
                      onChange={(e) => {
                        const v = parseInt(e.target.value);
                        if (v > 0 && v <= 10) updateDimensions(v, cols);
                      }}
                    />
                    <span className="text-slate-300 text-xs">&times;</span>
                    <Input
                      type="number"
                      min={1}
                      max={10}
                      className="w-12 h-7 text-center text-xs px-1"
                      value={cols}
                      onChange={(e) => {
                        const v = parseInt(e.target.value);
                        if (v > 0 && v <= 10) updateDimensions(rows, v);
                      }}
                    />
                    <div className="flex-1" />
                    <Input
                      value={varNamesStr}
                      onChange={(e) => setVarNamesStr(e.target.value)}
                      placeholder="x, y, z"
                      className="w-28 h-7 text-xs"
                    />
                  </div>

                  <MatrixInput
                    rows={rows}
                    cols={cols}
                    varNames={
                      varNames.length === cols
                        ? varNames
                        : Array.from({ length: cols }, (_, i) => `x${i + 1}`)
                    }
                    matrix={matrix}
                    bVector={bVector}
                    onMatrixChange={handleMatrixChange}
                    onBChange={handleBChange}
                  />
                </TabsContent>

                <TabsContent value="raw" className="px-3 pb-3 pt-3 mt-0">
                  <EquationInput value={rawEquations} onChange={setRawEquations} />
                </TabsContent>
              </Tabs>
            </div>

            {/* Buttons */}
            <div className="flex gap-2">
              <Button
                onClick={handleSolve}
                className="flex-1 h-9 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-sm shadow-blue-200/50"
              >
                Beregn
              </Button>
              <Button
                variant="outline"
                onClick={handleCopyLatex}
                disabled={!result}
                className="h-9 px-3 text-xs rounded-lg"
              >
                {latexCopied ? "Kopieret!" : "Kopier LaTeX"}
              </Button>
            </div>
          </div>

          {/* Right panel — Results */}
          <div className="lg:col-span-8">
            <div className="bg-white rounded-lg border border-slate-200 shadow-sm flex flex-col min-h-[400px] lg:max-h-[calc(100vh-130px)]">
              <div className="px-5 py-3 border-b border-slate-100 flex items-center justify-between flex-shrink-0">
                <h2 className="text-sm font-semibold text-slate-700">Resultater</h2>
                {result && (
                  <span className="text-[10px] text-slate-400 uppercase tracking-wider font-medium">
                    {method === "ref" ? "REF" : "RREF"} &middot; {result.steps.length} trin
                  </span>
                )}
              </div>
              <div className="p-5 overflow-y-auto flex-1">
                {error && (
                  <div className="bg-red-50 text-red-600 rounded-lg p-3 mb-4 text-sm border border-red-100">
                    {error}
                  </div>
                )}
                <ResultDisplay result={result} />
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="py-6">
        <p className="text-center text-[11px] text-slate-300">
          &copy; 2025 Fjederik &middot; Mobilepay endelig et spejl&aelig;g
        </p>
      </footer>
    </div>
  );
}
