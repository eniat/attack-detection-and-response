import BatchActions from "@/components/BatchActions";
import MitreBadge from "@/components/MitreBadge";
import SeverityBadge from "@/components/SeverityBadge";
import {
  getAlertsForBatch,
  getBatchEvents,
  getCasesForBatch
} from "@/lib/api";
import { Alert, Case, Event } from "@/lib/types";

type PageProps = {
  params: Promise<{
    batchUuid: string;
  }>;
};

export default async function EventBatchPage({ params }: PageProps) {
  const { batchUuid } = await params;

  let events: Event[] = [];
  let alerts: Alert[] = [];
  let cases: Case[] = [];

  try {
    [events, alerts, cases] = await Promise.all([
      getBatchEvents(batchUuid),
      getAlertsForBatch(batchUuid),
      getCasesForBatch(batchUuid)
    ]);
  } catch {
    events = [];
    alerts = [];
    cases = [];
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Event Batch</h1>

      <p className="mb-6 break-all text-sm text-slate-400">
        Batch ID: {batchUuid}
      </p>

      <BatchActions batchUuid={batchUuid} />

      <section className="mb-8">
        <h2 className="mb-4 text-2xl font-bold">Generated Cases</h2>

        {cases.length === 0 ? (
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-4 text-slate-400">
            No cases generated for this upload.
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {cases.map((caseItem) => (
              <div
                key={caseItem.id}
                className="rounded-lg border border-slate-800 bg-slate-900 p-4"
              >
                <div className="mb-2 flex items-center gap-2">
                  <SeverityBadge severity={caseItem.severity} />
                  <span className="text-sm text-slate-400">
                    {caseItem.status}
                  </span>
                </div>

                <h3 className="mb-2 text-lg font-semibold">
                  {caseItem.title}
                </h3>

                <p className="mb-2 text-sm text-slate-400">
                  Affected user: {caseItem.affected_user}
                </p>

                <p className="text-sm text-slate-300">
                  {caseItem.summary}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="mb-8">
        <h2 className="mb-4 text-2xl font-bold">Generated Alerts</h2>

        <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-900">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 text-slate-400">
                <tr>
                    <th className="p-3">Rule</th>
                    <th className="p-3">Title</th>
                    <th className="p-3">Severity</th>
                    <th className="p-3">User</th>
                    <th className="p-3">MITRE</th>
                </tr>
            </thead>

            <tbody>
              {alerts.map((alert) => (
                <tr key={alert.id} className="border-b border-slate-800">
                  <td className="p-3">{alert.rule_id}</td>
                  <td className="p-3">{alert.title}</td>
                  <td className="p-3">
                    <SeverityBadge severity={alert.severity} />
                  </td>
                  <td className="p-3">{alert.affected_user}</td>
                  <td className="p-3">
                    <MitreBadge
                        techniqueId={alert.mitre_technique_id}
                        techniqueName={alert.mitre_technique_name}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {alerts.length === 0 && (
            <p className="p-4 text-sm text-slate-400">
              No alerts generated for this upload.
            </p>
          )}
        </div>
      </section>

      <section>
        <h2 className="mb-4 text-2xl font-bold">Events</h2>

        <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-900">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 text-slate-400">
              <tr>
                <th className="p-3">Timestamp</th>
                <th className="p-3">User</th>
                <th className="p-3">Type</th>
                <th className="p-3">IP</th>
                <th className="p-3">Country</th>
                <th className="p-3">Status</th>
                <th className="p-3">Operation</th>
              </tr>
            </thead>

            <tbody>
              {events.map((event) => (
                <tr key={event.id} className="border-b border-slate-800">
                  <td className="p-3">{event.timestamp}</td>
                  <td className="p-3">{event.user_principal_name}</td>
                  <td className="p-3">{event.event_type}</td>
                  <td className="p-3">{event.ip_address}</td>
                  <td className="p-3">{event.country}</td>
                  <td className="p-3">{event.status}</td>
                  <td className="p-3">{event.operation}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {events.length === 0 && (
            <p className="p-4 text-sm text-slate-400">
              No events found for this upload.
            </p>
          )}
        </div>
      </section>
    </div>
  );
}