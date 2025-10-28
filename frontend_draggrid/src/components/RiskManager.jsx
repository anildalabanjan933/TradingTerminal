// ============================================================================
// 📄 FILE: RiskManager.jsx — Final compact P&L + metrics layout
// ============================================================================
import React from "react";

export default function RiskManager() {
  const positions = [
    { symbol: "NIFTY", qty: 1, pnl: 452.3 },
    { symbol: "BANKNIFTY", qty: 2, pnl: -123.4 },
  ];
  const total = positions.reduce((a, b) => a + b.pnl, 0);

  return (
    <div
      className="risk-manager"
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: "#0e0e0e",
        color: "#ccc",
        fontSize: 12,
      }}
    >
      {/* Header */}
      <div
        style={{
          background: "#141414",
          borderBottom: "1px solid #222",
          padding: "2px 8px",
          fontWeight: 600,
          fontSize: 12,
        }}
      >
        📊 Risk Manager (Right Half)
      </div>

      {/* Positions Table */}
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          textAlign: "right",
          marginTop: 4,
        }}
      >
        <thead>
          <tr style={{ color: "#777", fontSize: 11 }}>
            <th style={{ textAlign: "left", padding: "2px 6px" }}>Symbol</th>
            <th>Qty</th>
            <th>P&L (₹)</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((p, i) => (
            <tr key={i}>
              <td
                style={{
                  textAlign: "left",
                  padding: "2px 6px",
                  color: "#aaa",
                }}
              >
                {p.symbol}
              </td>
              <td>{p.qty}</td>
              <td
                style={{
                  color: p.pnl >= 0 ? "#00ff7f" : "#ff4d4d",
                  fontWeight: 600,
                }}
              >
                {p.pnl.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Summary */}
      <div
        style={{
          marginTop: "auto",
          borderTop: "1px solid #222",
          padding: "4px 8px",
          fontWeight: 600,
          color: total >= 0 ? "#00ff7f" : "#ff4d4d",
        }}
      >
        Total P&L : {total.toFixed(2)} ₹
      </div>
    </div>
  );
}
