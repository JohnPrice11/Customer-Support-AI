import { useState, useEffect } from "react";
import { Send, Bot, User, Loader2, Sparkles } from "lucide-react";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");

  useEffect(() => {
    setSessionId(Math.random().toString(36).substring(7));
  }, []);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { id: Date.now(), text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("https://techmart-backend-co6s.onrender.com/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage.text,
        }),
      });

      const data = await response.json();

      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.response || "Sorry, I couldn't process that.",
        sender: "bot"
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("API Error:", error);
      setMessages((prev) => [...prev, { id: Date.now(), text: "⚠️ Connection error. Is the backend running?", sender: "bot" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-gray-100 to-blue-50 font-sans selection:bg-blue-200">

      {/* Glassmorphism Header */}
      <header className="sticky top-0 z-10 bg-white/70 backdrop-blur-md border-b border-gray-200 p-4 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-tr from-blue-600 to-indigo-600 p-2 rounded-xl shadow-lg shadow-blue-200">
            <Bot size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600">
              TechMart Support
            </h1>
            <p className="text-xs text-green-500 font-medium flex items-center gap-1">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              AI Agents Online
            </p>
          </div>
        </div>
        <button
          onClick={() => window.location.href = '/login'}
          className="text-sm font-medium text-slate-500 hover:text-blue-600 transition-colors"
        >
          Sign Out
        </button>
      </header>

      {/* Chat History */}
      <main className="flex-1 overflow-y-auto p-6 space-y-6 max-w-4xl w-full mx-auto pb-32 scroll-smooth">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-slate-400 space-y-4 animate-fade-in-up">
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
              <Sparkles size={40} className="mx-auto mb-4 text-blue-400" />
              <h2 className="text-lg font-semibold text-slate-700 text-center">How can I help you today?</h2>
              <p className="text-sm text-center mt-2 max-w-xs">Ask me about your recent orders, product specifications, or technical issues.</p>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            {msg.sender === "bot" && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center mr-3 mt-1 shadow-sm shrink-0">
                <Bot size={16} className="text-white" />
              </div>
            )}

            <div className={`max-w-[75%] p-4 rounded-3xl shadow-sm text-sm leading-relaxed ${msg.sender === "user"
                ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-tr-sm shadow-blue-200"
                : "bg-white border border-slate-100 text-slate-700 rounded-tl-sm"
              }`}>
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center mr-3 mt-1 shadow-sm shrink-0">
              <Bot size={16} className="text-white" />
            </div>
            <div className="bg-white border border-slate-100 text-slate-500 p-4 rounded-3xl rounded-tl-sm shadow-sm flex items-center gap-3">
              <Loader2 size={18} className="animate-spin text-blue-500" />
              <span className="text-sm font-medium animate-pulse">Agents are analyzing...</span>
            </div>
          </div>
        )}
      </main>

      {/* Floating Input Area */}
      <footer className="fixed bottom-0 w-full bg-gradient-to-t from-slate-50 via-slate-50 to-transparent pb-6 pt-10">
        <form onSubmit={sendMessage} className="max-w-3xl mx-auto px-4">
          <div className="relative flex items-center bg-white shadow-lg shadow-slate-200/50 border border-slate-200 rounded-full p-2 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-transparent transition-all duration-300">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message TechMart Support..."
              className="flex-1 bg-transparent text-slate-800 px-4 py-2 focus:outline-none"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full flex items-center justify-center disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors shadow-md"
            >
              <Send size={18} className="ml-1" />
            </button>
          </div>
          <p className="text-center text-xs text-slate-400 mt-3">AI agents can make mistakes. Please verify important policies.</p>
        </form>
      </footer>

    </div>
  );
}