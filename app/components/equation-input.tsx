import { Textarea } from "~/components/ui/textarea";

interface EquationInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function EquationInput({ value, onChange }: EquationInputProps) {
  return (
    <div className="space-y-2">
      <p className="text-sm text-muted-foreground">
        Skriv en ligning per linje. Eksempel:
      </p>
      <Textarea
        className="font-mono min-h-[180px] text-sm"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={"3x + 2y = 5\ny - z = 3\n2x + z = 7"}
      />
    </div>
  );
}
