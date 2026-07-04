"use client";

import { useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [batchUuid, setBatchUuid] = useState("");

  async function handleUpload() {
    if (!file) {
      setMessage("Select a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload/`, {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (!response.ok) {
      setMessage(result.detail || "Upload failed.");
      return;
    }

    setMessage(`Uploaded ${result.events_imported} events.`);
    setBatchUuid(result.upload_batch_uuid);
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Upload Logs</h1>

      <div className="max-w-xl rounded-lg border border-slate-800 bg-slate-900 p-6">
        <div className="mb-4">
          <input
            id="csv-upload"
            type="file"
            accept=".csv"
            className="hidden"
            onChange={(event) => {
              setFile(event.target.files?.[0] || null);
              setBatchUuid("");
              setMessage("");
            }}
          />

          <label
            htmlFor="csv-upload"
            className="inline-block cursor-pointer rounded bg-slate-700 px-4 py-2 font-semibold hover:bg-slate-600"
          >
            Choose CSV File
          </label>

          {file && (
            <p className="mt-2 text-sm text-slate-400">
              Selected: {file.name}
            </p>
          )}
        </div>

        <button
          onClick={handleUpload}
          className="rounded bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500"
        >
          Upload CSV
        </button>

        {message && <p className="mt-4 text-slate-300">{message}</p>}

        {batchUuid && (
          <a
            href={`/events/${batchUuid}`}
            className="mt-4 inline-block text-blue-400 underline"
          >
            Open uploaded event batch
          </a>
        )}
      </div>
    </div>
  );
}