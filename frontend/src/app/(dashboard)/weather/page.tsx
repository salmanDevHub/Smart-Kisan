"use client";

import { useEffect, useState } from "react";
import TopBar from "@/components/TopBar";
import Card from "@/components/Card";
import { api, WeatherData } from "@/lib/api";

const CITIES = ["Multan", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Peshawar", "Quetta", "Vehari", "Bahawalpur", "Sargodha"];

export default function WeatherPage() {
  const [city, setCity] = useState("Multan");
  const [data, setData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.weather(city).then((d) => { setData(d); setLoading(false); });
  }, [city]);

  return (
    <>
      <TopBar title="Weather & Farm Alerts" />
      <div className="p-8 space-y-6">
        <select value={city} onChange={(e) => setCity(e.target.value)} className="bg-white border border-black/10 rounded-lg px-3 py-2 text-sm">
          {CITIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        {loading && <p className="text-sm text-ink/40">Loading…</p>}

        {!loading && data && data.meta.status === "unavailable" && (
          <Card><p className="text-alert-500 text-sm">Weather data unavailable — {data.meta.note}</p></Card>
        )}

        {!loading && data && data.meta.status !== "unavailable" && (
          <>
            <Card>
              <div className="flex items-center gap-6">
                <span className="text-6xl">☀️</span>
                <div>
                  <p className="text-5xl font-semibold">{Math.round(data.temperature_c ?? 0)}°C</p>
                  <p className="text-ink/50">{data.condition} — {data.city}</p>
                </div>
                <div className="ml-auto grid grid-cols-2 gap-x-8 gap-y-2 text-sm text-ink/60">
                  <p>Feels like {Math.round(data.feels_like_c ?? 0)}°C</p>
                  <p>Humidity {data.humidity_pct}%</p>
                  <p>Wind {Math.round(data.wind_kph ?? 0)} km/h</p>
                  <p>Rain chance {data.rain_probability_pct ?? 0}%</p>
                </div>
              </div>
            </Card>

            {data.forecast_3day.length > 0 && (
              <div className="grid grid-cols-3 gap-4">
                {data.forecast_3day.map((f) => (
                  <Card key={f.date}>
                    <p className="text-sm text-ink/50">{new Date(f.date).toLocaleDateString("en-PK", { weekday: "long" })}</p>
                    <p className="text-2xl font-semibold mt-1">{Math.round(f.max_c)}° / {Math.round(f.min_c)}°</p>
                    <p className="text-xs text-ink/50 mt-1">{f.condition} · {f.rain_probability_pct}% rain</p>
                  </Card>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
}
