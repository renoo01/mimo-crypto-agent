"""MiMo Crypto Agent Configuration"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── MiMo API ───
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_API_BASE = os.getenv("MIMO_API_BASE", "https://platform.xiaomimimo.com/v1")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2-5-reasoning")
MIMO_MAX_TOKENS = int(os.getenv("MIMO_MAX_TOKENS", "4096"))
MIMO_TEMPERATURE = float(os.getenv("MIMO_TEMPERATURE", "0.7"))

# ─── Telegram ───
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ─── Data Sources ───
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"
ETHERSCAN_API = "https://api.etherscan.io/api"
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY", "")
COINGECKO_API = "https://api.coingecko.com/api/v3"

# ─── Agent Settings ───
ANALYSIS_INTERVAL = int(os.getenv("ANALYSIS_INTERVAL", "300"))  # seconds
MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "5"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ─── Chains ───
SUPPORTED_CHAINS = {
    "ethereum": {"name": "Ethereum", "chain_id": 1, "scanner": "https://etherscan.io"},
    "solana": {"name": "Solana", "chain_id": None, "scanner": "https://solscan.io"},
    "base": {"name": "Base", "chain_id": 8453, "scanner": "https://basescan.org"},
    "arbitrum": {"name": "Arbitrum", "chain_id": 42161, "scanner": "https://arbiscan.io"},
    "bsc": {"name": "BNB Chain", "chain_id": 56, "scanner": "https://bscscan.com"},
}
