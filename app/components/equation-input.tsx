interface EquationInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function EquationInput({ value, onChange }: EquationInputProps) {
  return (
    <div className="space-y-2">
      <p className="text-[11px] text-slate-400">
        Skriv en ligning per linje, f.eks. <code className="text-slate-500 bg-slate-100 px-1 rounded">3x + 2y = 5</code>
      </p>
      <textarea
        className="w-full min-h-[200px] rounded-md border border-slate-200 bg-slate-50 px-3 py-2.5
                   font-mono text-sm leading-relaxed resize-none
                   focus:bg-white focus:border-blue-400 focus:ring-1 focus:ring-blue-100 focus:outline-none
                   placeholder:text-slate-300 transition-colors"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={"3x + 2y = 5\ny - z = 3\n2x + z = 7"}
        spellCheck={false}
      />
    </div>
  );
}
