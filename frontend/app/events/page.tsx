import { getEvents } from "@/lib/api";
import { Event } from "@/lib/types";

export default async function EventsPage() {
  let events: Event[] = [];

  try {
    events = await getEvents();
  } catch {
    events = [];
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Events</h1>

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
      </div>
    </div>
  );
}