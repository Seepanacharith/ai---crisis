import React from 'react';
import { X, FileText, Database, Layers } from 'lucide-react';

export default function SourceModal({ isOpen, onClose, sources }) {
  if (!isOpen || !sources || sources.length === 0) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[85vh] flex flex-col">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-2">
            <Database className="w-5 h-5 text-rose-500" />
            <h3 className="text-lg font-bold text-white">Retrieved RAG Sources</h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Sources List */}
        <div className="overflow-y-auto space-y-4 py-4 pr-1 flex-1">
          {sources.map((src, idx) => (
            <div key={idx} className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-rose-400 font-semibold">
                <span className="flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-rose-500" /> {src.source || 'Knowledge Document'}
                </span>
                {src.disaster_type && (
                  <span className="bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded text-[10px] uppercase font-mono">
                    {src.disaster_type}
                  </span>
                )}
              </div>
              
              {src.section && (
                <p className="text-xs text-slate-300 font-medium flex items-center gap-1">
                  <Layers className="w-3.5 h-3.5 text-slate-500" /> Section: {src.section}
                </p>
              )}

              {src.snippet && (
                <div className="bg-slate-900/90 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 font-mono leading-relaxed">
                  "{src.snippet}"
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-slate-800 text-right">
          <button onClick={onClose} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg">
            Close Citations
          </button>
        </div>

      </div>
    </div>
  );
}
