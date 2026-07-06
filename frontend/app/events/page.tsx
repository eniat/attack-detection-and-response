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
              <div className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
                Event Batch
              </div>

              <h2 className="mb-3 break-words text-xl font-bold text-slate-100">
                {batch.original_filename}
              </h2>

              <p className="mb-3 break-all rounded bg-slate-800 px-3 py-2 text-xs text-slate-400">
                Batch UUID: {batch.upload_batch_uuid}
              </p>

              <div className="space-y-2 text-sm text-slate-400">
                <p>
                  Events: {batch.event_count}
                </p>

                <p>
                  Uploaded: {batch.created_at}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}