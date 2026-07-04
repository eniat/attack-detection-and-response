import { Alert, Case, CaseComment, Event, UploadBatch } from "./types";

const API_BASE_URL =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...options
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${path}`);
  }

  return response.json();
}

export async function getEvents(): Promise<Event[]> {
  return fetchJson<Event[]>("/events/");
}

export async function getAlerts(): Promise<Alert[]> {
  return fetchJson<Alert[]>("/alerts/");
}

export async function getCases(): Promise<Case[]> {
  return fetchJson<Case[]>("/cases/");
}

export async function getBatches(): Promise<UploadBatch[]> {
  return fetchJson<UploadBatch[]>("/batches/");
}

export async function getBatchEvents(uploadBatchUuid: string): Promise<Event[]> {
  return fetchJson<Event[]>(`/batches/${uploadBatchUuid}/events`);
}

export async function getAlertsForBatch(uploadBatchUuid: string): Promise<Alert[]> {
  return fetchJson<Alert[]>(`/alerts/batch/${uploadBatchUuid}`);
}

export async function getCasesForBatch(uploadBatchUuid: string): Promise<Case[]> {
  return fetchJson<Case[]>(`/cases/by-batch/${uploadBatchUuid}`);
}

export async function getCase(caseId: number): Promise<Case> {
  return fetchJson<Case>(`/cases/${caseId}`);
}

export async function getCaseComments(caseId: number): Promise<CaseComment[]> {
  return fetchJson<CaseComment[]>(`/cases/${caseId}/comments`);
}

export async function runDetections() {
  return fetchJson("/alerts/run", {
    method: "POST"
  });
}

export async function buildCases() {
  return fetchJson("/cases/build", {
    method: "POST"
  });
}

export async function runDetectionsForBatch(uploadBatchUuid: string) {
  return fetchJson(`/alerts/run/${uploadBatchUuid}`, {
    method: "POST"
  });
}

export async function buildCasesForBatch(uploadBatchUuid: string) {
  return fetchJson(`/cases/build/${uploadBatchUuid}`, {
    method: "POST"
  });
}

export async function updateCaseStatus(caseId: number, status: string): Promise<Case> {
  return fetchJson<Case>(`/cases/${caseId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ status })
  });
}

export async function addCaseComment(caseId: number, comment: string): Promise<CaseComment> {
  return fetchJson<CaseComment>(`/cases/${caseId}/comments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ comment })
  });
}