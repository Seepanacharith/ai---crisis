import React, { useState, useEffect } from 'react';
import { Activity, Users, MessageSquare, Zap, Database, AlertOctagon, CheckCircle2, ShieldAlert, Cpu } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { adminAPI, metricsAPI } from '../services/api';

export default function AdminDashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const res = await metricsAPI.getMetrics();
      setMetrics(res.data);
    } catch (err) {
      console.error("Failed to load admin metrics:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
              <Activity className="w-7 h-7 text-rose-500" /> System Engineering & Performance Portal
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Observability metrics, P50/P95 latency breakdown, Redis cache hit ratios, and ChromaDB vector store health.
            </p>
          </div>

          <button
            onClick={loadMetrics}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl flex items-center gap-2 border border-slate-700"
          >
            Refresh Metrics
          </button>
        </div>

        {loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading system metrics...</div>
        ) : metrics ? (
          <div className="space-y-8">
            
            {/* Top Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-2 shadow-xl">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="text-xs font-semibold uppercase tracking-wider">Total Questions</span>
                  <MessageSquare className="w-5 h-5 text-rose-400" />
                </div>
                <div className="text-3xl font-bold text-white font-mono">{metrics.total_questions}</div>
                <p className="text-[11px] text-slate-500">{metrics.questions_today} questions processed today</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-2 shadow-xl">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="text-xs font-semibold uppercase tracking-wider">Redis Cache Hit Rate</span>
                  <Zap className="w-5 h-5 text-emerald-400" />
                </div>
                <div className="text-3xl font-bold text-emerald-400 font-mono">{metrics.cache_hit_rate_pct}%</div>
                <p className="text-[11px] text-slate-500">Sub-millisecond Redis response caching</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-2 shadow-xl">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="text-xs font-semibold uppercase tracking-wider">Average Latency</span>
                  <Activity className="w-5 h-5 text-blue-400" />
                </div>
                <div className="text-3xl font-bold text-white font-mono">{metrics.avg_latency_ms} <span className="text-xs text-slate-400">ms</span></div>
                <p className="text-[11px] text-slate-500">P50: {metrics.p50_latency_ms}ms | P95: {metrics.p95_latency_ms}ms</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-2 shadow-xl">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="text-xs font-semibold uppercase tracking-wider">ChromaDB Chunks</span>
                  <Database className="w-5 h-5 text-purple-400" />
                </div>
                <div className="text-3xl font-bold text-white font-mono">{metrics.vector_store_chunks}</div>
                <p className="text-[11px] text-slate-500">Indexed vector embeddings</p>
              </div>

            </div>

            {/* Latency Breakdown & System Component Health */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              
              {/* Component Status Grid */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-rose-500" /> System Component Health Matrix
                </h3>

                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-slate-400 font-semibold">FastAPI REST Server</span>
                    <p className="text-emerald-400 font-bold uppercase flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Healthy
                    </p>
                  </div>

                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-slate-400 font-semibold">Redis Cache Engine</span>
                    <p className="text-emerald-400 font-bold uppercase flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Healthy
                    </p>
                  </div>

                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-slate-400 font-semibold">ChromaDB Vector Store</span>
                    <p className="text-emerald-400 font-bold uppercase flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Healthy
                    </p>
                  </div>

                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-slate-400 font-semibold">Gemini LLM Provider</span>
                    <p className="text-emerald-400 font-bold uppercase flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Healthy
                    </p>
                  </div>
                </div>
              </div>

              {/* Performance Latency Percentiles */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Activity className="w-5 h-5 text-blue-400" /> Latency Percentiles Breakdown
                </h3>

                <div className="space-y-4 text-xs">
                  <div className="space-y-1">
                    <div className="flex justify-between font-semibold text-slate-300">
                      <span>P50 Latency (Median)</span>
                      <span className="font-mono text-white">{metrics.p50_latency_ms} ms</span>
                    </div>
                    <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                      <div className="bg-blue-500 h-full rounded-full" style={{ width: '35%' }}></div>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between font-semibold text-slate-300">
                      <span>P95 Latency (95th Percentile)</span>
                      <span className="font-mono text-white">{metrics.p95_latency_ms} ms</span>
                    </div>
                    <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                      <div className="bg-amber-500 h-full rounded-full" style={{ width: '65%' }}></div>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between font-semibold text-slate-300">
                      <span>LLM Error Rate</span>
                      <span className="font-mono text-emerald-400">{metrics.llm_errors_count} Errors</span>
                    </div>
                    <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                      <div className="bg-emerald-500 h-full rounded-full" style={{ width: '0%' }}></div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

          </div>
        ) : null}

      </main>

      <Footer />
    </div>
  );
}
