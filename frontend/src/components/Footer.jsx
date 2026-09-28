import React from 'react';
import { Shield, Heart, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-800 text-slate-400 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        
        <div className="space-y-4 md:col-span-1">
          <div className="flex items-center space-x-2">
            <Shield className="w-6 h-6 text-rose-500" />
            <span className="text-lg font-bold text-white">AI Crisis Companion</span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            AI-powered disaster management & emergency assistance platform utilizing advanced Retrieval-Augmented Generation (RAG) and Gemini LLM integration.
          </p>
          <p className="text-[11px] text-slate-500">
            © 2026 AI Crisis Companion. Production Architecture Portfolio Project.
          </p>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Quick Navigation</h4>
          <ul className="space-y-2 text-xs">
            <li><Link to="/dashboard" className="hover:text-rose-400 transition-colors">Emergency Dashboard</Link></li>
            <li><Link to="/chat" className="hover:text-rose-400 transition-colors">AI Crisis Chat</Link></li>
            <li><Link to="/disasters" className="hover:text-rose-400 transition-colors">Disaster Safety Guides</Link></li>
            <li><Link to="/checklist" className="hover:text-rose-400 transition-colors">Preparedness Checklists</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Emergency Resources</h4>
          <ul className="space-y-2 text-xs">
            <li><Link to="/emergency-services" className="hover:text-rose-400 transition-colors">Nearby Shelters & Hospitals</Link></li>
            <li><Link to="/alerts" className="hover:text-rose-400 transition-colors">Real-Time Disaster Alerts</Link></li>
            <li><Link to="/admin" className="hover:text-rose-400 transition-colors">System Metrics & Performance</Link></li>
            <li><a href="/api/v1/health" target="_blank" rel="noreferrer" className="hover:text-rose-400 flex items-center gap-1">Backend Health Check <ExternalLink className="w-3 h-3"/></a></li>
          </ul>
        </div>

        <div className="space-y-3">
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Safety Notice</h4>
          <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs leading-relaxed text-slate-400">
            This platform is an emergency guidance companion. During active disaster events, always follow instructions from official local emergency response teams.
          </div>
        </div>

      </div>
    </footer>
  );
}
