import React from 'react';
import { AlertTriangle, PhoneCall } from 'lucide-react';

export default function EmergencyBanner() {
  return (
    <div className="bg-rose-950/80 border-b border-rose-800 text-rose-200 px-4 py-2 text-xs md:text-sm flex flex-wrap items-center justify-between gap-2 shadow-inner">
      <div className="flex items-center space-x-2 font-medium">
        <AlertTriangle className="w-4 h-4 text-rose-400 animate-pulse shrink-0" />
        <span>
          <strong>Emergency Disclaimer:</strong> For immediate life-threatening danger, follow official local authorities.
        </span>
      </div>
      <div className="flex items-center space-x-4 shrink-0 font-semibold text-white">
        <span className="flex items-center gap-1 bg-rose-800/80 px-2 py-0.5 rounded border border-rose-600">
          <PhoneCall className="w-3 h-3 text-rose-300" /> Helpline: 112 / 911 / 108
        </span>
      </div>
    </div>
  );
}
