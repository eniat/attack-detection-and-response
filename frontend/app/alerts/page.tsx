import MitreBadge from "@/components/MitreBadge";
import SeverityBadge from "@/components/SeverityBadge";
import { getAlerts } from "@/lib/api";
import { Alert } from "@/lib/types";

export default async function AlertsPage() {
  let alerts: Alert[] = [];

  try {
    alerts = await getAlerts();
  } catch {
    alerts = [];
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Alerts</h1>

      <p className="mb-4 text-slate-400">
        Alerts are generated from events and can be investigated. Click on an alert to view its details. 
      </p>

      <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-900">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-800 text-slate-400">
            <tr>
              <th className="p-3">Severity</th>
              <th className="p-3">Rule</th>
              <th className="p-3">Affected User</th>
              <th className="p-3">Source IP</th>
              <th className="p-3">MITRE</th>
              <th className="p-3">Score</th>
            </tr>
          </thead>

          <tbody>
            {alerts.map((alert) => (
              <tr key={alert.id} className="border-b border-slate-800">
                <td className="p-3">
                  <SeverityBadge severity={alert.severity} />
                </td>
                <td className="p-3">{alert.rule_name}</td>
                <td className="p-3">{alert.affected_user}</td>
                <td className="p-3">{alert.source_ip}</td>
                <td className="p-3">
                  <MitreBadge
                    techniqueId={alert.mitre_technique_id}
                    techniqueName={alert.mitre_technique_name}
                  />
                </td>
                <td className="p-3">{alert.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}