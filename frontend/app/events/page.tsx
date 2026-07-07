import EventUploadControls from "@/components/EventUploadControls";

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
    <div className="mb-8 flex flex-wrap items-start justify-between gap-6">
      <div className="min-w-0 flex-1">
          <h1 className="text-4xl font-bold">Events</h1>

          <p className="mt-3 text-xl text-slate-400">
            Uploaded CSV batches are shown below. Open a batch to view its events.
          </p>
        </div>

        <div className="flex shrink-0 items-start">
          <EventUploadControls />
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {batches.map((batch) => (
          <a
            key={batch.upload_batch_uuid}
            href={`/events/${batch.upload_batch_uuid}`}
            className="rounded-lg border border-slate-800 bg-slate-900 p-6 hover:bg-slate-800"
          >
            <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
              Event Batch
            </p>

            <h2 className="mt-5 break-words text-2xl font-bold">
              {batch.original_filename}
            </h2>

            <div className="mt-6 rounded bg-slate-800 p-3 text-sm text-slate-400">
              Batch UUID: {batch.upload_batch_uuid}
            </div>

            <p className="mt-5 text-lg text-slate-400">
              Events: {batch.event_count}
            </p>

            <p className="mt-4 text-lg text-slate-400">
              Uploaded: {new Date(batch.created_at).toLocaleString()}
            </p>
          </a>
        ))}
      </div>

      {batches.length === 0 && (
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-4 text-slate-400">
          No uploads found. Choose a CSV file above to create the first event batch.
        </div>
      )}
    </div>
  );
}