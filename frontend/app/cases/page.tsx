import SeverityBadge from "@/components/SeverityBadge";
import { getCases } from "@/lib/api";
import { Case } from "@/lib/types";

export default async function CasesPage() {
  let cases: Case[] = [];

  try {
    cases = await getCases();
  } catch {
    cases = [];
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Cases</h1>

      <p className="mb-4 text-slate-400">
        Build cases from the FastAPI docs using POST /cases/build.
      </p>

      <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-900">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-800 text-slate-400">
            <tr>
              <th className="p-3">Severity</th>
              <th className="p-3">Title</th>
              <th className="p-3">Affected User / Entity</th>
              <th className="p-3">Status</th>
              <th className="p-3">Score</th>
            </tr>
          </thead>

          <tbody>
            {cases.map((caseItem) => (
              <tr key={caseItem.id} className="border-b border-slate-800">
                <td className="p-3">
                  <SeverityBadge severity={caseItem.severity} />
                </td>
                <td className="p-3">{caseItem.title}</td>
                <td className="p-3">{caseItem.affected_user}</td>
                <td className="p-3">{caseItem.status}</td>
                <td className="p-3">{caseItem.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}