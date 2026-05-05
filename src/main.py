#!/usr/bin/env python3
"""
MiMo Crypto Agent — Main Entry Point
AI-Powered On-Chain Intelligence Platform powered by Xiaomi MiMo V2.5

Usage:
    python src/main.py --mode all       # Run bot + dashboard + agent
    python src/main.py --mode bot       # Telegram bot only
    python src/main.py --mode dashboard # Web dashboard only
    python src/main.py --mode agent     # Background agent only
"""

import argparse
import asyncio
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import MIMO_API_KEY, MIMO_MODEL, TELEGRAM_BOT_TOKEN
from src.agent import MiMoAgent
from src.dashboard import Dashboard
from src.telegram_bot import CryptoBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mimo-crypto-agent")


async def run_agent_mode(agent: MiMoAgent):
    """Run background analysis agent."""
    logger.info("🤖 Background agent started — analyzing markets every 5 minutes...")
    while True:
        try:
            # Quick market scan
            result = await agent.get_sentiment("crypto market today")
            logger.info(f"Market scan: {result.metadata.get('summary', 'N/A')}")
        except Exception as e:
            logger.error(f"Agent error: {e}")
        await asyncio.sleep(300)  # 5 minutes


def main():
    parser = argparse.ArgumentParser(description="MiMo Crypto Agent")
    parser.add_argument("--mode", choices=["all", "bot", "dashboard", "agent"], default="all")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if not MIMO_API_KEY:
        logger.error("❌ MIMO_API_KEY not set. Copy .env.example → .env and add your key.")
        sys.exit(1)

    agent = MiMoAgent(api_key=MIMO_API_KEY, model=MIMO_MODEL)
    logger.info(f"✅ MiMo Agent initialized (model: {MIMO_MODEL})")

    if args.mode == "dashboard":
        dash = Dashboard(agent, port=args.port)
        dash.run()

    elif args.mode == "bot":
        if not TELEGRAM_BOT_TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set.")
            sys.exit(1)
        bot = CryptoBot(TELEGRAM_BOT_TOKEN, agent)
        asyncio.run(bot.run())

    elif args.mode == "agent":
        asyncio.run(run_agent_mode(agent))

    else:  # all
        import threading

        # Start dashboard in thread
        dash = Dashboard(agent, port=args.port)
        t = threading.Thread(target=dash.run, daemon=True)
        t.start()

        # Start bot (blocking)
        if TELEGRAM_BOT_TOKEN:
            bot = CryptoBot(TELEGRAM_BOT_TOKEN, agent)
            asyncio.run(bot.run())
        else:
            logger.warning("⚠️ TELEGRAM_BOT_TOKEN not set — dashboard only")
            import time
            while True:
                time.sleep(1)


if __name__ == "__main__":
    main()
