import React, { useState, useEffect } from 'react';
import { MessageSquare, Trash2, Calendar, Shield, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { chatAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      loadHistory();
    }
  }, [isAuthenticated]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const res = await chatAPI.getHistory();
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to load chat history:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    try {
      await chatAPI.clearHistory();
      setHistory([]);
    } catch (err) {
      console.error("Failed to clear chat history:", err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 py-8 space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-2">
              <MessageSquare className="w-7 h-7 text-rose-500" /> Saved Conversations History
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Review past crisis queries, AI advice, and emergency recommendations.
            </p>
          </div>

          {history.length > 0 && (
            <button
              onClick={handleClear}
              className="px-3.5 py-2 bg-slate-800 hover:bg-rose-950 text-slate-300 hover:text-rose-400 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors border border-slate-700 hover:border-rose-900"
            >
              <Trash2 className="w-4 h-4" /> Clear All History
            </button>
          )}
        </div>

        {!isAuthenticated ? (
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl text-center space-y-4">
            <Shield className="w-10 h-10 text-rose-500 mx-auto" />
            <h3 className="text-lg font-bold text-white">Log in to view saved conversations</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Creating an account allows your crisis chat sessions and checklists to be saved securely.
            </p>
            <Link to="/login" className="inline-block px-6 py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-rose-600/20">
              Sign In
            </Link>
          </div>
        ) : loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading conversation history...</div>
        ) : history.length === 0 ? (
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl text-center space-y-3 text-slate-400 text-xs">
            <MessageSquare className="w-8 h-8 text-slate-600 mx-auto" />
            <p>No saved conversation history found.</p>
            <Link to="/chat" className="inline-block px-4 py-2 bg-rose-600 text-white font-semibold rounded-lg">
              Start New Chat
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((conv) => (
              <div key={conv.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="flex justify-between items-start">
                  <h3 className="text-base font-bold text-white">{conv.title}</h3>
                  <span className="text-xs text-slate-500 flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5" /> {new Date(conv.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="text-xs text-slate-400">
                  {conv.messages.length} message exchange(s) recorded.
                </div>
                <Link to={`/chat?conv=${conv.id}`} className="inline-flex items-center gap-1.5 text-xs text-rose-400 hover:underline font-semibold pt-2">
                  Continue Thread <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        )}

      </main>

      <Footer />
    </div>
  );
}
