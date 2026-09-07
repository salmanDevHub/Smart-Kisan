"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface User {
  id: number;
  name: string;
  phone: string;
  city?: string | null;
}

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (phone: string, password: string) => Promise<{ ok: boolean; error?: string }>;
  signup: (name: string, phone: string, password: string, city: string) => Promise<{ ok: boolean; error?: string }>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = typeof window !== "undefined" ? localStorage.getItem("sk_token") : null;
    const savedUser = typeof window !== "undefined" ? localStorage.getItem("sk_user") : null;
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  function persist(t: string, u: User) {
    localStorage.setItem("sk_token", t);
    localStorage.setItem("sk_user", JSON.stringify(u));
    setToken(t);
    setUser(u);
  }

  async function login(phone: string, password: string) {
    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, password }),
      });
      const data = await res.json();
      if (!res.ok) return { ok: false, error: data.detail || "Login nahi ho saka." };
      persist(data.token, data.user);
      return { ok: true };
    } catch {
      return { ok: false, error: "Server se connect nahi ho saka." };
    }
  }

  async function signup(name: string, phone: string, password: string, city: string) {
    try {
      const res = await fetch(`${API_URL}/api/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, phone, password, city }),
      });
      const data = await res.json();
      if (!res.ok) return { ok: false, error: data.detail || "Signup nahi ho saka." };
      persist(data.token, data.user);
      return { ok: true };
    } catch {
      return { ok: false, error: "Server se connect nahi ho saka." };
    }
  }

  function logout() {
    localStorage.removeItem("sk_token");
    localStorage.removeItem("sk_user");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
