"use client";

import Link from "next/link";
import { useState } from "react";

import SeverityBadge from "@/components/SeverityBadge";
import {
  addCaseComment,
  updateCaseStatus,
  generateReport
} from "@/lib/api";
import { Case, CaseComment } from "@/lib/types";

type CaseDetailClientProps = {
  caseItem: Case;
  initialComments: CaseComment[];
};

const statusOptions = [
  "open",
  "investigating",
  "contained",
  "false_positive",
  "closed"
];

export default function CaseDetailClient({
  caseItem,initialComments}: CaseDetailClientProps) {
  const [status, setStatus] = useState(caseItem.status);
  const [comments, setComments] = useState(initialComments);
  const [newComment, setNewComment] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [reportMarkdown, setReportMarkdown] = useState("");

  async function handleStatusChange(event: React.ChangeEvent<HTMLSelectElement>) {
    const updatedStatus = event.target.value;

    setLoading(true);
    setMessage("");

    try {
      const updatedCase = await updateCaseStatus(caseItem.id, updatedStatus);
      setStatus(updatedCase.status);
      setMessage("Case status updated.");
    } catch {
      setMessage("Failed to update case status.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAddComment(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!newComment.trim()) {
      setMessage("Enter a comment first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const comment = await addCaseComment(caseItem.id, newComment);
      setComments([...comments, comment]);
      setNewComment("");
      setMessage("Comment added.");
    } catch {
      setMessage("Failed to add comment.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateReport() {
    setLoading(true);
    setMessage("");

    try {
      const report = await generateReport(caseItem.id);
      setReportMarkdown(report.report_markdown);
      setMessage("Report generated.");
    } catch {
      setMessage("Failed to generate report.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="mb-6">
        <Link
          href={`/events/${caseItem.upload_batch_uuid}`}
          className="text-sm text-blue-400 underline hover:text-blue-300"
        >
          Back to event batch
        </Link>
      </div>

      <div className=" rounded-lg border border-slate-800 bg-slate-900 p-6">
        <div className="flex flex-col gap-4 xl:flex-row xl:justify-between">

          <div className="min-w-0">
            <h1 className="text-3xl font-bold">
                {caseItem.title}
            </h1>

            <p className="mt-4 text-sm text-slate-400">
              Batch ID:
            </p>

            <Link
              href={`/events/${caseItem.upload_batch_uuid}`}
              className="break-all text-blue-400 underline"
            >
              {caseItem.upload_batch_uuid}
            </Link>

            <p className="mt-4 text-slate-300">
              <span className="font-semibold">
                Affected entity:
              </span>{" "}
              {caseItem.affected_user}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:w-[480px]">

            <div className="rounded bg-slate-800 p-4">
              <p className="text-xs uppercase text-slate-500">
                Severity
              </p>

              <div className="mt-2">
                <SeverityBadge severity={caseItem.severity}/>
              </div>
            </div>

            <div className="rounded bg-slate-800 p-4">
              <p className="text-xs uppercase text-slate-500">
                Score
              </p>

              <p className="mt-2 text-2xl font-bold">
                {caseItem.score}
              </p>
            </div>

              <div className="rounded bg-slate-800 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Status
                </p>

                <p className="mt-2">
                    {status}
                </p>
              </div>

              <div className="rounded bg-slate-800 p-4">
                <p className="text-xs uppercase text-slate-500">
                    Related Event
                </p>

                <Link
                  href={`/events/${caseItem.upload_batch_uuid}`}
                  className="mt-2 block text-blue-400 underline hover:text-blue-300"
                >
                  View source event
                </Link>
              </div>
          </div>

        </div>
    </div>

    <div className="mt-8 grid gap-6 xl:grid-cols-[minmax(0,1.5fr)_minmax(320px,0.8fr)]">
      <div className="space-y-6">
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
            <h2 className="mb-3 text-2xl font-bold">Summary</h2>
            <p className="text-slate-300">{caseItem.summary}</p>
        </div>

      <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
        <h2 className="mb-3 text-2xl font-bold">Recommendations</h2>
        <ul className="list-disc space-y-2 pl-6 text-slate-300">
          {caseItem.recommendations
            .split("\n")
            .map((recommendation) => recommendation.replace("- ", "").trim())
            .filter(Boolean)
            .map((recommendation) => (
              <li key={recommendation}>{recommendation}</li>
            ))}
        </ul>
      </div>

      <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
        <h2 className="mb-4 text-2xl font-bold">Analyst Comments</h2>

        {comments.length === 0 ? (
          <p className="mb-4 text-slate-400">No comments added yet.</p>
        ) : (
          <div className="space-y-3">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className="rounded border border-slate-800 bg-slate-950 p-4"
              >
                <p className="text-slate-300">{comment.comment}</p>
                <p className="mt-2 text-xs text-slate-500">
                  {comment.created_at}
                </p>
              </div>
            ))}
          </div>
        )}

        <form onSubmit={handleAddComment}>
          <textarea
            value={newComment}
            onChange={(event) => setNewComment(event.target.value)}
            rows={4}
            className="mb-3 w-full rounded border border-slate-700 bg-slate-950 p-3 text-slate-100"
            placeholder="Add analyst comment..."
          />

          <button
            type="submit"
            disabled={loading}
            className="rounded bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500 disabled:opacity-50"
          >
            Add Comment
          </button>
        </form>
      </div>
      </div>

      <div className="space-y-6 xl:border-l xl:border-slate-800 xl:pl-6">

        <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-4 text-2xl font-bold">Update Status</h2>

          <select
            value={status}
            onChange={handleStatusChange}
            disabled={loading}
            className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
          >
            {statusOptions.map((statusOption) => (
              <option key={statusOption} value={statusOption}>
                {statusOption}
              </option>
            ))}
          </select>

          {message && <p className="mt-4 text-sm text-slate-300">{message}</p>}
        </div>


        <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-4 text-2xl font-bold">Case Report</h2>

          <button
            onClick={handleGenerateReport}
            disabled={loading}
            className="rounded bg-emerald-600 px-4 py-2 font-semibold hover:bg-emerald-500 disabled:opacity-50"
          >
            Generate Report
          </button>

          {reportMarkdown && (
            <pre className="mt-4 max-h-[400px] overflow-auto whitespace-pre-wrap rounded border border-slate-800 bg-slate-950 p-4 text-sm text-slate-300">
              {reportMarkdown}
            </pre>
          )}
        </div>


        <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">

          <h2 className="mb-4 text-2xl font-bold">
            Case Information
          </h2>

          <div className="space-y-3 text-sm text-slate-300">

            <p>
              <strong>Case ID:</strong> {caseItem.id}
            </p>

            <p>
              <strong>Upload Batch:</strong>
            </p>

            <p className="break-all">
              {caseItem.upload_batch_uuid}
            </p>

            <p>
              <strong>Current Status:</strong> {status}
            </p>

            <p>
              <strong>Score:</strong> {caseItem.score}
            </p>

            <p>
              <strong>Severity:</strong> {caseItem.severity}
            </p>

          </div>

        </div>

      </div>
    </div>
    </div>
  );
}