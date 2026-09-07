"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await login(phone, password);
    setLoading(false);
    if (res.ok) router.push("/");
    else setError(res.error || "Login nahi ho saka.");
  }

  return (
    <div className="w-full max-w-sm bg-white rounded-2xl shadow-card p-8">
      <div className="text-center mb-6">
        <span className="text-3xl">🌱</span>
        <h1 className="text-xl font-semibold text-ink mt-2">Smart Kisan mein Login karein</h1>
        <p className="text-sm text-ink/50 mt-1">Apna phone number aur password darj karein</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="text-sm text-ink/60 block mb-1">Phone Number</label>
          <input
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="03001234567"
            required
            className="w-full bg-cream rounded-lg px-3 py-2.5 text-sm outline-none border border-black/5 focus:border-brand-400"
          />
        </div>
        <div>
          <label className="text-sm text-ink/60 block mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full bg-cream rounded-lg px-3 py-2.5 text-sm outline-none border border-black/5 focus:border-brand-400"
          />
        </div>

        {error && <p className="text-sm text-alert-500">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-brand-600 hover:bg-brand-700 text-white py-2.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
        >
          {loading ? "Login ho raha hai…" : "Login"}
        </button>
      </form>

      <p className="text-center text-sm text-ink/50 mt-5">
        Account nahi hai? <Link href="/signup" className="text-brand-600 font-medium">Signup karein</Link>
      </p>
    </div>
  );
}
