"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function EventUploadControls() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  async function handleUpload() {
    if (!file) {
      setMessage("Select a CSV file first.");
      return;
    }

    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (!response.ok) {
        setMessage(result.detail || "Upload failed.");
        return;
      }

      setMessage(`Uploaded ${result.events_imported} events.`);
      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      router.refresh();
    } catch {
      setMessage("Upload failed.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="flex flex-col items-end justify-start gap-2">
      <div className="flex flex-wrap gap-3">
        <input
          ref={fileInputRef}
          id="csv-upload"
          type="file"
          accept=".csv"
          className="hidden"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />

        <label
          htmlFor="csv-upload"
          className="cursor-pointer rounded bg-slate-700 px-4 py-2 text-sm font-semibold hover:bg-slate-600"
        >
          Choose CSV
        </label>

        <button
          onClick={handleUpload}
          disabled={uploading}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>

      <div className="text-right text-xs text-slate-400">
        {file && <p>Selected: {file.name}</p>}
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}