"use client";

import { useEffect, useState } from "react";
import TopBar from "@/components/TopBar";
import Card from "@/components/Card";
import StatusPill from "@/components/StatusPill";
import { api, FertilizerPrice, FertilizerCompany, MarketplaceProduct } from "@/lib/api";

export default function FertilizerPage() {
  const [tab, setTab] = useState<"intelligence" | "marketplace">("marketplace");

  return (
    <>
      <TopBar title="Fertilizer" />
      <div className="px-8 pt-6">
        <div className="flex gap-1 bg-white border border-black/10 rounded-lg p-1 w-fit">
          <button
            onClick={() => setTab("marketplace")}
            className={`px-4 py-1.5 rounded-md text-sm transition-colors ${tab === "marketplace" ? "bg-brand-600 text-white" : "text-ink/60 hover:text-ink"}`}
          >
            Marketplace
          </button>
          <button
            onClick={() => setTab("intelligence")}
            className={`px-4 py-1.5 rounded-md text-sm transition-colors ${tab === "intelligence" ? "bg-brand-600 text-white" : "text-ink/60 hover:text-ink"}`}
          >
            Price Intelligence
          </button>
        </div>
      </div>
      <div className="p-8 pt-6">
        {tab === "intelligence" ? <PriceIntelligence /> : <Marketplace />}
      </div>
    </>
  );
}

function PriceIntelligence() {
  const [items, setItems] = useState<FertilizerPrice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.fertilizerPrices().then((d) => { setItems(d); setLoading(false); });
  }, []);

  return (
    <Card title="Fertilizer Price Intelligence">
      {loading ? <p className="text-sm text-ink/40">Loading…</p> : (
        <div className="divide-y divide-black/5">
          {items.map((f) => (
            <div key={f.name} className="flex items-center justify-between py-3">
              <div>
                <p className="font-medium">{f.name}{f.brand ? ` — ${f.brand}` : ""}</p>
                <StatusPill status={f.meta.status} source={f.meta.source} note={f.meta.note} />
              </div>
              <div className="text-right">
                {f.price != null ? (
                  <p className="font-semibold">Rs {f.price.toLocaleString()}</p>
                ) : (
                  <p className="text-sm text-ink/30 italic">no verified price</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

function Marketplace() {
  const [companies, setCompanies] = useState<FertilizerCompany[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [products, setProducts] = useState<MarketplaceProduct[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [category, setCategory] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.marketplaceCompanies().then(setCompanies);
    api.marketplaceCategories().then(setCategories);
  }, []);

  useEffect(() => {
    setLoading(true);
    const handle = setTimeout(() => {
      api.marketplaceProducts({ companyId: companyId || undefined, category: category || undefined, search: search || undefined })
        .then((d) => { setProducts(d); setLoading(false); });
    }, 250);
    return () => clearTimeout(handle);
  }, [companyId, category, search]);

  return (
    <div className="grid grid-cols-4 gap-6">
      <div className="col-span-1 space-y-4">
        <Card title="Search">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products…"
            className="w-full bg-cream rounded-lg px-3 py-2 text-sm outline-none border border-black/5 focus:border-brand-400"
          />
        </Card>

        <Card title="Categories">
          <div className="space-y-1">
            <button
              onClick={() => setCategory("")}
              className={`w-full text-left px-3 py-1.5 rounded-lg text-sm ${category === "" ? "bg-brand-50 text-brand-700 font-medium" : "text-ink/60 hover:bg-cream"}`}
            >
              All Categories
            </button>
            {categories.map((c) => (
              <button
                key={c}
                onClick={() => setCategory(c)}
                className={`w-full text-left px-3 py-1.5 rounded-lg text-sm ${category === c ? "bg-brand-50 text-brand-700 font-medium" : "text-ink/60 hover:bg-cream"}`}
              >
                {c}
              </button>
            ))}
          </div>
        </Card>

        <Card title="Companies">
          <div className="space-y-1 max-h-96 overflow-y-auto scrollbar-thin">
            <button
              onClick={() => setCompanyId("")}
              className={`w-full text-left px-3 py-1.5 rounded-lg text-sm ${companyId === "" ? "bg-brand-50 text-brand-700 font-medium" : "text-ink/60 hover:bg-cream"}`}
            >
              All Companies
            </button>
            {companies.map((c) => (
              <button
                key={c.id}
                onClick={() => setCompanyId(c.id)}
                className={`w-full text-left px-3 py-1.5 rounded-lg text-sm flex items-center gap-2 ${companyId === c.id ? "bg-brand-50 text-brand-700 font-medium" : "text-ink/60 hover:bg-cream"}`}
              >
                <span className="w-6 h-6 rounded-md bg-brand-100 text-brand-700 text-[10px] font-bold flex items-center justify-center shrink-0">
                  {c.logo_initial}
                </span>
                <span className="truncate">{c.name}</span>
              </button>
            ))}
          </div>
        </Card>
      </div>

      <div className="col-span-3">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-ink/50">{loading ? "Loading…" : `${products.length} products`}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {products.map((p) => (
            <Card key={p.id}>
              <div className="flex items-start justify-between mb-2">
                <div>
                  <p className="text-[11px] uppercase tracking-wide text-amber-500 font-medium">{p.category}</p>
                  <h4 className="font-semibold text-ink mt-0.5">{p.name}</h4>
                  <p className="text-xs text-ink/50">{p.company_name}</p>
                </div>
              </div>
              <p className="text-sm text-ink/60 mb-3">{p.description}</p>
              {p.nutrient_content && (
                <p className="text-xs text-brand-600 mb-2">Nutrient content: {p.nutrient_content}</p>
              )}
              <div className="flex items-center justify-between pt-3 border-t border-black/5">
                <span className="text-sm text-ink/40 italic">Contact dealer for price</span>
                <button className="bg-brand-600 hover:bg-brand-700 text-white text-xs px-3 py-1.5 rounded-lg transition-colors">
                  Find Dealer
                </button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
