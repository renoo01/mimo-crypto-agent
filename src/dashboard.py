"""Web Dashboard for MiMo Crypto Agent"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import asyncio
import threading
import time
import logging

logger = logging.getLogger(__name__)

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MiMo Crypto Agent — Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a0f; color: #e0e0e0; }
        .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; text-align: center; border-bottom: 2px solid #FF6900; }
        .header h1 { font-size: 2rem; color: #FF6900; margin-bottom: 0.5rem; }
        .header p { color: #888; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; padding: 2rem; max-width: 1200px; margin: 0 auto; }
        .stat-card { background: #1a1a2e; border-radius: 12px; padding: 1.5rem; border: 1px solid #333; }
        .stat-card h3 { color: #FF6900; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem; }
        .stat-card .value { font-size: 2rem; font-weight: bold; color: #fff; }
        .stat-card .value.green { color: #00ff88; }
        .stat-card .value.orange { color: #FF6900; }
        .agents { max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem; }
        .agent-card { background: #1a1a2e; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid #FF6900; }
        .agent-card h3 { color: #fff; margin-bottom: 0.5rem; }
        .agent-card .status { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; }
        .agent-card .status.active { background: rgba(0,255,136,0.2); color: #00ff88; }
        .agent-card .desc { color: #888; margin-top: 0.5rem; }
        .footer { text-align: center; padding: 2rem; color: #555; border-top: 1px solid #333; }
        .footer a { color: #FF6900; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 MiMo Crypto Agent</h1>
        <p>AI-Powered On-Chain Intelligence Platform | Powered by Xiaomi MiMo V2.5</p>
    </div>
    <div class="stats">
        <div class="stat-card">
            <h3>Total Queries</h3>
            <div class="value orange" id="total-queries">0</div>
        </div>
        <div class="stat-card">
            <h3>Tokens Consumed</h3>
            <div class="value green" id="total-tokens">0</div>
        </div>
        <div class="stat-card">
            <h3>Active Agents</h3>
            <div class="value" id="active-agents">5</div>
        </div>
        <div class="stat-card">
            <h3>Avg Response Time</h3>
            <div class="value" id="avg-latency">0ms</div>
        </div>
    </div>
    <div class="agents">
        <h2 style="color:#fff;margin-bottom:1rem;">Active Agents</h2>
        <div class="agent-card">
            <h3>🔥 Memecoin Sniper</h3>
            <span class="status active">ACTIVE</span>
            <div class="desc">Real-time token launch detection, rug-pull analysis, momentum scoring</div>
        </div>
        <div class="agent-card">
            <h3>🐋 Whale Tracker</h3>
            <span class="status active">ACTIVE</span>
            <div class="desc">Monitor top wallets, smart money flows, large transfer alerts</div>
        </div>
        <div class="agent-card">
            <h3>📊 Polymarket Analyzer</h3>
            <span class="status active">ACTIVE</span>
            <div class="desc">Odds comparison, value bet detection, news correlation</div>
        </div>
        <div class="agent-card">
            <h3>🎯 Airdrop Hunter</h3>
            <span class="status active">ACTIVE</span>
            <div class="desc">Eligibility checking, task prioritization, Sybil scoring</div>
        </div>
        <div class="agent-card">
            <h3>📰 Sentiment Engine</h3>
            <span class="status active">ACTIVE</span>
            <div class="desc">Multi-source sentiment analysis (X/Twitter, news, on-chain)</div>
        </div>
    </div>
    <div class="footer">
        Built with ❤️ using <a href="https://mimo.xiaomi.com">Xiaomi MiMo V2.5</a> |
        <a href="https://platform.xiaomimimo.com">MiMo API Platform</a>
    </div>
</body>
</html>"""


class Dashboard:
    """Simple web dashboard."""

    def __init__(self, agent, host="0.0.0.0", port=5000):
        self.agent = agent
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template_string(DASHBOARD_HTML)

        @self.app.route("/api/stats")
        def stats():
            return jsonify(self.agent.stats)

        @self.app.route("/api/health")
        def health():
            return jsonify({"status": "ok", "model": self.agent.model})

    def run(self):
        logger.info(f"🌐 Dashboard running at http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
