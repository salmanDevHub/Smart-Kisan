"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: "🏠" },
  { href: "/market-prices", label: "Market Prices", icon: "🌾" },
  { href: "/fertilizer", label: "Fertilizer", icon: "🧪" },
  { href: "/weather", label: "Weather", icon: "☀️" },
  { href: "/assistant", label: "AI Assistant", icon: "💬" },
  { href: "/news", label: "News & Alerts", icon: "📰" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  return (
    <aside className="w-64 shrink-0 bg-sidebar text-white/90 flex flex-col min-h-screen">
      <div className="px-6 py-6 flex items-center gap-2 border-b border-white/10">
        <span className="text-2xl">🌱</span>
        <div>
          <p className="font-semibold text-white leading-none">Smart Kisan</p>
          <p className="text-[11px] text-white/50 mt-0.5">AI Agriculture Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                active
                  ? "bg-sidebar-active text-white font-medium"
                  : "text-white/70 hover:bg-sidebar-hover hover:text-white"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="px-3 py-4 border-t border-white/10">
        {user ? (
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center text-sm font-semibold">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white truncate">{user.name}</p>
              <button
                onClick={() => { logout(); router.push("/login"); }}
                className="text-[11px] text-white/50 hover:text-white/80"
              >
                Logout
              </button>
            </div>
          </div>
        ) : (
          <Link
            href="/login"
            className="block text-center bg-brand-500 hover:bg-brand-600 text-white text-sm py-2 rounded-lg transition-colors"
          >
            Login / Signup
          </Link>
        )}
      </div>
    </aside>
  );
}
