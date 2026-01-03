import { Link, useLocation } from "react-router-dom";
import { Activity, Settings, TrendingUp, FileText, Play, Square } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import axios from "axios";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Layout({ children }) {
  const location = useLocation();
  const [botStatus, setBotStatus] = useState({ running: false });
  const [loading, setLoading] = useState(false);

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API}/bot/status`);
      setBotStatus(response.data);
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStartBot = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/bot/start`);
      toast.success("Bot started successfully!");
      await fetchStatus();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to start bot");
    } finally {
      setLoading(false);
    }
  };

  const handleStopBot = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/bot/stop`);
      toast.success("Bot stopped successfully!");
      await fetchStatus();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to stop bot");
    } finally {
      setLoading(false);
    }
  };

  const navItems = [
    { path: "/", label: "Dashboard", icon: Activity },
    { path: "/config", label: "Configuration", icon: Settings },
    { path: "/trades", label: "Trades", icon: TrendingUp },
    { path: "/logs", label: "Logs", icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50 backdrop-blur-sm bg-white/90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">Trading Bot</h1>
                <p className="text-xs text-slate-500">Index Options Manager</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Bot Status */}
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  botStatus.running ? "bg-green-500 animate-pulse" : "bg-red-500"
                }`} />
                <span className="text-sm font-medium text-slate-700">
                  {botStatus.running ? "Running" : "Stopped"}
                </span>
              </div>

              {/* Start/Stop Button */}
              {botStatus.running ? (
                <Button
                  onClick={handleStopBot}
                  disabled={loading}
                  size="sm"
                  variant="destructive"
                  data-testid="stop-bot-btn"
                  className="gap-2"
                >
                  <Square className="w-4 h-4" />
                  Stop Bot
                </Button>
              ) : (
                <Button
                  onClick={handleStartBot}
                  disabled={loading}
                  size="sm"
                  data-testid="start-bot-btn"
                  className="gap-2 bg-green-600 hover:bg-green-700"
                >
                  <Play className="w-4 h-4" />
                  Start Bot
                </Button>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-slate-200 min-h-[calc(100vh-4rem)] p-4">
          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  data-testid={`nav-${item.label.toLowerCase()}`}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                    isActive
                      ? "bg-indigo-50 text-indigo-700 font-medium"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}