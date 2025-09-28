import React, { useState } from "react";

// Landing page for Capital One's Credit Center
// - Pick a user from a dropdown
// - Kick off the Python analysis by POSTing to your backend
// - Redirect to /analysis?user=NAME when the job starts
//
// Expected backend endpoint (example):
//   POST /api/run-agent
//   Body: { user: "Kyle", transactionsFile: "synthetic_transactions_kyle.json" }
//   Returns: { started: true }
//
// Replace the endpoint below to match your server. If you prefer query params,
// adjust the fetch() call accordingly.

export default function LandingPage() {
  const [user, setUser] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const USERS = ["Kyle", "Griffin", "Graham", "Emilio"]; // edit as needed

  const COLORS = {
    cobalt: "#004C97", // Capital One blue
    scarlet: "#D0343A", // accent red
    slate: "#1F2937", // dark gray text
    fog: "#F3F4F6", // light gray bg
    white: "#FFFFFF",
  };

  async function handleAnalyze(e) {
    e.preventDefault();
    setError("");

    if (!user) {
      setError("Please select a user.");
      return;
    }

    const fileName = `synthetic_transactions_${user.toLowerCase()}.json`;

    try {
      setIsSubmitting(true);

      const res = await fetch("/api/run-agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, transactionsFile: fileName }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Request failed with ${res.status}`);
      }

      const data = await res.json().catch(() => ({}));
      if (!data.started && !data.ok) {
        throw new Error("Agent did not start. Check server logs.");
      }

      // Navigate to analysis page with the chosen user
      window.location.href = `/analysis?user=${encodeURIComponent(user)}`;
    } catch (err) {
      setError(err?.message || "Something went wrong starting the analysis.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen" style={{ background: COLORS.fog }}>
      {/* Header */}
      <header
        className="w-full shadow-sm"
        style={{ background: COLORS.cobalt }}
      >
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center justify-between">
          <h1 className="text-2xl md:text-3xl font-semibold" style={{ color: COLORS.white }}>
            Welcome to <span className="font-bold">Capital One's Credit Center</span>
          </h1>
          <span
            className="px-3 py-1 rounded-full text-sm font-medium"
            style={{ background: COLORS.white, color: COLORS.cobalt }}
          >
            Mini‑App
          </span>
        </div>
      </header>

      {/* Main Card */}
      <main className="max-w-3xl mx-auto px-6">
        <section className="mt-10">
          <div className="bg-white rounded-2xl shadow-md p-6 md:p-8">
            <h2 className="text-xl md:text-2xl font-semibold mb-2" style={{ color: COLORS.slate }}>
              Analyze a Financial Profile
            </h2>
            <p className="text-sm md:text-base text-gray-600 mb-6">
              Choose a user to evaluate their spending and get personalized card recommendations.
            </p>

            <form onSubmit={handleAnalyze} className="space-y-5">
              <div>
                <label htmlFor="user" className="block text-sm font-medium text-gray-700 mb-2">
                  Select User
                </label>
                <div className="relative">
                  <select
                    id="user"
                    value={user}
                    onChange={(e) => setUser(e.target.value)}
                    className="w-full appearance-none rounded-xl border border-gray-300 bg-white px-4 py-3 pr-10 text-gray-900 focus:outline-none focus:ring-2"
                    style={{ focusRingColor: COLORS.cobalt }}
                    aria-label="Select a user"
                  >
                    <option value="" disabled>
                      — Choose a user —
                    </option>
                    {USERS.map((u) => (
                      <option key={u} value={u}>
                        {u}
                      </option>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 text-gray-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 011.08 1.04l-4.25 4.25a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
              </div>

              {error && (
                <div
                  className="rounded-xl px-4 py-3 text-sm"
                  style={{ background: "#FEF2F2", color: "#991B1B", border: "1px solid #FECACA" }}
                >
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting || !user}
                className="w-full inline-flex items-center justify-center rounded-xl px-5 py-3 font-semibold text-white shadow-sm transition"
                style={{ background: isSubmitting || !user ? "#9CA3AF" : COLORS.scarlet }}
              >
                {isSubmitting ? "Starting…" : "Run Analysis"}
              </button>

              <p className="text-xs text-gray-500">
                This will run <code className="font-mono">agent.py</code> using
                <code className="font-mono"> synthetic_transactions_{"{user}"}.json</code> and
                redirect you to the analysis page.
              </p>
            </form>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-10 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} Capital One — Credit Center (Hackathon Demo)
        </footer>
      </main>
    </div>
  );
}
