"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import {
  buildCasesForBatch,
  runDetectionsForBatch
} from "@/lib/api";

type BatchActionsProps = {
  batchUuid: string;
};

export default function BatchActions({ batchUuid }: BatchActionsProps) {
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRunDetections() {
    setLoading(true);
    setMessage("");

    try {
      const result = await runDetectionsForBatch(batchUuid);
      setMessage(`${result.message}. Alerts created: ${result.alerts_created}`);
      router.refresh();
    } catch {
      setMessage("Failed to run detections for this upload.");
    } finally {
      setLoading(false);
    }
  }

  async function handleBuildCases() {
    setLoading(true);
    setMessage("");

    try {
      const result = await buildCasesForBatch(batchUuid);
      setMessage(`${result.message}. Cases created: ${result.cases_created}`);
      router.refresh();
    } catch {
      setMessage("Failed to build cases for this upload.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900 p-4">
      <div className="flex flex-wrap gap-3">
        <button
          onClick={handleRunDetections}
          disabled={loading}
          className="rounded bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          Run Detections for This Upload
        </button>

        <button
          onClick={handleBuildCases}
          disabled={loading}
          className="rounded bg-purple-600 px-4 py-2 font-semibold hover:bg-purple-500 disabled:opacity-50"
        >
          Build Cases for This Upload
        </button>
      </div>

      {message && <p className="mt-4 text-sm text-slate-300">{message}</p>}
    </div>
  );
}