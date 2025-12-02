import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    setSummary({
      totalRides: 500,
      completionRate: 88,
      totalRevenue: 220000,
      peakHours: [
        { hour: "8", rides: 40 },
        { hour: "9", rides: 38 },
        { hour: "18", rides: 37 },
        { hour: "19", rides: 35 },
      ],
      zoneRevenue: [
        { zone: "Whitefield", revenue: 32000 },
        { zone: "Koramangala", revenue: 30000 },
        { zone: "Indiranagar", revenue: 28000 },
        { zone: "BTM Layout", revenue: 22000 },
      ],
      cancellationByHour: [
        { hour: "7", rate: 15 },
        { hour: "8", rate: 14 },
        { hour: "9", rate: 13 },
        { hour: "18", rate: 16 },
      ],
    });
  }, []);

  if (!summary) return <div style={{ padding: 24 }}>Loading dashboard...</div>;

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#020617",
        color: "white",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI'",
        padding: "24px",
      }}
    >
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 28, marginBottom: 8 }}>
          Namma Yatri Ride-Hailing Analytics
        </h1>
        <p style={{ color: "#9ca3af" }}>
          Bangalore demand optimization • 7 days • 500 rides
        </p>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 16,
          marginBottom: 24,
        }}
      >
        <KpiCard
          label="Total Rides"
          value={summary.totalRides.toLocaleString()}
          subtitle="Sample dataset"
        />
        <KpiCard
          label="Completion Rate"
          value={summary.completionRate + "%"}
          subtitle="Target: 95%"
        />
        <KpiCard
          label="Total Revenue"
          value={"₹" + summary.totalRevenue.toLocaleString()}
          subtitle="Sample week"
        />
        <KpiCard
          label="Projected Uplift"
          value="+₹50,000"
          subtitle="With optimization"
        />
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1.5fr",
          gap: 16,
          marginBottom: 24,
        }}
      >
        <Card title="Hourly Demand Trend">
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={summary.peakHours}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="hour" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="rides"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Revenue by Top Zones">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={summary.zoneRevenue} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis type="number" stroke="#9ca3af" />
              <YAxis dataKey="zone" type="category" stroke="#9ca3af" />
              <Tooltip />
              <Bar dataKey="revenue" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1.5fr 2fr",
          gap: 16,
        }}
      >
        <Card title="Cancellation Hotspots (by Hour)">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={summary.cancellationByHour}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="hour" stroke="#9ca3af" />
              <YAxis unit="%" stroke="#9ca3af" />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="rate"
                stroke="#f97316"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Executive Summary & Insights">
          <ul style={{ paddingLeft: 18, color: "#e5e7eb", fontSize: 14 }}>
            <li>Peak demand in 7-10 AM and 5-8 PM windows; supply gaps here.</li>
            <li>
              Top 3 zones contribute ~60% of weekly revenue; prioritize drivers
              nearby.
            </li>
            <li>
              Cancellations spike when wait time exceeds 8 minutes during peak
              hours.
            </li>
            <li>
              Recommendation: +40% driver coverage in peak slots for top zones,
              projected +₹50K/week revenue.
            </li>
          </ul>
        </Card>
      </section>
    </div>
  );
}

function KpiCard({ label, value, subtitle }) {
  return (
    <div
      style={{
        background: "linear-gradient(to bottom right, #0f172a, #020617)",
        borderRadius: 12,
        padding: 16,
        border: "1px solid #1f2937",
      }}
    >
      <div style={{ fontSize: 13, color: "#9ca3af", marginBottom: 4 }}>
        {label}
      </div>
      <div style={{ fontSize: 24, fontWeight: 600, marginBottom: 4 }}>
        {value}
      </div>
      <div style={{ fontSize: 12, color: "#6b7280" }}>{subtitle}</div>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <div
      style={{
        background: "#020617",
        borderRadius: 12,
        padding: 16,
        border: "1px solid #1f2937",
      }}
    >
      <div
        style={{
          fontSize: 15,
          fontWeight: 500,
          marginBottom: 8,
          color: "#e5e7eb",
        }}
      >
        {title}
      </div>
      {children}
    </div>
  );
}

export default App;


