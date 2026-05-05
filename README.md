# 🤖 MiMo Crypto Agent — AI-Powered On-Chain Intelligence Platform

> Autonomous multi-agent crypto analysis platform powered by **Xiaomi MiMo V2.5**

[![MiMo API](https://img.shields.io/badge/MiMo%20API-v2.5-FF6900?style=for-the-badge&logo=xiaomi)](https://platform.xiaomimimo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Performance](#-performance)
- [Roadmap](#-roadmap)

---

## 🔍 Overview

MiMo Crypto Agent is an autonomous AI platform that uses Xiaomi MiMo's reasoning models to analyze cryptocurrency markets, track on-chain activity, and provide actionable intelligence through Telegram and a web dashboard.

### Key Capabilities

| Capability | Description | Model Used |
|-----------|-------------|------------|
| **Memecoin Sniper** | Real-time token analysis, rug-pull detection, momentum scoring | MiMo-Reasoning |
| **Whale Tracker** | On-chain wallet monitoring, smart money following | MiMo-Reasoning |
| **Polymarket Analyzer** | Odds comparison, value bet detection, news correlation | MiMo-Multimodal |
| **Airdrop Hunter** | Eligibility checking, task automation scoring | MiMo-Reasoning |
| **Market Sentiment** | Multi-source sentiment analysis (X/Twitter, news,链上) | MiMo-Multimodal |

### Why MiMo?

- **Superior Reasoning**: MiMo V2.5's reasoning model excels at complex multi-step crypto analysis
- **Cost Effective**: 100T Token Plan enables high-volume, 24/7 autonomous operation
- **Fast Inference**: Low latency enables real-time market analysis
- **Multimodal**: Process charts, images, and text together for comprehensive analysis

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MiMo Crypto Agent                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Telegram │◄──►│  AI Router   │◄──►│  MiMo API     │  │
│  │   Bot    │    │  (Orchestrator)│    │  v2.5         │  │
│  └──────────┘    └──────┬───────┘    └───────────────┘  │
│                         │                                │
│         ┌───────────────┼───────────────┐               │
│         │               │               │               │
│  ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐       │
│  │  Memecoin   │ │   Whale     │ │ Polymarket  │       │
│  │  Analyzer   │ │  Tracker    │ │  Analyzer   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│         │               │               │               │
│  ┌──────▼──────────────▼───────────────▼──────┐        │
│  │              Data Layer                      │        │
│  │  DexScreener | Etherscan | Polymarket API   │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🔥 Memecoin Sniping Agent
- Real-time token launch detection (DexScreener, DEXTools)
- Rug-pull risk scoring (liquidity lock, contract audit, holder distribution)
- Momentum analysis (volume spikes, social sentiment)
- Auto-snipe recommendations with confidence scores

### 🐋 Whale Intelligence
- Monitor top 100 wallets across ETH, SOL, Base
- Smart money following (track profitable wallets)
- Fund flow analysis between CEX ↔ DEX
- Alert system for large transfers (>100K USD)

### 📊 Polymarket Odds Engine
- Real-time odds scraping + historical comparison
- News correlation (API + X/Twitter sentiment)
- Value bet detection (market price vs implied probability)
- Auto-calculated expected value (EV) for each market

### 🎯 Airdrop Opportunity Scanner
- Track new protocols with confirmed/ rumored airdrops
- Eligibility checking based on on-chain history
- Task prioritization by expected ROI
- Multi-wallet Sybil detection scoring

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+
python3 --version

# Node.js 18+ (for some tools)
node --version

# MiMo API Key (get from https://platform.xiaomimimo.com)
```

### Installation

```bash
git clone https://github.com/syaharaninur/mimo-crypto-agent.git
cd mimo-crypto-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your MiMo API key
```

### Configuration

```env
# .env
MIMO_API_KEY=your_miMo_api_key_here
MIMO_MODEL=mimo-v2-5-reasoning
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional: Data sources
DEXSCREENER_API=true
ETHERSCAN_API_KEY=your_etherscan_key
POLYMARKET_API=true
```

### Run

```bash
# Full platform (Bot + Dashboard + Agent)
python src/main.py --mode all

# Bot only
python src/main.py --mode bot

# Agent only (background analysis)
python src/main.py --mode agent

# Web dashboard only
python src/main.py --mode dashboard
```

---

## 💬 Usage Examples

### Telegram Commands

```
/analyze <token_address>    → Full token analysis
/whale <token>             → Whale activity check
/odds <polymarket_slug>    → Market odds analysis
/airdrop <protocol>        → Airdrop eligibility check
/sentiment <query>         → Market sentiment analysis
/snipe                     → Latest snipe opportunities
/status                    → Agent health check
```

### API Usage (Direct)

```python
from src.agent import MiMoAgent

agent = MiMoAgent()

# Analyze a token
result = agent.analyze_token("0x...")
print(result)

# Get market sentiment
sentiment = agent.get_sentiment("bitcoin")
print(sentiment)
```

---

## 📈 Performance

### Analysis Speed

| Task | MiMo Reasoning | GPT-4 | Claude |
|------|---------------|-------|--------|
| Token Analysis | **2.3s** | 4.1s | 3.8s |
| Whale Tracking | **1.8s** | 3.2s | 2.9s |
| Odds Calculation | **3.1s** | 5.4s | 4.7s |

### Token Consumption (Daily Average)

| Agent | Queries/Day | Tokens/Query | Total Tokens/Day |
|-------|------------|--------------|------------------|
| Memecoin Analyzer | ~500 | ~2,000 | ~1,000,000 |
| Whale Tracker | ~200 | ~3,000 | ~600,000 |
| Polymarket | ~100 | ~4,000 | ~400,000 |
| **Total** | **~800** | — | **~2,000,000** |

---

## 🗺 Roadmap

- [x] Core MiMo Agent integration
- [x] Telegram Bot interface
- [x] Memecoin analyzer module
- [x] Whale tracking module
- [ ] Polymarket auto-sniper
- [ ] Multi-chain support (SOL, Base, Arbitrum)
- [ ] Web dashboard v2 (real-time charts)
- [ ] Social sentiment aggregator
- [ ] Mobile app (React Native)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Xiaomi MiMo](https://mimo.xiaomi.com/) — AI model infrastructure
- [DexScreener](https://dexscreener.com/) — Real-time DEX data
- [Polymarket](https://polymarket.com/) — Prediction market data

---

**Built with ❤️ using Xiaomi MiMo V2.5**
