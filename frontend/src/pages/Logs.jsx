import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RefreshCw, Terminal } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Logs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchLogs();
    
    if (autoRefresh) {
      const interval = setInterval(fetchLogs, 3000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchLogs = async () => {
    try {
      const response = await axios.get(`${API}/bot/logs?lines=200`);
      setLogs(response.data.logs);
    } catch (error) {
      console.error("Error fetching logs:", error);
    } finally {
      setLoading(false);
    }
  };

  const getLogColor = (line) => {
    if (line.includes("ERROR")) return "text-red-600";
    if (line.includes("WARNING")) return "text-amber-600";
    if (line.includes("INFO")) return "text-blue-600";
    if (line.includes("SIGNAL")) return "text-purple-600 font-semibold";
    if (line.includes("BUY") || line.includes("SELL")) return "text-green-600 font-semibold";
    return "text-slate-700";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8" data-testid="logs-page">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Logs</h2>
          <p className="text-slate-600 mt-1">Real-time bot activity logs</p>
        </div>
        <div className="flex space-x-3">
          <Button
            onClick={() => setAutoRefresh(!autoRefresh)}
            variant={autoRefresh ? "default" : "outline"}
            data-testid="auto-refresh-btn"
            className="gap-2"
          >
            {autoRefresh ? "Auto-refresh ON" : "Auto-refresh OFF"}
          </Button>
          <Button onClick={fetchLogs} variant="outline" className="gap-2" data-testid="refresh-logs-btn">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Logs Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Terminal className="w-5 h-5" />
            <CardTitle>Bot Logs</CardTitle>
          </div>
          <CardDescription>
            {logs.length > 0 ? `Showing last ${logs.length} log entries` : "No logs available"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {logs.length > 0 ? (
            <div className="bg-slate-900 rounded-lg p-4 overflow-auto max-h-[600px]">
              <div className="font-mono text-xs space-y-0.5">
                {logs.map((log, index) => (
                  <div
                    key={index}
                    className={`${getLogColor(log)} whitespace-pre-wrap break-all`}
                    style={{ color: "inherit" }}
                  >
                    {log}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <Terminal className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500">No logs available</p>
              <p className="text-sm text-slate-400 mt-1">Start the bot to see logs</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Legend */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Log Colors</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-600 rounded"></div>
              <span>Error</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-amber-600 rounded"></div>
              <span>Warning</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-600 rounded"></div>
              <span>Info</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-600 rounded"></div>
              <span>Signal</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-600 rounded"></div>
              <span>Trade</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}