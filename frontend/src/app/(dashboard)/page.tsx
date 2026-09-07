"use client";

import { useEffect, useState } from "react";
import TopBar from "@/components/TopBar";
import Card from "@/components/Card";
import StatusPill from "@/components/StatusPill";
import { api, WeatherData, CropPrice, FertilizerPrice, NewsItem } from "@/lib/api";
import Link from "next/link";

export default function DashboardHome() {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [crops, setCrops] = useState<CropPrice[]>([]);
  const [fert, setFert] = useState<FertilizerPrice[]>([]);
  const [news, setNews] = useState<NewsItem[]>([]);

  useEffect(() => {
    api.weather("Multan").then(setWeather);
    api.cropPrices().then(setCrops);
    api.fertilizerPrices().then(setFert);
    api.news(3).then(setNews);
  }, []);

  const verifiedCount =
    (crops.filter((c) => c.meta.status !== "unavailable").length) +
    (fert.filter((f) => f.meta.status !== "unavailable").length);

  return (
    <>
      <TopBar title="Dashboard" />
      <div className="p-8 space-y-6">
        <div className="bg-gradient-to-r from-brand-700 to-brand-500 rounded-2xl p-6 text-white">
          <p className="text-sm text-white/70 mb-1">آج کا مارکیٹ ریٹ، موسم اور مشورہ</p>
          <h2 className="text-2xl font-semibold">Daily Market, Weather &amp; AI Advisory for Farmers</h2>
        </div>

        <div className="grid grid-cols-4 gap-4">
          <Card><p className="text-xs text-ink/50 mb-1">Market Overview</p><p className="text-2xl font-semibold">{crops.length}</p><p className="text-xs text-ink/40">Commodities tracked</p></Card>
          <Card><p className="text-xs text-ink/50 mb-1">Verified Data</p><p className="text-2xl font-semibold">{verifiedCount}</p><p className="text-xs text-ink/40">Markets today</p></Card>
          <Card><p className="text-xs text-ink/50 mb-1">AI Insights</p><p className="text-2xl font-semibold text-brand-600">Active</p><p className="text-xs text-ink/40">Smart analysis</p></Card>
          <Card><p className="text-xs text-ink/50 mb-1">Farm Alerts</p><p className="text-2xl font-semibold">{news.length}</p><p className="text-xs text-ink/40">New alerts</p></Card>
        </div>

        <div className="grid grid-cols-3 gap-6">
          <Card className="col-span-2" title="Market Prices (Today)" action={<Link href="/market-prices" className="text-xs text-brand-600 font-medium">View All →</Link>}>
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-ink/40 text-xs uppercase">
                  <th className="pb-2 font-normal">Commodity</th>
                  <th className="pb-2 font-normal">Market</th>
                  <th className="pb-2 font-normal text-right">Price</th>
                  <th className="pb-2 font-normal text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {crops.slice(0, 5).map((c, i) => (
                  <tr key={i} className="border-t border-black/5">
                    <td className="py-2.5">{c.crop}</td>
                    <td className="py-2.5 text-ink/60">{c.market}</td>
                    <td className="py-2.5 text-right font-medium">
                      {c.price != null ? `Rs ${c.price.toLocaleString()}` : <span className="text-ink/30 italic font-normal">—</span>}
                    </td>
                    <td className="py-2.5 text-right"><StatusPill status={c.meta.status} note={c.meta.note} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>

          <Card title="Weather Today">
            {weather && weather.meta.status !== "unavailable" ? (
              <>
                <div className="flex items-center gap-3">
                  <span className="text-4xl">☀️</span>
                  <div>
                    <p className="text-3xl font-semibold">{Math.round(weather.temperature_c ?? 0)}°C</p>
                    <p className="text-sm text-ink/50">{weather.condition}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-4 text-xs text-ink/60">
                  <p>Humidity {weather.humidity_pct}%</p>
                  <p>Wind {Math.round(weather.wind_kph ?? 0)} km/h</p>
                  <p>Rain {weather.rain_probability_pct ?? 0}%</p>
                </div>
              </>
            ) : (
              <p className="text-sm text-alert-500">Weather data unavailable — {weather?.meta.note}</p>
            )}
          </Card>
        </div>

        <Card className="bg-brand-50 border-brand-100" title="AI Advisory (Summary)">
          <p className="text-sm text-ink/70">
            AI insights use only verified data currently available. Connect live mandi and
            fertilizer price sources (see backend README) to unlock full market advisory.
          </p>
        </Card>
      </div>
    </>
  );
}
