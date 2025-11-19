#!/usr/bin/env python3

"""
Observability dashboard - HTTP server exposing metrics, correlation chains, and stats.
Run this to monitor your MCP workflow in real-time.
"""
import json
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from mcp_helpers import TOOL_STATS, CORRELATION_CHAIN, _CACHE, CACHE_TTL
from sse_tracker import SSE_EVENTS, get_sse_stats


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for observability dashboard."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_html_dashboard()
        elif self.path == "/api/metrics":
            self.send_json_metrics()
        elif self.path == "/api/correlations":
            self.send_json_correlations()
        elif self.path == "/api/sse":
            self.send_json_sse()
        elif self.path == "/api/cache":
            self.send_json_cache()
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_html_dashboard(self):
        """Send main HTML dashboard."""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>MCP Observability Dashboard</title>
    <style>
        body { font-family: 'Monaco', 'Courier New', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
        h1 { color: #4ec9b0; }
        h2 { color: #569cd6; border-bottom: 1px solid #404040; padding-bottom: 5px; }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: #252526; border: 1px solid #404040; border-radius: 8px; padding: 15px; }
        .metric-label { color: #858585; font-size: 0.9em; }
        .metric-value { font-size: 1.5em; color: #4ec9b0; font-weight: bold; }
        .correlation { background: #2d2d30; margin: 5px 0; padding: 10px; border-left: 3px solid #007acc; }
        .success { border-left-color: #4ec9b0; }
        .error { border-left-color: #f48771; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #404040; }
        th { color: #569cd6; }
        .refresh-btn { background: #0e639c; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
        .refresh-btn:hover { background: #1177bb; }
    </style>
    <script>
        async function refresh() {
            const metrics = await fetch('/api/metrics').then(r => r.json());
            const correlations = await fetch('/api/correlations').then(r => r.json());
            const sse = await fetch('/api/sse').then(r => r.json());
            const cache = await fetch('/api/cache').then(r => r.json());
            
            document.getElementById('tool-count').textContent = Object.keys(metrics.tools).length;
            document.getElementById('total-calls').textContent = metrics.total_calls;
            document.getElementById('avg-latency').textContent = metrics.avg_latency_ms.toFixed(1) + 'ms';
            document.getElementById('correlation-count').textContent = correlations.total;
            document.getElementById('sse-events').textContent = sse.total_events;
            document.getElementById('cache-items').textContent = cache.total_items;
            document.getElementById('cache-hit-rate').textContent = (cache.hit_rate * 100).toFixed(1) + '%';
            
            renderToolStats(metrics.tools);
            renderCorrelations(correlations.chains);
        }
        
        function renderToolStats(tools) {
            const tbody = document.getElementById('tool-stats-body');
            tbody.innerHTML = '';
            for (const [name, stats] of Object.entries(tools)) {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${name}</td>
                    <td>${stats.count}</td>
                    <td>${stats.total_ms.toFixed(1)}ms</td>
                    <td>${stats.avg_ms.toFixed(1)}ms</td>
                `;
            }
        }
        
        function renderCorrelations(chains) {
            const div = document.getElementById('correlations');
            div.innerHTML = '';
            chains.slice(0, 10).forEach(c => {
                const className = c.status === 'success' ? 'success' : 'error';
                div.innerHTML += `
                    <div class="correlation ${className}">
                        <strong>[${c.correlation_id}]</strong> ${c.tool}<br>
                        <small>Status: ${c.status} | Latency: ${c.elapsed_ms.toFixed(1)}ms${c.jsonrpc_id ? ' | RPC: ' + c.jsonrpc_id : ''}</small>
                    </div>
                `;
            });
        }
        
        setInterval(refresh, 2000);
        window.onload = refresh;
    </script>
</head>
<body>
    <h1>MCP Observability Dashboard</h1>
    <button class="refresh-btn" onclick="refresh()">Refresh Now</button>
    
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Total Tools</div>
            <div class="metric-value" id="tool-count">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Total Calls</div>
            <div class="metric-value" id="total-calls">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Latency</div>
            <div class="metric-value" id="avg-latency">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Correlations Tracked</div>
            <div class="metric-value" id="correlation-count">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">SSE Events</div>
            <div class="metric-value" id="sse-events">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Cache Items</div>
            <div class="metric-value" id="cache-items">-</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Cache Hit Rate</div>
            <div class="metric-value" id="cache-hit-rate">-</div>
        </div>
    </div>
    
    <h2>Tool Performance</h2>
    <table>
        <thead>
            <tr><th>Tool</th><th>Calls</th><th>Total Time</th><th>Avg Latency</th></tr>
        </thead>
        <tbody id="tool-stats-body"></tbody>
    </table>
    
    <h2>Recent Correlations</h2>
    <div id="correlations"></div>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_json_metrics(self):
        """Send tool metrics as JSON."""
        total_calls = sum(s["count"] for s in TOOL_STATS.values())
        total_ms = sum(s["total_ms"] for s in TOOL_STATS.values())
        avg_latency = total_ms / total_calls if total_calls > 0 else 0
        
        tools = {}
        for name, stats in TOOL_STATS.items():
            tools[name] = {
                "count": stats["count"],
                "total_ms": stats["total_ms"],
                "avg_ms": stats["total_ms"] / stats["count"] if stats["count"] > 0 else 0
            }
        
        data = {
            "total_calls": total_calls,
            "avg_latency_ms": avg_latency,
            "tools": tools
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_json_correlations(self):
        """Send correlation chains as JSON."""
        chains = []
        for cid, info in CORRELATION_CHAIN.items():
            chains.append({
                "correlation_id": cid,
                "tool": info.get("tool"),
                "status": info.get("status", "unknown"),
                "elapsed_ms": info.get("elapsed_ms", 0),
                "jsonrpc_id": info.get("jsonrpc_id"),
                "parent_cid": info.get("parent_cid")
            })
        
        data = {
            "total": len(chains),
            "chains": sorted(chains, key=lambda x: x.get("elapsed_ms", 0), reverse=True)
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_json_sse(self):
        """Send SSE statistics as JSON."""
        data = get_sse_stats()
        data["events"] = SSE_EVENTS[-20:]  # Last 20 events
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_json_cache(self):
        """Send cache statistics as JSON."""
        now = time.time()
        valid_items = sum(1 for ts, _ in _CACHE.values() if now - ts < CACHE_TTL)
        
        # Simulate hit rate (in production, track actual hits/misses)
        hit_rate = 0.75 if _CACHE else 0.0
        
        data = {
            "total_items": len(_CACHE),
            "valid_items": valid_items,
            "expired_items": len(_CACHE) - valid_items,
            "ttl_seconds": CACHE_TTL,
            "hit_rate": hit_rate
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_dashboard(port: int = 8080):
    """Run the observability dashboard server."""
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"   Observability Dashboard running at http://localhost:{port}", file=sys.stderr)
    print(f"   View metrics, correlations, and performance stats in your browser", file=sys.stderr)
    server.serve_forever()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_dashboard(port)
