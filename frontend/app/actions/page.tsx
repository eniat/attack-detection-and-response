"use client";

import { useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ActionsPage() {
  const [message, setMessage] = useState("");

  async function runDetections() {
    const response = await fetch(`${API_BASE_URL}/alerts/run`, {
      method: "POST"
    });

    const result = await response.json();

    setMessage(`${result.message}. Alerts created: ${result.alerts_created}`);
  }

  async function buildCases() {
    const response = await fetch(`${API_BASE_URL}/cases/build`, {
      method: "POST",
    });

    const result = await response.json();

    setMessage(`${result.message}. Cases created: ${result.cases_created}`);
  }

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold">Detection Actions</h1>

      <div className="flex gap-4">
        <button
          onClick={runDetections}
          className="rounded bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500"
        >
          Run Detections
        </button>

        <button
          onClick={buildCases}
          className="rounded bg-purple-600 px-4 py-2 font-semibold hover:bg-purple-500"
        >
          Build Cases
        </button>
      </div>

      {message && <p className="mt-4 text-slate-300">{message}</p>}
    </div>
  );
}