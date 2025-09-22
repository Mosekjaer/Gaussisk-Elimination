import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";

interface MatrixInputProps {
  rows: number;
  cols: number;
  varNames: string[];
  matrix: number[][];
  bVector: number[];
  onMatrixChange: (row: number, col: number, value: number) => void;
  onBChange: (row: number, value: number) => void;
}

export function MatrixInput({
  rows,
  cols,
  varNames,
  matrix,
  bVector,
  onMatrixChange,
  onBChange,
}: MatrixInputProps) {
  return (
    <div className="space-y-3">
      {/* Header row with variable names */}
      <div className="flex items-center gap-2">
        <div className="w-8" />
        {varNames.slice(0, cols).map((name, j) => (
          <div key={j} className="w-16 text-center text-sm font-medium text-muted-foreground">
            {name}
          </div>
        ))}
        <div className="w-4" />
        <div className="w-16 text-center text-sm font-medium text-muted-foreground">RHS</div>
      </div>

      {/* Matrix rows */}
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="flex items-center gap-2">
          <Label className="w-8 text-right text-xs text-muted-foreground">R{i + 1}</Label>

          {Array.from({ length: cols }, (_, j) => (
            <Input
              key={j}
              type="number"
              step="any"
              className="w-16 text-center font-mono text-sm"
              value={matrix[i]?.[j] ?? ""}
              onChange={(e) => {
                const val = e.target.value === "" ? 0 : parseFloat(e.target.value);
                onMatrixChange(i, j, isNaN(val) ? 0 : val);
              }}
              placeholder="0"
            />
          ))}

          <span className="text-muted-foreground font-medium">=</span>

          <Input
            type="number"
            step="any"
            className="w-16 text-center font-mono text-sm"
            value={bVector[i] ?? ""}
            onChange={(e) => {
              const val = e.target.value === "" ? 0 : parseFloat(e.target.value);
              onBChange(i, isNaN(val) ? 0 : val);
            }}
            placeholder="0"
          />
        </div>
      ))}
    </div>
  );
}
