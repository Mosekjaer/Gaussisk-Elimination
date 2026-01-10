import { useState, useCallback } from "react";
import type { Route } from "./+types/home";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";
import { Separator } from "~/components/ui/separator";
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
      content:
        "L\u00f8s line\u00e6re ligningssystemer med Gaussisk elimination - REF og RREF metoder",
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

  const varNames = varNamesStr
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  const updateDimensions = useCallback(
    (newRows: number, newCols: number) => {
      setRows(newRows);
      setCols(newCols);

      // Resize matrix
      const newMatrix = createEmptyMatrix(newRows, newCols);
      for (let i = 0; i < Math.min(newRows, matrix.length); i++) {
        for (let j = 0; j < Math.min(newCols, matrix[i]?.length ?? 0); j++) {
          newMatrix[i][j] = matrix[i][j];
        }
      }
      setMatrix(newMatrix);

      // Resize b vector
      const newB = createEmptyVector(newRows);
      for (let i = 0; i < Math.min(newRows, bVector.length); i++) {
        newB[i] = bVector[i];
      }
      setBVector(newB);

      // Update default var names if they match the default pattern
      const defaultNames = Array.from({ length: cols }, (_, i) => `x${i + 1}`).join(", ");
      if (varNamesStr === defaultNames || varNames.length !== newCols) {
        setVarNamesStr(
          Array.from({ length: newCols }, (_, i) => `x${i + 1}`).join(", ")
        );
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
      let A: number[][];
      let b: number[];
      let names: string[];

      if (inputMode === "matrix") {
        A = matrix.map((r) => [...r]);
        b = [...bVector];

        if (varNames.length !== cols) {
          names = Array.from({ length: cols }, (_, i) => `x${i + 1}`);
        } else {
          names = [...varNames];
        }
      } else {
        const equations = rawEquations
          .split("\n")
          .map((s) => s.trim())
          .filter((s) => s && !s.startsWith("#"));

        if (equations.length === 0) {
          setError("Indtast mindst \u00e9n ligning.");
          return;
        }

        const parsed = parseRawEquations(equations);
        A = parsed.A;
        b = parsed.b;
        names = parsed.varNames;
      }

      const res = gaussianElimination(A, b, names, method === "rref");
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
      alert(
        "LaTeX kopieret!\n\nInds\u00e6t i Word's equation editor."
      );
    });
  }, [result]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold tracking-tight">
            Gaussisk Elimination
          </h1>
          <p className="text-sm text-muted-foreground">
            Din (m&aring;ske) bedste ven til eksamen i Line&aelig;r Matematisk Analyse
            og Elektriske Kredsl&oslash;b
          </p>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left panel - Input */}
          <div className="space-y-4">
            {/* Method selection */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Metode</CardTitle>
              </CardHeader>
              <CardContent>
                <Select
                  value={method}
                  onValueChange={(v) => setMethod(v as "ref" | "rref")}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ref">
                      Row Echelon Form (REF)
                    </SelectItem>
                    <SelectItem value="rref">
                      Reduced Row Echelon Form (RREF)
                    </SelectItem>
                  </SelectContent>
                </Select>
              </CardContent>
            </Card>

            {/* Input mode */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Input</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Tabs
                  value={inputMode}
                  onValueChange={(v) => setInputMode(v as "matrix" | "raw")}
                >
                  <TabsList className="w-full">
                    <TabsTrigger value="matrix" className="flex-1">
                      Matrix
                    </TabsTrigger>
                    <TabsTrigger value="raw" className="flex-1">
                      R&aring; ligninger
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="matrix" className="space-y-4 mt-4">
                    {/* Dimensions */}
                    <div className="flex items-end gap-4">
                      <div className="space-y-1">
                        <Label className="text-xs">R&aelig;kker</Label>
                        <Input
                          type="number"
                          min={1}
                          max={10}
                          className="w-20"
                          value={rows}
                          onChange={(e) => {
                            const v = parseInt(e.target.value);
                            if (v > 0 && v <= 10)
                              updateDimensions(v, cols);
                          }}
                        />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">Kolonner</Label>
                        <Input
                          type="number"
                          min={1}
                          max={10}
                          className="w-20"
                          value={cols}
                          onChange={(e) => {
                            const v = parseInt(e.target.value);
                            if (v > 0 && v <= 10)
                              updateDimensions(rows, v);
                          }}
                        />
                      </div>
                    </div>

                    <Separator />

                    {/* Variable names */}
                    <div className="space-y-1">
                      <Label className="text-xs">
                        Variable (kommasepareret)
                      </Label>
                      <Input
                        value={varNamesStr}
                        onChange={(e) => setVarNamesStr(e.target.value)}
                        placeholder="x1, x2, x3"
                      />
                    </div>

                    <Separator />

                    {/* Matrix input */}
                    <MatrixInput
                      rows={rows}
                      cols={cols}
                      varNames={
                        varNames.length === cols
                          ? varNames
                          : Array.from(
                              { length: cols },
                              (_, i) => `x${i + 1}`
                            )
                      }
                      matrix={matrix}
                      bVector={bVector}
                      onMatrixChange={handleMatrixChange}
                      onBChange={handleBChange}
                    />
                  </TabsContent>

                  <TabsContent value="raw" className="mt-4">
                    <EquationInput
                      value={rawEquations}
                      onChange={setRawEquations}
                    />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Action buttons */}
            <div className="flex gap-3">
              <Button onClick={handleSolve} className="flex-1">
                Beregn
              </Button>
              <Button
                variant="outline"
                onClick={handleCopyLatex}
                disabled={!result}
              >
                LaTeX Format
              </Button>
            </div>
          </div>

          {/* Right panel - Results */}
          <Card className="min-h-[400px] lg:min-h-[500px]">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Resultater</CardTitle>
            </CardHeader>
            <CardContent className="overflow-auto max-h-[calc(100vh-200px)]">
              {error && (
                <div className="bg-destructive/10 text-destructive rounded-md p-3 mb-4 text-sm">
                  {error}
                </div>
              )}
              <ResultDisplay result={result} />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
