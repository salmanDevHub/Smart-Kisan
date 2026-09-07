"use client";

export default function TopBar({ title }: { title?: string }) {
  const today = new Date().toLocaleDateString("en-PK", {
    weekday: "short", year: "numeric", month: "short", day: "numeric",
  });

  return (
    <div className="flex items-center justify-between px-8 py-5 bg-white border-b border-black/5">
      <h1 className="text-xl font-semibold text-ink">{title}</h1>
      <div className="flex items-center gap-4 text-sm text-ink/60">
        <span>{today}</span>
        <button className="w-9 h-9 rounded-full bg-cream flex items-center justify-center hover:bg-brand-50 transition-colors">
          🔔
        </button>
      </div>
    </div>
  );
}
