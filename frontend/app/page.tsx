"use client";

import { useEffect, useState } from "react";
import { api, TransactionResponse } from "@/lib/api";
import { generateRandomTransaction } from "@/lib/utils";
import { RiskGauge } from "@/components/RiskGauge";
import { HistoryTable } from "@/components/HistoryTable";
import { Activity, RefreshCw } from "lucide-react";

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [currentScore, setCurrentScore] = useState(0);
  const [history, setHistory] = useState<TransactionResponse[]>([]);

  const fetchHistory = async () => {
    try {
      const res = await api.get("/history");
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSimulate = async () => {
    setLoading(true);
    const mockData = generateRandomTransaction();
    
    try {
      // Send to Backend
      const res = await api.post("/predict", mockData);
      
      // Update UI
      setCurrentScore(res.data.risk_score);
      
      // Refresh Table
      await fetchHistory();
    } catch (err) {
      console.error(err);
      alert("API Error: Ensure backend is running on port 8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-600 rounded-lg">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">FraudGuard AI</h1>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            System Status: <span className="text-emerald-400">ONLINE</span>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Left Column: Controls & Gauge */}
          <div className="space-y-6">
            <section className="bg-slate-900/50 p-6 rounded-xl border border-slate-800">
              <h2 className="text-lg font-semibold text-white mb-4">Live Inference</h2>
              <RiskGauge score={currentScore} />
              
              <button
                onClick={handleSimulate}
                disabled={loading}
                className="mt-6 w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-3 px-4 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin" />
                ) : (
                  "Simulate Transaction"
                )}
              </button>
              <p className="mt-4 text-xs text-slate-500 text-center">
                Generates random PCA vectors and sends to XGBoost model.
              </p>
            </section>
          </div>

          {/* Right Column: History */}
          <div className="md:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Recent Activity</h2>
              <button onClick={fetchHistory} className="text-xs text-indigo-400 hover:text-indigo-300">
                Refresh Log
              </button>
            </div>
            <HistoryTable transactions={history} />
          </div>
        </div>

      </div>
    </main>
  );
}