const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type DataStatus = "verified" | "latest_available" | "unavailable";

export interface SourceMeta {
  status: DataStatus;
  source?: string | null;
  source_url?: string | null;
  as_of?: string | null;
  note?: string | null;
}

export interface NewsItem {
  title: string;
  summary: string;
  published?: string | null;
  category: string;
  source: string;
  source_url: string;
}

export interface WeatherData {
  city: string;
  temperature_c?: number | null;
  feels_like_c?: number | null;
  humidity_pct?: number | null;
  wind_kph?: number | null;
  rain_probability_pct?: number | null;
  condition?: string | null;
  forecast_3day: Array<{
    date: string;
    condition: string;
    max_c: number;
    min_c: number;
    rain_probability_pct: number;
  }>;
  meta: SourceMeta;
}

export interface CropPrice {
  crop: string;
  market: string;
  city: string;
  province: string;
  price?: number | null;
  unit: string;
  trend?: string | null;
  meta: SourceMeta;
}

export interface FertilizerPrice {
  name: string;
  brand?: string | null;
  price?: number | null;
  previous_price?: number | null;
  change_pct?: number | null;
  city?: string | null;
  unit: string;
  meta: SourceMeta;
}

export interface FertilizerCompany {
  id: string;
  name: string;
  logo_initial: string;
  description: string;
  website?: string | null;
  categories: string[];
}

export interface MarketplaceProduct {
  id: string;
  company_id: string;
  company_name: string;
  name: string;
  category: string;
  nutrient_content?: string | null;
  description: string;
  price?: number | null;
  unit?: string | null;
}

async function safeFetch<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_URL}${path}`, { cache: "no-store" });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export const api = {
  news: (limit = 12) => safeFetch<NewsItem[]>(`/api/news?limit=${limit}`, []),
  weather: (city: string) =>
    safeFetch<WeatherData | null>(`/api/weather?city=${encodeURIComponent(city)}`, null),
  cropPrices: (crop?: string, city?: string) => {
    const params = new URLSearchParams();
    if (crop) params.set("crop", crop);
    if (city) params.set("city", city);
    return safeFetch<CropPrice[]>(`/api/mandi/prices?${params.toString()}`, []);
  },
  fertilizerPrices: () => safeFetch<FertilizerPrice[]>(`/api/fertilizer/prices`, []),
  marketplaceCompanies: () => safeFetch<FertilizerCompany[]>(`/api/marketplace/companies`, []),
  marketplaceCategories: () => safeFetch<string[]>(`/api/marketplace/categories`, []),
  marketplaceProducts: (params: { companyId?: string; category?: string; search?: string } = {}) => {
    const q = new URLSearchParams();
    if (params.companyId) q.set("company_id", params.companyId);
    if (params.category) q.set("category", params.category);
    if (params.search) q.set("search", params.search);
    return safeFetch<MarketplaceProduct[]>(`/api/marketplace/products?${q.toString()}`, []);
  },
  chat: async (message: string, city?: string): Promise<string> => {
    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: [], city }),
      });
      if (!res.ok) return "Maaf kijiye, jawab abhi nahi mil saka. Backend chal raha hai check karein.";
      const data = await res.json();
      return data.reply as string;
    } catch {
      return "Backend se connect nahi ho saka. Kya server chal raha hai?";
    }
  },
};
