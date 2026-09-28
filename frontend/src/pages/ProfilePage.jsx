import React from 'react';
import { User, Mail, Shield, Calendar, LogOut, CheckSquare } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8 space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
            <User className="w-7 h-7 text-rose-500" /> User Profile & Settings
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Account preferences and active emergency configuration.
          </p>
        </div>

        {/* Profile Details Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6">
          
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 rounded-2xl bg-rose-600/20 border border-rose-500/30 flex items-center justify-center text-rose-500 font-bold text-xl">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">{user?.name}</h2>
              <span className="inline-block mt-1 px-2.5 py-0.5 rounded text-xs font-mono font-semibold uppercase bg-rose-950 text-rose-300 border border-rose-800">
                {user?.role || 'Standard User'}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
              <span className="text-slate-500 uppercase tracking-wider font-semibold flex items-center gap-1.5">
                <Mail className="w-3.5 h-3.5 text-slate-400" /> Email Address
              </span>
              <p className="text-slate-200 font-medium">{user?.email}</p>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
              <span className="text-slate-500 uppercase tracking-wider font-semibold flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-slate-400" /> Member Since
              </span>
              <p className="text-slate-200 font-medium">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Active Member'}
              </p>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 flex justify-end">
            <button
              onClick={() => {
                logout();
                navigate('/');
              }}
              className="px-4 py-2 bg-rose-950 hover:bg-rose-900 border border-rose-800 text-rose-200 text-xs font-semibold rounded-xl flex items-center gap-2 transition-colors"
            >
              <LogOut className="w-4 h-4" /> Sign Out
            </button>
          </div>

        </div>

      </main>

      <Footer />
    </div>
  );
}
