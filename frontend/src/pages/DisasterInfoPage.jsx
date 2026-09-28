import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Waves, Activity, Flame, Wind, CheckCircle2, AlertTriangle, Shield, ArrowRight } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { disasterAPI } from '../services/api';

export default function DisasterInfoPage() {
  const { type } = useParams();
  const [activeTab, setActiveTab] = useState(type || 'flood');
  const [guides, setGuides] = useState([]);
  const [selectedGuide, setSelectedGuide] = useState(null);

  useEffect(() => {
    const fetchGuides = async () => {
      try {
        const res = await disasterAPI.getAll();
        setGuides(res.data);
        const match = res.data.find(g => g.type === activeTab) || res.data[0];
        setSelectedGuide(match);
      } catch (err) {
        console.error("Failed to load disaster guides:", err);
      }
    };
    fetchGuides();
  }, [activeTab]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
            <Shield className="w-7 h-7 text-rose-500" /> Disaster Safety & Action Protocols
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Authoritative, step-by-step emergency procedures for Flood, Earthquake, Fire, and Cyclone hazards.
          </p>
        </div>

        {/* Tab Selection */}
        <div className="flex flex-wrap gap-3 border-b border-slate-800 pb-4">
          {[
            { id: 'flood', label: 'Flood Safety', icon: Waves, color: 'text-blue-400' },
            { id: 'earthquake', label: 'Earthquake Protocol', icon: Activity, color: 'text-amber-400' },
            { id: 'fire', label: 'Fire Evacuation', icon: Flame, color: 'text-rose-400' },
            { id: 'cyclone', label: 'Cyclone Readiness', icon: Wind, color: 'text-emerald-400' },
          ].map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-semibold text-xs sm:text-sm transition-all ${
                  isSelected
                    ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30'
                    : 'bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <Icon className={`w-4 h-4 ${isSelected ? 'text-white' : tab.color}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Selected Guide Details */}
        {selectedGuide && (
          <div className="space-y-8 animate-fade-in">
            
            {/* Overview Banner */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-3">
              <h2 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
                {selectedGuide.title}
              </h2>
              <p className="text-sm text-slate-300 leading-relaxed max-w-4xl">
                {selectedGuide.overview}
              </p>
            </div>

            {/* 3 Phases Grid: Before, During, After */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Phase 1: Before */}
              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
                <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-xl w-fit text-blue-400 font-bold text-xs uppercase tracking-wider">
                  Phase 1: Before (Preparation)
                </div>
                <ul className="space-y-3 text-xs text-slate-300">
                  {selectedGuide.before.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Phase 2: During */}
              <div className="bg-slate-900/80 border border-rose-900/50 rounded-2xl p-6 space-y-4 shadow-lg shadow-rose-950/30">
                <div className="p-2.5 bg-rose-500/10 border border-rose-500/20 rounded-xl w-fit text-rose-400 font-bold text-xs uppercase tracking-wider">
                  Phase 2: During (Immediate Action)
                </div>
                <ul className="space-y-3 text-xs text-slate-300">
                  {selectedGuide.during.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5 animate-pulse" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Phase 3: After */}
              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
                <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl w-fit text-emerald-400 font-bold text-xs uppercase tracking-wider">
                  Phase 3: After (Recovery & Health)
                </div>
                <ul className="space-y-3 text-xs text-slate-300">
                  {selectedGuide.after.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>

          </div>
        )}

      </main>

      <Footer />
    </div>
  );
}
