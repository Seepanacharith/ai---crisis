import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Send, Bot, User, Copy, Check, RefreshCw, Trash2, Globe, Shield, BookOpen, Sparkles, Layers, AlertCircle, Zap } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import Navbar from '../components/Navbar';
import SourceModal from '../components/SourceModal';
import { chatAPI } from '../services/api';

const SUGGESTED_QUESTIONS = [
  "What should I do during a flood?",
  "What should I keep in an emergency kit?",
  "What should I do during an earthquake?",
  "How should I evacuate during a fire?",
  "How do I prepare for a cyclone?",
  "What emergency supplies should I carry?",
];

export default function AIChatPage() {
  const [searchParams] = useSearchParams();
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Welcome to AI Crisis Companion. I am your specialized emergency assistance system. Ask me any safety question or select a disaster category.',
      sources: [],
      latency: null,
      cache_hit: false
    }
  ]);
  const [input, setInput] = useState('');
  const [disasterType, setDisasterType] = useState('all');
  const [language, setLanguage] = useState('en');
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [selectedSources, setSelectedSources] = useState(null);
  const [isSourceModalOpen, setIsSourceModalOpen] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    const initialQuery = searchParams.get('query');
    if (initialQuery) {
      handleSendMessage(initialQuery);
    }
  }, [searchParams]);

  const handleSendMessage = async (textToSend = input) => {
    const messageText = textToSend.trim();
    if (!messageText || isTyping) return;

    const userMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      // Execute stream request using SSE fetch
      const response = await fetch('/api/v1/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
        },
        body: JSON.stringify({
          message: messageText,
          disaster_type: disasterType,
          language: language
        })
      });

      if (!response.ok) {
        throw new Error("API Response Error");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let assistantMsgId = (Date.now() + 1).toString();
      let streamedContent = "";

      // Add placeholder assistant message
      setMessages((prev) => [
        ...prev,
        {
          id: assistantMsgId,
          role: 'assistant',
          content: '',
          sources: [],
          latency: null,
          cache_hit: false
        }
      ]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunkStr = decoder.decode(value, { stream: true });
        const lines = chunkStr.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.replace("data: ", "").trim();
            if (dataStr === "[DONE]") {
              break;
            }
            try {
              const parsed = JSON.parse(dataStr);
              if (parsed.token) {
                streamedContent += parsed.token;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMsgId ? { ...msg, content: streamedContent } : msg
                  )
                );
              }
            } catch (e) {
              // Ignore partial JSON parse errors during stream
            }
          }
        }
      }

      // Fetch standard JSON for full sources & timing details
      const jsonRes = await chatAPI.sendQuery({
        message: messageText,
        disaster_type: disasterType,
        language: language
      });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMsgId
            ? {
                ...msg,
                content: jsonRes.data.response,
                sources: jsonRes.data.sources,
                latency: jsonRes.data.latency,
                cache_hit: jsonRes.data.cache_hit
              }
            : msg
        )
      );

    } catch (err) {
      console.error("Chat Error:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: '⚠️ Safety Service Alert: Connection temporarily interrupted. Please follow official local authority guidelines.',
          sources: [],
          latency: null,
          cache_hit: false
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClearHistory = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Conversation history cleared. Ready for your emergency queries.',
        sources: [],
        latency: null,
        cache_hit: false
      }
    ]);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar />

      <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full px-4 sm:px-6 py-6 space-y-4">
        
        {/* Controls Bar (Disaster Selector + Language Selector) */}
        <div className="bg-slate-900 border border-slate-800 p-3 rounded-2xl flex flex-wrap items-center justify-between gap-3 text-xs">
          
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-rose-500" />
            <span className="font-semibold text-slate-300">Disaster Context:</span>
            <select
              value={disasterType}
              onChange={(e) => setDisasterType(e.target.value)}
              className="bg-slate-950 border border-slate-700 text-white rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-rose-500"
            >
              <option value="all">All Disasters</option>
              <option value="flood">Flood</option>
              <option value="earthquake">Earthquake</option>
              <option value="fire">Fire</option>
              <option value="cyclone">Cyclone</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <Globe className="w-4 h-4 text-rose-400" />
            <span className="font-semibold text-slate-300">Language:</span>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-slate-950 border border-slate-700 text-white rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-rose-500 font-medium"
            >
              <option value="en">English</option>
              <option value="hi">Hindi (हिंदी)</option>
              <option value="te">Telugu (తెలుగు)</option>
            </select>

            <button
              onClick={handleClearHistory}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors ml-2"
              title="Clear Conversation"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>

        </div>

        {/* Chat Messages Stream */}
        <div className="flex-1 bg-slate-900/60 border border-slate-800 rounded-2xl p-4 sm:p-6 overflow-y-auto space-y-6 min-h-[500px] max-h-[650px] shadow-inner">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 sm:gap-4 ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-rose-600/20 border border-rose-500/30 flex items-center justify-center text-rose-500 shrink-0">
                  <Bot className="w-5 h-5" />
                </div>
              )}

              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-sm leading-relaxed space-y-3 ${
                  msg.role === 'user'
                    ? 'bg-rose-600 text-white rounded-tr-none shadow-md shadow-rose-600/20'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none'
                }`}
              >
                <div className="prose prose-invert max-w-none text-sm">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>

                {/* Assistant Footer (Sources, Latency, Copy) */}
                {msg.role === 'assistant' && msg.id !== 'welcome' && (
                  <div className="pt-2 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-400 font-mono">
                    <div className="flex items-center space-x-2">
                      {msg.cache_hit && (
                        <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-1.5 py-0.5 rounded">
                          REDIS CACHE HIT
                        </span>
                      )}
                      {msg.latency && (
                        <span>
                          {msg.latency.total_ms}ms (LLM: {msg.latency.llm_ms}ms)
                        </span>
                      )}
                    </div>

                    <div className="flex items-center space-x-2">
                      {msg.sources && msg.sources.length > 0 && (
                        <button
                          onClick={() => {
                            setSelectedSources(msg.sources);
                            setIsSourceModalOpen(true);
                          }}
                          className="flex items-center gap-1 text-rose-400 hover:underline font-medium"
                        >
                          <BookOpen className="w-3 h-3" /> Sources ({msg.sources.length})
                        </button>
                      )}

                      <button
                        onClick={() => handleCopy(msg.content, msg.id)}
                        className="p-1 hover:text-white rounded"
                        title="Copy Response"
                      >
                        {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0">
                  <User className="w-5 h-5" />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="flex items-center space-x-3 text-xs text-rose-400 font-medium">
              <Bot className="w-4 h-4 animate-bounce" />
              <span>AI is typing emergency response...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          <span className="text-slate-500 font-semibold shrink-0 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-rose-400" /> Suggested:
          </span>
          {SUGGESTED_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(q)}
              className="bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-full shrink-0 transition-colors whitespace-nowrap"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Chat Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="bg-slate-900 border border-slate-800 p-2.5 rounded-2xl flex items-center gap-2 shadow-xl"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your disaster or emergency query..."
            className="flex-1 bg-transparent px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="p-3 bg-rose-600 hover:bg-rose-500 disabled:opacity-40 text-white rounded-xl transition-all shadow-md shadow-rose-600/20"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>

      </div>

      <SourceModal
        isOpen={isSourceModalOpen}
        onClose={() => setIsSourceModalOpen(false)}
        sources={selectedSources}
      />
    </div>
  );
}
