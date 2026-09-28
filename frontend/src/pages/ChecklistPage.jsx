import React, { useState, useEffect } from 'react';
import { CheckSquare, Save, RotateCcw, Shield, CheckCircle2, AlertCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { checklistAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ChecklistPage() {
  const [disasterType, setDisasterType] = useState('flood');
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    loadChecklist();
  }, [disasterType]);

  const loadChecklist = async () => {
    setLoading(true);
    try {
      const res = await checklistAPI.get(disasterType);
      setItems(res.data);
    } catch (err) {
      console.error("Checklist load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const toggleItem = (id) => {
    setItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, completed: !item.completed } : item
      )
    );
  };

  const handleSave = async () => {
    if (!isAuthenticated) {
      setSaveStatus('Please log in to persist your checklist items across devices.');
      setTimeout(() => setSaveStatus(''), 4000);
      return;
    }

    try {
      await checklistAPI.save(disasterType, items);
      setSaveStatus('Checklist state saved successfully!');
      setTimeout(() => setSaveStatus(''), 3000);
    } catch (err) {
      setSaveStatus('Failed to save checklist.');
    }
  };

  const handleReset = () => {
    setItems((prev) => prev.map((item) => ({ ...item, completed: false })));
  };

  const completedCount = items.filter((i) => i.completed).length;
  const progressPct = items.length > 0 ? Math.round((completedCount / items.length) * 100) : 0;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 py-8 space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
              <CheckSquare className="w-7 h-7 text-emerald-400" /> Emergency Go-Bag Checklist
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Prepare essential survival gear to sustain yourself for 72 hours during evacuation.
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-xl flex items-center gap-1.5 transition-all shadow-md shadow-emerald-600/20"
            >
              <Save className="w-4 h-4" /> Save Checklist
            </button>
            <button
              onClick={handleReset}
              className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs rounded-xl flex items-center gap-1.5 transition-colors"
            >
              <RotateCcw className="w-4 h-4" /> Reset
            </button>
          </div>
        </div>

        {saveStatus && (
          <div className="bg-emerald-950/80 border border-emerald-800 text-emerald-300 px-4 py-2.5 rounded-xl text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-emerald-400" /> {saveStatus}
          </div>
        )}

        {/* Disaster Type Selector */}
        <div className="flex flex-wrap gap-2">
          {['flood', 'earthquake', 'fire', 'cyclone'].map((type) => (
            <button
              key={type}
              onClick={() => setDisasterType(type)}
              className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
                disasterType === type
                  ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {type} Kit
            </button>
          ))}
        </div>

        {/* Progress Bar */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-3">
          <div className="flex justify-between text-xs font-bold">
            <span className="text-white uppercase tracking-wider">{disasterType} Preparation Progress</span>
            <span className="text-emerald-400 font-mono">{completedCount} / {items.length} Ready ({progressPct}%)</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden border border-slate-800">
            <div
              className="bg-emerald-500 h-full transition-all duration-300 rounded-full"
              style={{ width: `${progressPct}%` }}
            ></div>
          </div>
        </div>

        {/* Items Checklist List */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
          {loading ? (
            <div className="text-center py-8 text-xs text-slate-400">Loading checklist...</div>
          ) : (
            items.map((item) => (
              <label
                key={item.id}
                onClick={() => toggleItem(item.id)}
                className={`flex items-start space-x-3 p-3.5 rounded-xl border transition-all cursor-pointer select-none ${
                  item.completed
                    ? 'bg-emerald-950/20 border-emerald-900/50 text-slate-300'
                    : 'bg-slate-950/80 border-slate-800 text-slate-200 hover:border-slate-700'
                }`}
              >
                <input
                  type="checkbox"
                  checked={item.completed}
                  onChange={() => {}}
                  className="mt-0.5 rounded text-emerald-500 focus:ring-0 bg-slate-900 border-slate-700 w-4 h-4 shrink-0 cursor-pointer"
                />
                <span className={`text-xs sm:text-sm font-medium ${item.completed ? 'line-through text-slate-400' : ''}`}>
                  {item.item}
                </span>
              </label>
            ))
          )}
        </div>

      </main>

      <Footer />
    </div>
  );
}
