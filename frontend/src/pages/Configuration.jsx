import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Save, RefreshCw } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Configuration() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API}/bot/config`);
      setConfig(response.data);
    } catch (error) {
      toast.error("Failed to load configuration");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.post(`${API}/bot/config`, config);
      toast.success("Configuration saved successfully!");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to save configuration");
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setConfig({ ...config, [field]: value });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8" data-testid="configuration-page">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Configuration</h2>
          <p className="text-slate-600 mt-1">Manage your trading bot settings</p>
        </div>
        <div className="flex space-x-3">
          <Button
            onClick={fetchConfig}
            variant="outline"
            data-testid="refresh-config-btn"
            className="gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </Button>
          <Button
            onClick={handleSave}
            disabled={saving}
            data-testid="save-config-btn"
            className="gap-2"
          >
            <Save className="w-4 h-4" />
            {saving ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Dhan API Credentials */}
        <Card>
          <CardHeader>
            <CardTitle>Dhan API Credentials</CardTitle>
            <CardDescription>Your broker API authentication</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="client-id">Client ID</Label>
              <Input
                id="client-id"
                data-testid="client-id-input"
                value={config?.dhan_client_id || ""}
                onChange={(e) => handleChange("dhan_client_id", e.target.value)}
                placeholder="Enter your Dhan Client ID"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="access-token">Access Token</Label>
              <Input
                id="access-token"
                data-testid="access-token-input"
                type="password"
                value={config?.dhan_access_token || ""}
                onChange={(e) => handleChange("dhan_access_token", e.target.value)}
                placeholder="Enter your Dhan Access Token"
              />
            </div>
          </CardContent>
        </Card>

        {/* Trading Configuration */}
        <Card>
          <CardHeader>
            <CardTitle>Trading Configuration</CardTitle>
            <CardDescription>Basic trading settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="trading-mode">Trading Mode</Label>
              <Select
                value={config?.trading_mode}
                onValueChange={(value) => handleChange("trading_mode", value)}
              >
                <SelectTrigger id="trading-mode" data-testid="trading-mode-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="paper">Paper Trading (Simulated)</SelectItem>
                  <SelectItem value="live">Live Trading (Real Money)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="index">Index</Label>
              <Select
                value={config?.index_name}
                onValueChange={(value) => handleChange("index_name", value)}
              >
                <SelectTrigger id="index" data-testid="index-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="NIFTY">NIFTY</SelectItem>
                  <SelectItem value="BANKNIFTY">BANKNIFTY (Future)</SelectItem>
                  <SelectItem value="FINNIFTY">FINNIFTY (Future)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="lot-size">Lot Size</Label>
              <Input
                id="lot-size"
                data-testid="lot-size-input"
                type="number"
                value={config?.lot_size || 0}
                onChange={(e) => handleChange("lot_size", parseInt(e.target.value))}
                min="1"
                max="100"
              />
            </div>
          </CardContent>
        </Card>

        {/* Risk Management */}
        <Card>
          <CardHeader>
            <CardTitle>Risk Management</CardTitle>
            <CardDescription>Control your risk exposure</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="stop-loss">Stop Loss (%)</Label>
              <Input
                id="stop-loss"
                data-testid="stop-loss-input"
                type="number"
                value={config?.stop_loss_percent || 0}
                onChange={(e) => handleChange("stop_loss_percent", parseFloat(e.target.value))}
                min="5"
                max="50"
                step="0.1"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="trailing-stop">Trailing Stop (%)</Label>
              <Input
                id="trailing-stop"
                data-testid="trailing-stop-input"
                type="number"
                value={config?.trailing_stop_percent || 0}
                onChange={(e) => handleChange("trailing_stop_percent", parseFloat(e.target.value))}
                min="3"
                max="30"
                step="0.1"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="max-trades">Max Trades per Day</Label>
              <Input
                id="max-trades"
                data-testid="max-trades-input"
                type="number"
                value={config?.max_trades_per_day || 0}
                onChange={(e) => handleChange("max_trades_per_day", parseInt(e.target.value))}
                min="1"
                max="100"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="max-loss">Max Loss per Day (₹)</Label>
              <Input
                id="max-loss"
                data-testid="max-loss-input"
                type="number"
                value={config?.max_loss_per_day || 0}
                onChange={(e) => handleChange("max_loss_per_day", parseFloat(e.target.value))}
                min="1000"
                step="1000"
              />
            </div>
          </CardContent>
        </Card>

        {/* SuperTrend Strategy */}
        <Card>
          <CardHeader>
            <CardTitle>SuperTrend Strategy</CardTitle>
            <CardDescription>Strategy parameters</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="period">Period</Label>
              <Input
                id="period"
                data-testid="period-input"
                type="number"
                value={config?.supertrend_period || 0}
                onChange={(e) => handleChange("supertrend_period", parseInt(e.target.value))}
                min="3"
                max="30"
              />
              <p className="text-xs text-slate-500">Lower = more signals, Higher = fewer signals</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="multiplier">Multiplier</Label>
              <Input
                id="multiplier"
                data-testid="multiplier-input"
                type="number"
                value={config?.supertrend_multiplier || 0}
                onChange={(e) => handleChange("supertrend_multiplier", parseFloat(e.target.value))}
                min="1"
                max="10"
                step="0.1"
              />
              <p className="text-xs text-slate-500">Lower = closer to price, Higher = further from price</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="timeframe">Candle Timeframe (minutes)</Label>
              <Select
                value={config?.candle_timeframe?.toString()}
                onValueChange={(value) => handleChange("candle_timeframe", parseInt(value))}
              >
                <SelectTrigger id="timeframe" data-testid="timeframe-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1 minute</SelectItem>
                  <SelectItem value="3">3 minutes</SelectItem>
                  <SelectItem value="5">5 minutes</SelectItem>
                  <SelectItem value="15">15 minutes</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="polling">Polling Interval (seconds)</Label>
              <Input
                id="polling"
                data-testid="polling-input"
                type="number"
                value={config?.polling_interval || 0}
                onChange={(e) => handleChange("polling_interval", parseInt(e.target.value))}
                min="1"
                max="60"
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Warning Note */}
      <Card className="bg-amber-50 border-amber-200">
        <CardContent className="p-4">
          <p className="text-sm text-amber-900">
            <strong>Note:</strong> Changes to configuration require a bot restart to take effect. 
            Stop the bot, save changes, then start it again.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}