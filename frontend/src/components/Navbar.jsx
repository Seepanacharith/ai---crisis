import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Shield, MessageSquare, AlertCircle, PhoneCall, User, LogOut, LayoutDashboard, FileText, CheckSquare, MapPin, Bell, Activity } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="p-2 bg-rose-600/20 border border-rose-500/40 rounded-xl group-hover:bg-rose-600/30 transition-colors">
              <Shield className="w-6 h-6 text-rose-500" />
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                AI Crisis Companion <span className="text-xs bg-rose-950 text-rose-400 border border-rose-800 px-1.5 py-0.5 rounded font-mono">v1.0</span>
              </span>
              <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase">Disaster Management & Emergency AI</p>
            </div>
          </Link>

          {/* Nav Links */}
          <div className="hidden lg:flex items-center space-x-1 font-medium text-sm text-slate-300">
            <Link to="/dashboard" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/dashboard') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <LayoutDashboard className="w-4 h-4" /> Dashboard
            </Link>
            <Link to="/chat" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/chat') ? 'bg-rose-600 text-white font-semibold shadow-lg shadow-rose-600/30' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <MessageSquare className="w-4 h-4" /> AI Crisis Chat
            </Link>
            <Link to="/disasters" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/disasters') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <FileText className="w-4 h-4" /> Safety Guides
            </Link>
            <Link to="/checklist" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/checklist') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <CheckSquare className="w-4 h-4" /> Checklists
            </Link>
            <Link to="/emergency-services" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/emergency-services') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <MapPin className="w-4 h-4" /> Services
            </Link>
            <Link to="/alerts" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/alerts') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <Bell className="w-4 h-4" /> Alerts
            </Link>
            <Link to="/admin" className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-all ${isActive('/admin') ? 'bg-slate-800 text-rose-400 font-semibold' : 'hover:bg-slate-800/60 hover:text-white'}`}>
              <Activity className="w-4 h-4" /> Admin Metrics
            </Link>
          </div>

          {/* User Actions */}
          <div className="flex items-center space-x-3">
            {isAuthenticated ? (
              <div className="flex items-center space-x-2">
                <Link to="/profile" className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 text-sm font-medium transition-colors">
                  <User className="w-4 h-4 text-rose-400" />
                  <span className="hidden sm:inline">{user?.name || 'Profile'}</span>
                </Link>
                <button onClick={() => { logout(); navigate('/'); }} className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors" title="Logout">
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login" className="text-slate-300 hover:text-white px-3 py-1.5 text-sm font-medium transition-colors">
                  Log In
                </Link>
                <Link to="/register" className="bg-rose-600 hover:bg-rose-500 text-white px-4 py-1.5 rounded-lg text-sm font-semibold transition-all shadow-md shadow-rose-600/20">
                  Register
                </Link>
              </div>
            )}
          </div>

        </div>
      </div>
    </nav>
  );
}
