export default function SeverityBadge({ severity }: { severity: string }) {
  return (
    <span className="rounded bg-slate-700 px-2 py-1 text-xs font-semibold">
      {severity}
    </span>
  );
}