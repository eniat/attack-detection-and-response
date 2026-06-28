export default function MitreBadge({
  techniqueId,
  techniqueName,
}: {
  techniqueId: string;
  techniqueName: string;
}) {
  return (
    <span className="rounded bg-slate-800 px-2 py-1 text-xs text-slate-300">
      {techniqueId} - {techniqueName}
    </span>
  );
}