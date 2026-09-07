"use client";

import { useEffect, useState } from "react";
import TopBar from "@/components/TopBar";
import Card from "@/components/Card";
import { api, NewsItem } from "@/lib/api";

const CATEGORY_COLOR: Record<string, string> = {
  "Market": "text-amber-500",
  "Fertilizer": "text-brand-600",
  "Weather": "text-alert-500",
  "Policy": "text-ink/60",
};

export default function NewsPage() {
  const [items, setItems] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.news(15).then((d) => { setItems(d); setLoading(false); });
  }, []);

  return (
    <>
      <TopBar title="News & Alerts" />
      <div className="p-8 space-y-4">
        {loading && <p className="text-sm text-ink/40">Loading…</p>}

        {!loading && items.length === 0 && (
          <Card><p className="text-sm text-alert-500">No verified news items could be retrieved right now — source feeds unreachable.</p></Card>
        )}

        {items.map((item, i) => (
          <Card key={i}>
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className={`text-[11px] uppercase tracking-wide font-semibold ${CATEGORY_COLOR[item.category] || "text-ink/50"}`}>
                  {item.category}
                </p>
                <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-ink hover:text-brand-600 block mt-1">
                  {item.title}
                </a>
                <p className="text-sm text-ink/60 mt-1">{item.summary}</p>
                <p className="text-xs text-ink/40 mt-2">{item.source} · {item.published || "date unavailable"}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </>
  );
}
