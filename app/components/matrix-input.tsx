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
    <div className="space-y-1.5">
      {/* Header */}
      <div className="flex items-center gap-1">
        <div className="w-6" />
        {varNames.slice(0, cols).map((name, j) => (
          <div
            key={j}
            className="flex-1 text-center text-[10px] font-medium text-slate-400 uppercase tracking-wider"
          >
            {name}
          </div>
        ))}
        <div className="w-3" />
        <div className="flex-1 text-center text-[10px] font-medium text-slate-400 uppercase tracking-wider">
          b
        </div>
      </div>

      {/* Rows */}
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="flex items-center gap-1">
          <span className="w-6 text-right text-[10px] text-slate-300 font-mono tabular-nums">
            {i + 1}
          </span>

          {Array.from({ length: cols }, (_, j) => (
            <input
              key={j}
              type="number"
              step="any"
              className="flex-1 min-w-0 h-8 text-center text-sm font-mono bg-slate-50 border border-slate-200 rounded-md
                         focus:bg-white focus:border-blue-400 focus:ring-1 focus:ring-blue-100 focus:outline-none
                         transition-colors tabular-nums
                         [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              value={matrix[i]?.[j] === 0 ? "" : matrix[i]?.[j] ?? ""}
              onChange={(e) => {
                const val = e.target.value === "" ? 0 : parseFloat(e.target.value);
                onMatrixChange(i, j, isNaN(val) ? 0 : val);
              }}
              placeholder="0"
            />
          ))}

          <div className="w-3 text-center text-slate-300 text-xs">=</div>

          <input
            type="number"
            step="any"
            className="flex-1 min-w-0 h-8 text-center text-sm font-mono bg-blue-50/50 border border-blue-200/60 rounded-md
                       focus:bg-white focus:border-blue-400 focus:ring-1 focus:ring-blue-100 focus:outline-none
                       transition-colors tabular-nums
                       [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
            value={bVector[i] === 0 ? "" : bVector[i] ?? ""}
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
