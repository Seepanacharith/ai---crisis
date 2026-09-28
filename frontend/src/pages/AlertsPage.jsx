import React, { useState, useEffect } from 'react';
import { Bell, AlertTriangle, Shield, Clock, MapPin, ExternalLink } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { alertAPI } from '../services/api';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [disasterFilter, setDisasterFilter] = useState('all');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAlerts();
  }, [disasterFilter]);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const res = await alertAPI.getAll(disasterFilter);
      setAlerts(res.data);
    } catch (err) {
      console.error("Failed to load alerts:", err);
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
              <Bell className="w-7 h-7 text-amber-400" /> Live Disaster Alerts & Warnings
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Authoritative real-time weather advisories, hurricane watches, flash flood warnings, and aftershock notices.
            </p>
          </div>

          <select
            value={disasterFilter}
            onChange={(e) => setDisasterFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2 text-xs font-semibold focus:outline-none focus:border-rose-500"
          >
            <option value="all">All Disasters</option>
            <option value="flood">Floods</option>
            <option value="earthquake">Earthquakes</option>
            <option value="fire">Wildfires</option>
            <option value="cyclone">Cyclones</option>
          </select>
        </div>

        {/* Alerts List */}
        {loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading active alerts...</div>
        ) : (
          <div className="space-y-4">
            {alerts.map((alt) => (
              <div
                key={alt.id}
                className={`bg-slate-900 border rounded-2xl p-6 space-y-3 transition-all ${
                  alt.severity === 'Critical'
                    ? 'border-rose-900/80 shadow-lg shadow-rose-950/20'
                    : 'border-amber-900/60 shadow-lg shadow-amber-950/10'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center space-x-3">
                    <span className={`px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider ${
                      alt.severity === 'Critical' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-amber-950 text-amber-400 border border-amber-800'
                    }`}>
                      {alt.severity}
                    </span>
                    <h3 className="text-base font-bold text-white">{alt.title}</h3>
                  </div>

                  <span className="text-xs text-slate-500 font-mono flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" /> Issued: {new Date(alt.issued_at).toLocaleTimeString()}
                  </span>
                </div>

                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  {alt.description}
                </p>

                <div className="pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1 text-slate-300 font-medium">
                    <MapPin className="w-3.5 h-3.5 text-rose-500" /> Region: {alt.location}
                  </span>
                  <span className="text-[11px] text-slate-500">
                    Source: <strong className="text-slate-300">{alt.source}</strong>
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

      </main>

      <Footer />
    </div>
  );
}
