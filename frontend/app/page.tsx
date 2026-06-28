export default function HomePage() {
  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">
        Cloud Identity Detection and Response
      </h1>

      <p className="max-w-3xl text-slate-300">
        This platform ingests Microsoft Entra ID / Microsoft 365 style logs,
        detects suspicious identity activity, maps alerts to MITRE ATT&CK, and
        builds analyst ready investigation cases.
      </p>

      <div className="mt-8 grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <h2 className="font-semibold">1. Upload Logs</h2>
          <p className="mt-2 text-sm text-slate-400">
            Upload authentication and audit events through the FastAPI backend.
          </p>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <h2 className="font-semibold">2. Run Detections</h2>
          <p className="mt-2 text-sm text-slate-400">
            Generate alerts for password spraying, brute force, MFA fatigue,
            impossible travel, OAuth abuse and mailbox forwarding. 
          </p>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <h2 className="font-semibold">3. Investigate Cases</h2>
          <p className="mt-2 text-sm text-slate-400">
            Review grouped alerts, evidence, severity and response actions.
          </p>
        </div>
      </div>
    </div>
  );
}