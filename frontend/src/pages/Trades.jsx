import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { RefreshCw, TrendingUp, TrendingDown } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Trades() {
  const [trades, setTrades] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [tradesRes, perfRes] = await Promise.all([
        axios.get(`${API}/bot/trades`),
        axios.get(`${API}/bot/performance`)
      ]);
      
      setTrades(tradesRes.data.trades);
      setPerformance(perfRes.data);
    } catch (error) {
      console.error("Error fetching trades:", error);
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

  return (
    <div className="space-y-8" data-testid="trades-page">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Trades</h2>
          <p className="text-slate-600 mt-1">View your trading history and performance</p>
        </div>
        <Button onClick={fetchData} variant="outline" className="gap-2" data-testid="refresh-trades-btn">
          <RefreshCw className="w-4 h-4" />
          Refresh
        </Button>
      </div>

      {/* Performance Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Total P&L</p>
                <p className={`text-2xl font-bold mt-2 ${
                  performance?.total_pnl >= 0 ? "text-green-600" : "text-red-600"
                }`}>
                  ₹{performance?.total_pnl?.toFixed(2) || 0}
                </p>
              </div>
              {performance?.total_pnl >= 0 ? (
                <TrendingUp className="w-8 h-8 text-green-600" />
              ) : (
                <TrendingDown className="w-8 h-8 text-red-600" />
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <p className="text-sm font-medium text-slate-600">Win Rate</p>
            <p className="text-2xl font-bold text-indigo-600 mt-2">
              {performance?.win_rate?.toFixed(1) || 0}%
            </p>
            <p className="text-xs text-slate-500 mt-1">
              {performance?.wins || 0} wins / {performance?.losses || 0} losses
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <p className="text-sm font-medium text-slate-600">Avg Win</p>
            <p className="text-2xl font-bold text-green-600 mt-2">
              ₹{performance?.avg_win?.toFixed(2) || 0}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <p className="text-sm font-medium text-slate-600">Avg Loss</p>
            <p className="text-2xl font-bold text-red-600 mt-2">
              ₹{Math.abs(performance?.avg_loss || 0).toFixed(2)}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Trades Table */}
      <Card>
        <CardHeader>
          <CardTitle>Trade History</CardTitle>
          <CardDescription>
            {trades.length > 0 ? `${trades.length} trades today` : "No trades yet today"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {trades.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Time</TableHead>
                    <TableHead>Symbol</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Price</TableHead>
                    <TableHead>Qty</TableHead>
                    <TableHead>P&L</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {trades.map((trade, index) => (
                    <TableRow key={index} data-testid={`trade-row-${index}`}>
                      <TableCell className="font-mono text-sm">
                        {new Date(trade.timestamp).toLocaleTimeString()}
                      </TableCell>
                      <TableCell className="font-medium">{trade.symbol}</TableCell>
                      <TableCell>
                        <Badge variant={trade.order_type === "BUY" ? "default" : "secondary"}>
                          {trade.order_type}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-mono">₹{trade.price.toFixed(2)}</TableCell>
                      <TableCell>{trade.quantity}</TableCell>
                      <TableCell>
                        {trade.pnl !== undefined && trade.pnl !== null ? (
                          <span className={trade.pnl >= 0 ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
                            {trade.pnl >= 0 ? "+" : ""}₹{trade.pnl.toFixed(2)}
                          </span>
                        ) : (
                          <span className="text-slate-400">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-xs">
                          {trade.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-slate-500">No trades to display</p>
              <p className="text-sm text-slate-400 mt-1">Start the bot to begin trading</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}