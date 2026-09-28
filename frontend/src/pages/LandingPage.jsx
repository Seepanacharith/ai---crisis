import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, MessageSquare, Waves, Activity, Flame, Wind, Database, Zap, Cpu, Lock, CheckCircle2, ArrowRight } from 'lucide-react';
import EmergencyBanner from '../components/EmergencyBanner';
import Footer from '../components/Footer';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <EmergencyBanner />

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full text-center flex-1 flex flex-col justify-center">
        
        {/* Glow backdrop */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-rose-600/15 blur-[120px] rounded-full pointer-events-none"></div>

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/80 border border-rose-800 text-rose-300 text-xs font-semibold mx-auto mb-6">
          <Zap className="w-3.5 h-3.5 text-rose-400" /> Advanced RAG & Multi-lingual Emergency AI
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
          AI Crisis Companion
        </h1>
        
        <p className="mt-4 text-xl sm:text-2xl text-slate-300 font-medium max-w-3xl mx-auto">
          AI-powered disaster awareness and emergency assistance.
        </p>

        <p className="mt-3 text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Get fast, reliable, contextual safety guidelines powered by ChromaDB vector search, hybrid retrieval, and Gemini LLM integration during floods, earthquakes, fires, and cyclones.
        </p>

        {/* CTA Buttons */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link to="/chat" className="px-6 py-3.5 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl shadow-lg shadow-rose-600/30 flex items-center gap-2 text-base transition-all transform hover:-translate-y-0.5">
            <MessageSquare className="w-5 h-5" /> Start AI Crisis Chat <ArrowRight className="w-5 h-5" />
          </Link>
          <Link to="/disasters" className="px-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold rounded-xl flex items-center gap-2 text-base transition-colors">
            Explore Disaster Safety
          </Link>
        </div>

        {/* Category Cards */}
        <div className="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
          
          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl hover:border-blue-500/50 transition-all group">
            <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl w-fit text-blue-400 group-hover:scale-110 transition-transform">
              <Waves className="w-6 h-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">Flood Safety</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">High ground evacuation routes, flash flood protocols, and water sanitation guidelines.</p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl hover:border-amber-500/50 transition-all group">
            <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl w-fit text-amber-400 group-hover:scale-110 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">Earthquake Protocol</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">Drop, Cover, and Hold On standards, aftershock safety, and gas leak mitigation.</p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl hover:border-rose-500/50 transition-all group">
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl w-fit text-rose-400 group-hover:scale-110 transition-transform">
              <Flame className="w-6 h-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">Fire Evacuation</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">Smoke crawling techniques, stop-drop-roll, and wildfire defensible space rules.</p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl hover:border-emerald-500/50 transition-all group">
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl w-fit text-emerald-400 group-hover:scale-110 transition-transform">
              <Wind className="w-6 h-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">Cyclone Prep</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">Storm shutter boarding, emergency power preparation, and eye-of-storm caution.</p>
          </div>

        </div>

      </section>

      {/* How RAG Works Section */}
      <section className="bg-slate-900/60 border-y border-slate-800 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">Production RAG Architecture</h2>
            <p className="mt-2 text-sm text-slate-400">
              Unlike generic LLMs, our RAG pipeline grounds answers strictly in verified emergency knowledge documents using vector search and hybrid reranking.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800">
              <Database className="w-8 h-8 text-rose-500 mx-auto mb-3" />
              <h4 className="font-semibold text-white text-sm">1. Document Loading</h4>
              <p className="text-xs text-slate-400 mt-2">Chunking knowledge base files with Recursive Character Splitters and metadata tagging.</p>
            </div>
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800">
              <Cpu className="w-8 h-8 text-rose-500 mx-auto mb-3" />
              <h4 className="font-semibold text-white text-sm">2. Hybrid Vector Search</h4>
              <p className="text-xs text-slate-400 mt-2">Combining ChromaDB semantic embeddings with BM25 keyword matching.</p>
            </div>
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800">
              <Zap className="w-8 h-8 text-rose-500 mx-auto mb-3" />
              <h4 className="font-semibold text-white text-sm">3. CrossEncoder Rerank</h4>
              <p className="text-xs text-slate-400 mt-2">Selecting top 3-5 high-relevance chunks to inject into Gemini prompt context.</p>
            </div>
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800">
              <Lock className="w-8 h-8 text-rose-500 mx-auto mb-3" />
              <h4 className="font-semibold text-white text-sm">4. Redis Cached Stream</h4>
              <p className="text-xs text-slate-400 mt-2">Sub-second response caching with Server-Sent Events (SSE) progressive token streaming.</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
