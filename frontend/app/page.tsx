import Link from "next/link";

export default function HomePage() {
  return (
    <div>
      <section className="mb-10">
        <h1 className="mb-4 text-4xl font-bold">
          Cloud Identity Detection and Response
        </h1>

        <p className="max-w-4xl text-slate-300">
          A portfolio security platform for ingesting Microsoft Entra ID and
          Microsoft 365 style logs, detecting identity-based attacks, mapping
          alerts to MITRE ATT&CK, and generating analyst-ready investigation
          cases.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/upload"
            className="rounded bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500"
          >
            Upload CSV Logs
          </Link>

          <Link
            href="/events"
            className="rounded bg-slate-800 px-4 py-2 font-semibold hover:bg-slate-700"
          >
            View Event Batches
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-5">
          <h2 className="mb-2 text-lg font-semibold">1. Upload</h2>
          <p className="text-sm text-slate-400">
            Import synthetic identity and audit logs as separate upload batches,
            preserving the original CSV filename, batch UUID, and event count.
          </p>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900 p-5">
          <h2 className="mb-2 text-lg font-semibold">2. Detect</h2>
          <p className="text-sm text-slate-400">
            Run batch-specific detections for password spraying, brute force,
            impossible travel, MFA fatigue, OAuth consent abuse, and mailbox
            forwarding activity.
          </p>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900 p-5">
          <h2 className="mb-2 text-lg font-semibold">3. Investigate</h2>
          <p className="text-sm text-slate-400">
            Review generated alerts and cases, update case status, add analyst
            comments, and track response actions for each upload batch.
          </p>
        </div>
      </section>

      <section className="mt-8 rounded-lg border border-slate-800 bg-slate-900 p-5">
        <h2 className="mb-3 text-xl font-semibold">Detection Coverage</h2>

        <div className="grid gap-3 text-sm text-slate-300 md:grid-cols-2 lg:grid-cols-3">
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            Password spraying
          </div>
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            Brute force attempts
          </div>
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            Impossible travel
          </div>
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            MFA fatigue
          </div>
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            OAuth consent abuse
          </div>
          <div className="rounded border border-slate-800 bg-slate-950 p-3">
            Mailbox forwarding abuse
          </div>
        </div>
      </section>
    </div>
  );
}