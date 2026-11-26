const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

async function request(path, options = {}) {
  if (!API_BASE_URL) {
    throw new Error("Backend not connected. Set VITE_API_BASE_URL in your Vercel project settings.");
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch {
    throw new Error("Could not reach the backend. Check the API URL, backend status, and CORS settings.");
  }

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || payload.message || `Request failed (${response.status}).`);
  }
  return payload;
}

export const isBackendConfigured = Boolean(API_BASE_URL);

export async function uploadReport(file) {
  const form = new FormData();
  form.append("file", file);
  return request("/api/upload", { method: "POST", body: form });
}

export async function askQuestion(documentId, question) {
  return request("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id: documentId, question })
  });
}

export async function generateSummary(documentId) {
  return request("/api/summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id: documentId })
  });
}