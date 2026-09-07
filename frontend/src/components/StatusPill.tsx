import { DataStatus } from "@/lib/api";

const CONFIG: Record<DataStatus, { label: string; dot: string; text: string }> = {
  verified: { label: "Verified", dot: "bg-brand-500", text: "text-brand-600" },
  latest_available: { label: "Latest available", dot: "bg-amber-400", text: "text-amber-500" },
  unavailable: { label: "No verified data", dot: "bg-alert-500", text: "text-alert-500" },
};

export default function StatusPill({
  status,
  note,
  source,
}: {
  status: DataStatus;
  note?: string | null;
  source?: string | null;
}) {
  const c = CONFIG[status];
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-[11px] font-medium ${c.text}`}
      title={note || undefined}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${c.dot}`} />
      {c.label}
      {source ? ` · ${source}` : ""}
    </span>
  );
}
