"use client";

import Link from "next/link";
import { useState } from "react";

import SeverityBadge from "@/components/SeverityBadge";
import {
  addCaseComment,
  updateCaseStatus
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

      <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900 p-6">
        <div className="mb-4 flex flex-wrap items-center gap-3">
          <SeverityBadge severity={caseItem.severity} />

          <span className="rounded bg-slate-800 px-3 py-1 text-sm text-slate-300">
            Status: {status}
          </span>
        </div>

        <h1 className="mb-4 text-3xl font-bold">{caseItem.title}</h1>

        <div className="grid gap-4 text-sm text-slate-300 md:grid-cols-2">
          <p>
            <span className="font-semibold text-slate-100">Batch ID:</span>{" "}
            <Link
              href={`/events/${caseItem.upload_batch_uuid}`}
              className="break-all text-blue-400 underline hover:text-blue-300"
            >
              {caseItem.upload_batch_uuid}
            </Link>
          </p>

          <p>
            <span className="font-semibold text-slate-100">Score:</span>{" "}
            {caseItem.score}
          </p>

          <p>
            <span className="font-semibold text-slate-100">
              Affected entity:
            </span>{" "}
            {caseItem.affected_user}
          </p>

          <p>
            <span className="font-semibold text-slate-100">
              Related alerts:
            </span>{" "}
            {caseItem.related_alert_ids}
          </p>
        </div>
      </div>

      <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900 p-6">
        <h2 className="mb-3 text-2xl font-bold">Summary</h2>
        <p className="text-slate-300">{caseItem.summary}</p>
      </div>

      <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900 p-6">
        <h2 className="mb-3 text-2xl font-bold">Recommendations</h2>
        <p className="whitespace-pre-line text-slate-300">
          {caseItem.recommendations}
        </p>
      </div>

      <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900 p-6">
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
        <h2 className="mb-4 text-2xl font-bold">Analyst Comments</h2>

        {comments.length === 0 ? (
          <p className="mb-4 text-slate-400">No comments added yet.</p>
        ) : (
          <div className="mb-6 space-y-3">
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
  );
}