import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Activity, DollarSign, Target, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Dashboard() {
  const [status, setStatus] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [statusRes, perfRes, configRes] = await Promise.all([
        axios.get(`${API}/bot/status`),
        axios.get(`${API}/bot/performance`),
        axios.get(`${API}/bot/config`)
      ]);
      
      setStatus(statusRes.data);
      setPerformance(perfRes.data);
      setConfig(configRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const stats = [
    {
      title: "Today's P&L",
      value: `₹${performance?.total_pnl?.toFixed(2) || 0}`,
      icon: DollarSign,
      color: performance?.total_pnl >= 0 ? "text-green-600" : "text-red-600",
      bgColor: performance?.total_pnl >= 0 ? "bg-green-50" : "bg-red-50",
      trend: performance?.total_pnl >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />
    },
    {
      title: "Total Trades",
      value: status?.total_trades_today || 0,
      icon: Activity,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      subtitle: `${config?.max_trades_per_day || 0} max/day`
    },
    {
      title: "Win Rate",
      value: `${performance?.win_rate?.toFixed(1) || 0}%`,
      icon: Target,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      subtitle: `${performance?.wins || 0}W / ${performance?.losses || 0}L`
    },
    {
      title: "Avg Win",
      value: `₹${performance?.avg_win?.toFixed(2) || 0}`,
      icon: TrendingUp,
      color: "text-green-600",
      bgColor: "bg-green-50",
      subtitle: `Avg Loss: ₹${Math.abs(performance?.avg_loss || 0).toFixed(2)}`
    }
  ];

  return (
    <div className="space-y-8" data-testid="dashboard">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-slate-900">Dashboard</h2>
        <p className="text-slate-600 mt-1">Overview of your trading bot performance</p>
      </div>

      {/* Status Alert */}
      {!status?.running && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
          <div>
            <h3 className="font-semibold text-amber-900">Bot is currently stopped</h3>
            <p className="text-sm text-amber-700">Click "Start Bot" in the header to begin trading</p>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-600">{stat.title}</p>
                    <p className={`text-2xl font-bold mt-2 ${stat.color}`}>
                      {stat.value}
                    </p>
                    {stat.subtitle && (
                      <p className="text-xs text-slate-500 mt-1">{stat.subtitle}</p>
                    )}
                  </div>
                  <div className={`${stat.bgColor} p-3 rounded-lg`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
                {stat.trend && (
                  <div className="flex items-center mt-3 space-x-1 text-sm">
                    <span className={stat.color}>{stat.trend}</span>
                    <span className="text-slate-600">Today</span>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Configuration Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Current Configuration</CardTitle>
            <CardDescription>Active bot settings</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <ConfigItem label="Trading Mode" value={config?.trading_mode} badge />
              <ConfigItem label="Index" value={config?.index_name} />
              <ConfigItem label="Lot Size" value={config?.lot_size} />
              <ConfigItem label="Stop Loss" value={`${config?.stop_loss_percent}%`} />
              <ConfigItem label="Trailing Stop" value={`${config?.trailing_stop_percent}%`} />
              <ConfigItem label="Max Loss/Day" value={`₹${config?.max_loss_per_day}`} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Strategy Settings</CardTitle>
            <CardDescription>SuperTrend parameters</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <ConfigItem label="Period" value={config?.supertrend_period} />
              <ConfigItem label="Multiplier" value={config?.supertrend_multiplier} />
              <ConfigItem label="Candle Timeframe" value={`${config?.candle_timeframe} min`} />
              <ConfigItem label="Polling Interval" value={`${config?.polling_interval} sec`} />
              <ConfigItem label="Strike Interval" value={config?.strike_interval} />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bot Status */}
      <Card>
        <CardHeader>
          <CardTitle>Bot Status</CardTitle>
          <CardDescription>Current operational status</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-slate-600">Status</span>
              <Badge variant={status?.running ? "default" : "secondary"}>
                {status?.running ? "Running" : "Stopped"}
              </Badge>
            </div>
            {status?.started_at && (
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-600">Started At</span>
                <span className="text-sm text-slate-900">
                  {new Date(status.started_at).toLocaleString()}
                </span>
              </div>
            )}
            {status?.pid && (
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-600">Process ID</span>
                <span className="text-sm text-slate-900 font-mono">{status.pid}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ConfigItem({ label, value, badge = false }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
      <span className="text-sm font-medium text-slate-600">{label}</span>
      {badge ? (
        <Badge variant={value === "live" ? "destructive" : "default"}>
          {value}
        </Badge>
      ) : (
        <span className="text-sm font-semibold text-slate-900">{value}</span>
      )}
    </div>
  );
}