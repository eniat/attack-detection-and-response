import Link from "next/link";

import { getBatches } from "@/lib/api";
import { UploadBatch } from "@/lib/types";

export default async function EventsPage() {
  let batches: UploadBatch[] = [];

  try {
    batches = await getBatches();
  } catch {
    batches = [];
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Events</h1>

      <p className="mb-6 text-slate-400">
        Uploaded CSV batches are shown below. Open a batch to view its events.
      </p>

      {batches.length === 0 ? (
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-6 text-slate-400">
          No uploaded event batches found.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {batches.map((batch) => (
            <Link
              key={batch.upload_batch_uuid}
              href={`/events/${batch.upload_batch_uuid}`}
              className="block rounded-lg border border-slate-800 bg-slate-900 p-5 hover:border-blue-500"
            >
              <div className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
                Event Batch
              </div>

              <h2 className="mb-2 text-lg font-semibold text-slate-100">
                {batch.filename}
              </h2>

              <p className="mb-2 text-sm text-slate-400">
                Events: {batch.event_count}
              </p>

              <p className="mb-2 break-all text-xs text-slate-500">
                Batch UUID: {batch.upload_batch_uuid}
              </p>

              <p className="text-xs text-slate-500">
                Uploaded: {batch.created_at}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}