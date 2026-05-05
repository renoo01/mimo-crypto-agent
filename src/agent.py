"""MiMo Agent — Core AI Engine for Crypto Analysis"""

import httpx
import json
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

# ─── MiMo API Client ───

MIMO_API_BASE = "https://platform.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2-5-reasoning"


@dataclass
class AnalysisResult:
    """Structured result from MiMo analysis."""
    query: str
    analysis: str
    confidence: float  # 0.0 - 1.0
    recommendation: str  # "BUY", "SELL", "HOLD", "SKIP", "WATCH"
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "EXTREME"
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens_used: int = 0
    latency_ms: int = 0


class MiMoAgent:
    """
    Core agent that uses Xiaomi MiMo V2.5 for crypto analysis.
    Supports reasoning mode for complex multi-step analysis.
    """

    def __init__(self, api_key: str, model: str = MIMO_MODEL, base_url: str = MIMO_API_BASE):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
        self._system_prompt = self._build_system_prompt()
        self._total_tokens = 0
        self._total_queries = 0

    def _build_system_prompt(self) -> str:
        return """You are MiMo Crypto Agent, an expert cryptocurrency analysis AI powered by Xiaomi MiMo V2.5.

Your capabilities:
1. Token Analysis — Evaluate contracts, tokenomics, holder distribution, liquidity
2. Whale Tracking — Interpret wallet movements, smart money flows
3. Market Sentiment — Analyze news, social media, on-chain metrics
4. Risk Assessment — Calculate rug-pull probability, impermanent loss risk
5. Opportunity Scoring — Expected value calculations for trades/airdrops

Output Format (always use this JSON structure):
{
    "summary": "Brief analysis summary (1-2 sentences)",
    "detailed_analysis": "Full breakdown",
    "confidence": 0.0-1.0,
    "recommendation": "BUY|SELL|HOLD|SKIP|WATCH",
    "risk_level": "LOW|MEDIUM|HIGH|EXTREME",
    "key_factors": ["factor1", "factor2", ...],
    "metrics": {
        // relevant numerical metrics
    }
}

Be objective, data-driven, and always highlight risks. Never give financial advice — present analysis for decision-making.
"""

    async def analyze(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        use_reasoning: bool = True,
    ) -> AnalysisResult:
        """Run MiMo analysis on a crypto-related query."""
        start = time.time()

        # Build user message
        user_msg = prompt
        if context:
            user_msg += f"\n\nContext Data:\n```json\n{json.dumps(context, indent=2)}\n```"

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_msg},
        ]

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 4096,
                    "temperature": 0.7 if use_reasoning else 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            tokens_used = data.get("usage", {}).get("total_tokens", 0)
            latency = int((time.time() - start) * 1000)

            # Parse JSON response
            try:
                # Extract JSON from possible markdown codeblock
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    json_str = content.split("```")[1].split("```")[0]
                else:
                    json_str = content

                parsed = json.loads(json_str.strip())
                return AnalysisResult(
                    query=prompt,
                    analysis=parsed.get("detailed_analysis", content),
                    confidence=float(parsed.get("confidence", 0.5)),
                    recommendation=parsed.get("recommendation", "WATCH"),
                    risk_level=parsed.get("risk_level", "MEDIUM"),
                    metadata={
                        "summary": parsed.get("summary", ""),
                        "key_factors": parsed.get("key_factors", []),
                        "metrics": parsed.get("metrics", {}),
                    },
                    tokens_used=tokens_used,
                    latency_ms=latency,
                )
            except json.JSONDecodeError:
                # Fallback: return raw text
                return AnalysisResult(
                    query=prompt,
                    analysis=content,
                    confidence=0.5,
                    recommendation="WATCH",
                    risk_level="MEDIUM",
                    tokens_used=tokens_used,
                    latency_ms=latency,
                )

        except Exception as e:
            logger.error(f"MiMo API error: {e}")
            return AnalysisResult(
                query=prompt,
                analysis=f"Analysis failed: {str(e)}",
                confidence=0.0,
                recommendation="SKIP",
                risk_level="HIGH",
                latency_ms=int((time.time() - start) * 1000),
            )

    async def analyze_token(self, token_address: str, chain: str = "ethereum") -> AnalysisResult:
        """Full token analysis using MiMo reasoning."""
        return await self.analyze(
            f"Analyze this token on {chain}: {token_address}\n\n"
            "Check: contract safety, holder distribution, liquidity, recent activity, "
            "social presence, and overall risk/reward profile.",
        )

    async def analyze_whale(self, wallet_address: str) -> AnalysisResult:
        """Analyze whale wallet activity."""
        return await self.analyze(
            f"Analyze this wallet's recent activity and portfolio:\n{wallet_address}\n\n"
            "Assess: trading patterns, profitability, notable positions, fund flows.",
        )

    async def get_sentiment(self, query: str) -> AnalysisResult:
        """Get market sentiment analysis."""
        return await self.analyze(
            f"Analyze current market sentiment for: {query}\n\n"
            "Consider: news, social media trends, on-chain metrics, technical indicators.",
        )

    async def analyze_polymarket(self, market_slug: str) -> AnalysisResult:
        """Analyze Polymarket odds and find value bets."""
        return await self.analyze(
            f"Analyze this Polymarket prediction market: {market_slug}\n\n"
            "Calculate: current odds, historical trend, news correlation, expected value. "
            "Identify if market is mispriced vs actual probability.",
        )

    @property
    def stats(self) -> Dict:
        return {
            "total_queries": self._total_queries,
            "total_tokens": self._total_tokens,
            "model": self.model,
        }

    async def close(self):
        await self.client.aclose()
