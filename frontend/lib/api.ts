const API_BASE_URL =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export async function getEvents() {
  const response = await fetch(`${API_BASE_URL}/events/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch events");
  }

  return response.json();
}

export async function getAlerts() {
  const response = await fetch(`${API_BASE_URL}/alerts/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch alerts");
  }

  return response.json();
}

export async function getCases() {
  const response = await fetch(`${API_BASE_URL}/cases/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch cases");
  }

  return response.json();
}

export async function runDetections() {
  const response = await fetch(`${API_BASE_URL}/alerts/run`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to run detections");
  }

  return response.json();
}

export async function buildCases() {
  const response = await fetch(`${API_BASE_URL}/cases/build`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to build cases");
  }

  return response.json();
}