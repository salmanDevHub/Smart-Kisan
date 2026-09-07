import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Smart Kisan — AI Agriculture Intelligence",
  description:
    "AI-powered digital agriculture assistant for Pakistani farmers: mandi prices, fertilizer marketplace, weather, and daily agri news.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans bg-cream text-ink antialiased`}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
