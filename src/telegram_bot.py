"""Telegram Bot Interface for MiMo Crypto Agent"""

import asyncio
import logging
from typing import Optional

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

logger = logging.getLogger(__name__)


class CryptoBot:
    """Telegram bot that interfaces with MiMo Agent."""

    def __init__(self, token: str, agent):
        self.token = token
        self.agent = agent
        self.app: Optional[Application] = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "🤖 **MiMo Crypto Agent**\n\n"
            "AI-powered crypto analysis powered by Xiaomi MiMo V2.5\n\n"
            "Commands:\n"
            "/analyze `<address>` — Full token analysis\n"
            "/whale `<address>` — Whale wallet analysis\n"
            "/sentiment `<query>` — Market sentiment\n"
            "/odds `<market>` — Polymarket analysis\n"
            "/status — Agent health check\n\n"
            "Or just ask me anything about crypto! 💬",
            parse_mode="Markdown",
        )

    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command."""
        if not context.args:
            await update.message.reply_text("❌ Usage: /analyze `<token_address>`", parse_mode="Markdown")
            return

        token = context.args[0]
        await update.message.reply_text(f"🔍 Analyzing token: `{token}`...\n⏳ Using MiMo Reasoning...", parse_mode="Markdown")

        result = await self.agent.analyze_token(token)

        response = (
            f"📊 **Token Analysis**\n"
            f"`{token}`\n\n"
            f"**Summary:** {result.metadata.get('summary', 'N/A')}\n\n"
            f"**Recommendation:** {self._format_recommendation(result.recommendation)}\n"
            f"**Risk Level:** {self._format_risk(result.risk_level)}\n"
            f"**Confidence:** {result.confidence:.0%}\n\n"
            f"**Analysis:**\n{result.analysis[:2000]}\n\n"
            f"⏱️ {result.latency_ms}ms | 🪙 {result.tokens_used} tokens"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

    async def whale(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /whale command."""
        if not context.args:
            await update.message.reply_text("❌ Usage: /whale `<wallet_address>`", parse_mode="Markdown")
            return

        wallet = context.args[0]
        await update.message.reply_text(f"🐋 Analyzing wallet: `{wallet}`...", parse_mode="Markdown")

        result = await self.agent.analyze_whale(wallet)

        response = (
            f"🐋 **Whale Analysis**\n"
            f"`{wallet}`\n\n"
            f"**Summary:** {result.metadata.get('summary', 'N/A')}\n\n"
            f"**Analysis:**\n{result.analysis[:2000]}\n\n"
            f"⏱️ {result.latency_ms}ms | 🪙 {result.tokens_used} tokens"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

    async def sentiment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sentiment command."""
        if not context.args:
            await update.message.reply_text("❌ Usage: /sentiment `<query>`", parse_mode="Markdown")
            return

        query = " ".join(context.args)
        await update.message.reply_text(f"📰 Analyzing sentiment: `{query}`...", parse_mode="Markdown")

        result = await self.agent.get_sentiment(query)

        response = (
            f"📰 **Sentiment Analysis**\n"
            f"Query: {query}\n\n"
            f"**Summary:** {result.metadata.get('summary', 'N/A')}\n\n"
            f"**Sentiment:** {self._format_recommendation(result.recommendation)}\n"
            f"**Confidence:** {result.confidence:.0%}\n\n"
            f"**Analysis:**\n{result.analysis[:2000]}\n\n"
            f"⏱️ {result.latency_ms}ms | 🪙 {result.tokens_used} tokens"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        stats = self.agent.stats
        await update.message.reply_text(
            f"🤖 **MiMo Crypto Agent Status**\n\n"
            f"Model: `{stats['model']}`\n"
            f"Total Queries: {stats['total_queries']}\n"
            f"Total Tokens: {stats['total_tokens']:,}\n"
            f"Status: ✅ Online",
            parse_mode="Markdown",
        )

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle free-form messages."""
        user_msg = update.message.text
        result = await self.agent.analyze(user_msg)
        await update.message.reply_text(
            f"🤖 {result.analysis[:3000]}\n\n"
            f"Confidence: {result.confidence:.0%} | ⏱️ {result.latency_ms}ms"
        )

    @staticmethod
    def _format_recommendation(rec: str) -> str:
        icons = {"BUY": "🟢 BUY", "SELL": "🔴 SELL", "HOLD": "🟡 HOLD", "SKIP": "⛔ SKIP", "WATCH": "👀 WATCH"}
        return icons.get(rec, f"❓ {rec}")

    @staticmethod
    def _format_risk(risk: str) -> str:
        icons = {"LOW": "🟢 LOW", "MEDIUM": "🟡 MEDIUM", "HIGH": "🔴 HIGH", "EXTREME": "💀 EXTREME"}
        return icons.get(risk, f"❓ {risk}")

    async def setup(self):
        """Initialize and configure bot."""
        self.app = Application.builder().token(self.token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("analyze", self.analyze))
        self.app.add_handler(CommandHandler("whale", self.whale))
        self.app.add_handler(CommandHandler("sentiment", self.sentiment))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat))

        await self.app.bot.set_my_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("analyze", "Analyze a token"),
            BotCommand("whale", "Analyze whale wallet"),
            BotCommand("sentiment", "Market sentiment analysis"),
            BotCommand("odds", "Polymarket odds analysis"),
            BotCommand("status", "Agent health check"),
        ])

    async def run(self):
        """Start polling."""
        await self.setup()
        logger.info("🤖 MiMo Crypto Bot started")
        await self.app.run_polling()
