// =============================================================================
// 📄 FILE: RightColumnSkeleton.jsx
// Connects Watchlist/Scanner placeholders to live backend feed
// =============================================================================

import React, { useEffect, useState } from "react";
import { getWatchlist } from "../api/backend";

export default function RightColumnSkeleton() {
  const [watchlist, setWatchlist] = useState([]);

  // Fetch watchlist every 5 seconds
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await getWatchlist();
        if (res?.watchlist) setWatchlist(res.watchlist);
      } catch (err) {
        console.error("❌ Error fetching watchlist:", err);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="right-column-inner">
      <div className="panel-header">🔍 Scanner Panel</div>

      <div className="panel-header">📋 Watchlist</div>
      <div className="watchlist-container">
        {watchlist.length === 0 ? (
          <p className="placeholder-text">Loading watchlist...</p>
        ) : (
          <table className="watchlist-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Price</th>
                <th>Change</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {watchlist.map((item, idx) => (
                <tr key={idx}>
                  <td>{item.symbol}</td>
                  <td>{item.price}</td>
                  <td
                    style={{
                      color: item.change >= 0 ? "#00ff7f" : "#ff4d4d",
                    }}
                  >
                    {item.change}
                  </td>
                  <td
                    style={{
                      color: item.percent >= 0 ? "#00ff7f" : "#ff4d4d",
                    }}
                  >
                    {item.percent}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
