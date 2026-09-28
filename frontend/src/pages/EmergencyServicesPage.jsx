import React, { useState, useEffect } from 'react';
import { MapPin, Phone, Activity, ShieldAlert, Navigation, Building2, Flame } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { emergencyAPI } from '../services/api';

export default function EmergencyServicesPage() {
  const [filterType, setFilterType] = useState('all');
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadFacilities();
  }, [filterType]);

  const loadFacilities = async () => {
    setLoading(true);
    try {
      const res = await emergencyAPI.getFacilities(filterType);
      setFacilities(res.data);
    } catch (err) {
      console.error("Failed to load facilities:", err);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'hospital': return Activity;
      case 'shelter': return Building2;
      case 'police': return ShieldAlert;
      case 'fire_station': return Flame;
      default: return MapPin;
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
              <MapPin className="w-7 h-7 text-rose-500" /> Nearby Emergency Services & Shelters
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Location-based geospatial finder for emergency medical centers, evacuation relief camps, police, and fire dispatch.
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex flex-wrap gap-2">
            {[
              { id: 'all', label: 'All Facilities' },
              { id: 'hospital', label: 'Hospitals' },
              { id: 'shelter', label: 'Relief Shelters' },
              { id: 'police', label: 'Police HQ' },
              { id: 'fire_station', label: 'Fire Dispatch' },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setFilterType(f.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  filterType === f.id
                    ? 'bg-rose-600 text-white shadow-md shadow-rose-600/30'
                    : 'bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Facilities Grid */}
        {loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading nearby facilities...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {facilities.map((fac) => {
              const IconComponent = getIcon(fac.type);
              return (
                <div key={fac.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl hover:border-slate-700 transition-all">
                  
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="p-3 bg-rose-600/10 border border-rose-500/20 rounded-xl text-rose-400">
                        <IconComponent className="w-6 h-6" />
                      </div>
                      <div>
                        <h3 className="font-bold text-white text-sm">{fac.name}</h3>
                        <span className="text-[10px] text-rose-400 font-mono uppercase bg-rose-950 px-2 py-0.5 rounded border border-rose-900">
                          {fac.type.replace('_', ' ')}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2 text-xs text-slate-300">
                    <p className="flex items-center gap-1.5 text-slate-400">
                      <MapPin className="w-4 h-4 text-slate-500 shrink-0" /> {fac.address}
                    </p>
                    <p className="flex items-center gap-1.5 text-emerald-400 font-medium">
                      <Phone className="w-4 h-4 shrink-0" /> {fac.phone}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                    <span className="text-slate-400 font-medium">{fac.capacity}</span>
                    <span className="text-rose-400 font-bold font-mono bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 flex items-center gap-1">
                      <Navigation className="w-3 h-3" /> {fac.distance_km} km
                    </span>
                  </div>

                </div>
              );
            })}
          </div>
        )}

      </main>

      <Footer />
    </div>
  );
}
