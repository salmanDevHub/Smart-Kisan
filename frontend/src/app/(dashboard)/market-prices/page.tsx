"use client";

import { useEffect, useState } from "react";
import TopBar from "@/components/TopBar";
import Card from "@/components/Card";
import StatusPill from "@/components/StatusPill";
import { api, CropPrice } from "@/lib/api";

const CROPS = ["wheat", "rice", "cotton", "maize", "sugarcane", "potato", "onion", "tomato"];
const CITIES = ["Multan", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Peshawar", "Quetta"];

export default function MarketPricesPage() {
  const [crop, setCrop] = useState("");
  const [city, setCity] = useState("");
  const [items, setItems] = useState<CropPrice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.cropPrices(crop || undefined, city || undefined).then((d) => {
      setItems(d);
      setLoading(false);
    });
  }, [crop, city]);

  return (
    <>
      <TopBar title="Market Prices" />
      <div className="p-8 space-y-4">
        <div className="flex gap-3">
          <select value={city} onChange={(e) => setCity(e.target.value)} className="bg-white border border-black/10 rounded-lg px-3 py-2 text-sm">
            <option value="">All Cities</option>
            {CITIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={crop} onChange={(e) => setCrop(e.target.value)} className="bg-white border border-black/10 rounded-lg px-3 py-2 text-sm capitalize">
            <option value="">All Commodities</option>
            {CROPS.map((c) => <option key={c} value={c} className="capitalize">{c}</option>)}
          </select>
        </div>

        <Card title="All Commodities">
          {loading ? (
            <p className="text-sm text-ink/40">Loading…</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-ink/40 text-xs uppercase">
                  <th className="pb-2 font-normal">Commodity</th>
                  <th className="pb-2 font-normal">Market</th>
                  <th className="pb-2 font-normal">Province</th>
                  <th className="pb-2 font-normal text-right">Price</th>
                  <th className="pb-2 font-normal text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it, i) => (
                  <tr key={i} className="border-t border-black/5">
                    <td className="py-2.5">{it.crop}</td>
                    <td className="py-2.5 text-ink/60">{it.market}</td>
                    <td className="py-2.5 text-ink/60">{it.province}</td>
                    <td className="py-2.5 text-right font-medium">
                      {it.price != null ? `Rs ${it.price.toLocaleString()} / ${it.unit}` : <span className="text-ink/30 italic font-normal">not available</span>}
                    </td>
                    <td className="py-2.5 text-right"><StatusPill status={it.meta.status} note={it.meta.note} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>

        <div className="flex items-start gap-3 bg-brand-50 border border-brand-100 rounded-xl p-4 text-sm text-brand-700">
          <span>🛡️</span>
          <div>
            <p className="font-medium">Why no data?</p>
            <p className="text-ink/60 mt-0.5">We only show verified data from official sources to ensure accuracy — never estimated or invented prices.</p>
          </div>
        </div>
      </div>
    </>
  );
}
