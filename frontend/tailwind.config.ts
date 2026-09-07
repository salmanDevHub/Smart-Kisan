import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        cream: "#f7f5ef",
        ink: "#1a2420",
        sidebar: {
          DEFAULT: "#132b1d",
          hover: "#1c3c28",
          active: "#24512f",
        },
        brand: {
          50: "#eef7f0",
          100: "#d3ecd8",
          400: "#3fa35a",
          500: "#2f7d4f",
          600: "#256640",
          700: "#1c4e31",
        },
        amber: {
          50: "#fdf3e2",
          400: "#e8a33d",
          500: "#d6912b",
        },
        alert: {
          50: "#fdece3",
          500: "#d9622b",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(20,30,20,0.04), 0 1px 12px rgba(20,30,20,0.05)",
      },
      borderRadius: {
        xl2: "1rem",
      },
    },
  },
  plugins: [],
};
export default config;
