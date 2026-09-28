import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, MessageSquare, AlertTriangle, Waves, Activity, Flame, Wind, CheckSquare, MapPin, Bell, Zap, ArrowRight, Clock, HeartHandshake, CheckCircle2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import EmergencyBanner from '../components/EmergencyBanner';
import { alertAPI, emergencyAPI, metricsAPI } from '../services/api';

export default function DashboardPage() {
  const [alerts, setAlerts] = useState([]);
  const [facilities, setFacilities] = useState([]);
  const [health, setHealth] = useState(null);
  const [quickQuery, setQuickQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [alertRes, facRes, healthRes] = await Promise.all([
          alertAPI.getAll(),
          emergencyAPI.getFacilities(),
          metricsAPI.getHealth()
        ]);
        setAlerts(alertRes.data.slice(0, 3));
        setFacilities(facRes.data.slice(0, 3));
        setHealth(healthRes.data);
      } catch (err) {
        console.error("Dashboard data load error:", err);
      }
    };
    loadDashboardData();
  }, []);

  const handleQuickAsk = (e) => {
    e.preventDefault();
    if (quickQuery.trim()) {
      navigate(`/chat?query=${encodeURIComponent(quickQuery)}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />
      <EmergencyBanner />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Top Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
              <Shield className="w-7 h-7 text-rose-500" /> Disaster Operations Dashboard
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Real-time emergency monitoring, AI assistant access, and local safety infrastructure.
            </p>
          </div>
          
          {/* System Status Widget */}
          <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 px-4 py-2.5 rounded-xl text-xs">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></div>
            <span className="text-slate-300 font-semibold">System Status:</span>
            <span className="text-emerald-400 font-bold bg-emerald-950/80 border border-emerald-800 px-2 py-0.5 rounded">
              ONLINE & READY
            </span>
          </div>
        </div>

        {/* Quick Ask AI Bar */}
        <div className="bg-gradient-to-r from-rose-950/60 via-slate-900 to-slate-900 border border-rose-900/50 p-6 rounded-2xl shadow-xl space-y-3">
          <div className="flex items-center space-x-2 text-rose-300 font-bold text-sm">
            <Zap className="w-5 h-5 text-rose-400" /> Quick Ask Crisis AI
          </div>
          <form onSubmit={handleQuickAsk} className="flex gap-2">
            <input
              type="text"
              value={quickQuery}
              onChange={(e) => setQuickQuery(e.target.value)}
              placeholder="Ask an emergency question (e.g., 'What should I do during a flood?')..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
            <button
              type="submit"
              className="px-6 py-3 bg-rose-600 hover:bg-rose-500 text-white font-bold text-sm rounded-xl flex items-center gap-2 shadow-lg shadow-rose-600/30"
            >
              Ask AI <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left 2 Columns */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Disaster Categories Grid */}
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Shield className="w-5 h-5 text-rose-500" /> Disaster Safety Categories
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                
                <Link to="/disasters/flood" className="bg-slate-900/80 border border-slate-800 hover:border-blue-500/50 p-5 rounded-xl flex items-center space-x-4 transition-all">
                  <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
                    <Waves className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-sm">Flood Protocol</h3>
                    <p className="text-xs text-slate-400">High ground & flash flood guide</p>
                  </div>
                </Link>

                <Link to="/disasters/earthquake" className="bg-slate-900/80 border border-slate-800 hover:border-amber-500/50 p-5 rounded-xl flex items-center space-x-4 transition-all">
                  <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-400">
                    <Activity className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-sm">Earthquake Protocol</h3>
                    <p className="text-xs text-slate-400">Drop, Cover & Hold On rules</p>
                  </div>
                </Link>

                <Link to="/disasters/fire" className="bg-slate-900/80 border border-slate-800 hover:border-rose-500/50 p-5 rounded-xl flex items-center space-x-4 transition-all">
                  <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400">
                    <Flame className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-sm">Fire Evacuation</h3>
                    <p className="text-xs text-slate-400">Smoke crawling & stop-drop-roll</p>
                  </div>
                </Link>

                <Link to="/disasters/cyclone" className="bg-slate-900/80 border border-slate-800 hover:border-emerald-500/50 p-5 rounded-xl flex items-center space-x-4 transition-all">
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
                    <Wind className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-sm">Cyclone Prep</h3>
                    <p className="text-xs text-slate-400">Storm shutters & eye caution</p>
                  </div>
                </Link>

              </div>
            </div>

            {/* Live Alerts Stream */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Bell className="w-5 h-5 text-amber-400" /> Active Emergency Alerts
                </h3>
                <Link to="/alerts" className="text-xs text-rose-400 hover:underline font-semibold">View All</Link>
              </div>

              <div className="space-y-3">
                {alerts.map((alt) => (
                  <div key={alt.id} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          alt.severity === 'Critical' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-amber-950 text-amber-400 border border-amber-800'
                        }`}>
                          {alt.severity}
                        </span>
                        <h4 className="text-xs font-bold text-white">{alt.title}</h4>
                      </div>
                      <p className="text-xs text-slate-400">{alt.description}</p>
                      <p className="text-[10px] text-slate-500 flex items-center gap-1 pt-1">
                        <MapPin className="w-3 h-3" /> {alt.location}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Right Column */}
          <div className="space-y-8">
            
            {/* Emergency Facilities Summary */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-rose-500" /> Nearby Facilities
                </h3>
                <Link to="/emergency-services" className="text-xs text-rose-400 hover:underline font-semibold">Full Map</Link>
              </div>

              <div className="space-y-3">
                {facilities.map((fac) => (
                  <div key={fac.id} className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1 text-xs">
                    <div className="flex justify-between font-bold text-white">
                      <span>{fac.name}</span>
                      <span className="text-rose-400 font-mono">{fac.distance_km} km</span>
                    </div>
                    <p className="text-slate-400">{fac.address}</p>
                    <div className="flex justify-between text-[10px] text-slate-500 pt-1">
                      <span>{fac.capacity}</span>
                      <span className="text-emerald-400 font-semibold">{fac.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Checklist Quick Entry */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <CheckSquare className="w-5 h-5 text-emerald-400" /> Go-Bag Checklist
              </h3>
              <p className="text-xs text-slate-400">
                Maintain a 72-hour survival kit for rapid evacuation readiness.
              </p>
              <Link to="/checklist" className="block text-center py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-xl transition-all shadow-md shadow-emerald-600/20">
                Open Interactive Checklist
              </Link>
            </div>

          </div>

        </div>

      </main>

      <Footer />
    </div>
  );
}
