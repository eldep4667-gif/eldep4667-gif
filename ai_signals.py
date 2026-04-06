"""Decision engine that fuses price structure, indicators, patterns, and news."""

from __future__ import annotations

import math

import pandas as pd


class AISignalEngine:
    """Generate an aggressive but transparent trading decision."""

    def __init__(self, df: pd.DataFrame, technical, pattern_detector, schools, news_summary: dict | None = None):
        self.df = df.copy()
        self.technical = technical
        self.pattern_detector = pattern_detector
        self.schools = schools
        self.news_summary = news_summary or {}

    def generate_signal(self, mode: str = "SMART") -> dict:
        snapshot = self.technical.get_indicators_snapshot()
        current = float(snapshot["close"])
        atr = float(self.technical.indicators["atr"].iloc[-1]) if not self.technical.indicators["atr"].empty else current * 0.004
        atr = max(atr, current * 0.0015)

        details = []
        score = 0.0

        score += self._score_trend(snapshot, current, details)
        score += self._score_momentum(snapshot, details)
        score += self._score_structure(current, atr, details)
        score += self._score_patterns(details)
        score += self._score_news(details)

        mode_boosts = {"SMART": 1.0, "SMC": 1.08, "ICT": 1.05, "SK": 1.03}
        score *= mode_boosts.get(mode, 1.0)

        action = "WAIT"
        if score >= 1.25:
            action = "BUY"
        elif score <= -1.25:
            action = "SELL"

        entry_low, entry_high = self._entry_zone(current, atr, action)
        sl, tp = self._risk_targets(current, atr, action)
        risk = max(abs(current - sl), 1e-9)
        reward = abs(tp - current)
        confidence = self._confidence(score, details)
        conflict_count = sum(1 for item in details if item["direction"] == "conflict")
        bias = "Bullish" if score > 0.3 else "Bearish" if score < -0.3 else "Neutral"

        summary = {
            "decision": action,
            "bias": bias,
            "entry": round(current, 5),
            "entry_zone": f"{entry_low:.5f} - {entry_high:.5f}",
            "sl": round(sl, 5),
            "tp": round(tp, 5),
            "rr": round(reward / risk, 2),
            "confidence": confidence,
            "score": round(score, 2),
            "confluence_score": round(abs(score) * 20, 1),
            "news_impact": self.news_summary.get("impact_label", "Unknown"),
            "news_bias": self.news_summary.get("sentiment", "neutral"),
            "reason": self._headline_reason(details, action),
            "invalidations": self._invalidations(action),
            "tp_sl_rationale": self._tp_sl_rationale(action, atr),
            "details": details,
            "conflicts": conflict_count,
        }
        return summary

    def _score_trend(self, snapshot: dict, current: float, details: list[dict]) -> float:
        score = 0.0
        ma20 = float(snapshot["ma20"])
        ma50 = float(snapshot["ma50"])
        trendline = snapshot["trendline_direction"]

        if current > ma20 > ma50:
            score += 1.2
            details.append(self._detail("Trend Alignment", "bullish", 1.2, "Price is trading above MA20 and MA50 with bullish alignment."))
        elif current < ma20 < ma50:
            score -= 1.2
            details.append(self._detail("Trend Alignment", "bearish", 1.2, "Price is trading below MA20 and MA50 with bearish alignment."))
        else:
            details.append(self._detail("Trend Alignment", "conflict", 0.45, "Moving averages are not fully aligned, so trend quality is mixed."))

        if trendline == "Bullish":
            score += 0.6
            details.append(self._detail("Trendline Slope", "bullish", 0.6, "Linear trend slope still favors continuation to the upside."))
        else:
            score -= 0.6
            details.append(self._detail("Trendline Slope", "bearish", 0.6, "Linear trend slope still favors continuation to the downside."))
        return score

    def _score_momentum(self, snapshot: dict, details: list[dict]) -> float:
        score = 0.0
        rsi = float(snapshot["rsi"])
        macd = float(snapshot["macd"])
        macd_signal = float(snapshot["macd_signal"])

        if rsi >= 58:
            score += 0.8
            details.append(self._detail("RSI Regime", "bullish", 0.8, f"RSI is strong at {rsi:.1f}, supporting momentum continuation."))
        elif rsi <= 42:
            score -= 0.8
            details.append(self._detail("RSI Regime", "bearish", 0.8, f"RSI is weak at {rsi:.1f}, supporting downside pressure."))
        else:
            details.append(self._detail("RSI Regime", "conflict", 0.35, f"RSI sits in the mid-zone at {rsi:.1f}, so momentum is not decisive."))

        if macd > macd_signal:
            score += 0.7
            details.append(self._detail("MACD Cross", "bullish", 0.7, "MACD is above signal and confirms positive momentum."))
        else:
            score -= 0.7
            details.append(self._detail("MACD Cross", "bearish", 0.7, "MACD is below signal and confirms negative momentum."))
        return score

    def _score_structure(self, current: float, atr: float, details: list[dict]) -> float:
        score = 0.0
        smc = self.schools.smc_analysis
        ict = self.schools.ict_analysis
        sk = self.schools.sk_analysis
        ta = self.schools.ta_summary

        last_bos = self._first(smc.get("bos", []), from_end=True)
        if last_bos:
            bullish = "bullish" in last_bos.get("type", "")
            value = 0.95 if bullish else -0.95
            score += value
            details.append(
                self._detail(
                    "SMC Structure",
                    "bullish" if bullish else "bearish",
                    abs(value),
                    "Latest break of structure supports institutional directional flow.",
                )
            )

        order_block = self._first(smc.get("order_blocks", []))
        if order_block:
            bullish = order_block.get("type") == "bullish"
            distance = abs(current - order_block.get("mid", current))
            strength = 0.75 if distance <= atr * 1.6 else 0.35
            score += strength if bullish else -strength
            details.append(
                self._detail(
                    "Order Block",
                    "bullish" if bullish else "bearish",
                    strength,
                    "Price is interacting with the nearest institutional order block.",
                )
            )

        ict_fvg = self._first(ict.get("fvg", []))
        if ict_fvg:
            bullish = ict_fvg.get("type") == "bullish"
            score += 0.35 if bullish else -0.35
            details.append(
                self._detail(
                    "Fair Value Gap",
                    "bullish" if bullish else "bearish",
                    0.35,
                    "A fresh imbalance still supports continuation if price respects it.",
                )
            )

        market_structure = sk.get("market_structure", "Neutral")
        if market_structure == "Bullish":
            score += 0.5
            details.append(self._detail("SK Structure", "bullish", 0.5, "Higher-level structure remains bullish on the active timeframe."))
        elif market_structure == "Bearish":
            score -= 0.5
            details.append(self._detail("SK Structure", "bearish", 0.5, "Higher-level structure remains bearish on the active timeframe."))

        support = float(ta.get("support", current))
        resistance = float(ta.get("resistance", current))
        if current - support <= atr * 1.2:
            score += 0.4
            details.append(self._detail("Support Reaction", "bullish", 0.4, "Current price is close to active support, improving rebound odds."))
        if resistance - current <= atr * 1.2:
            score -= 0.4
            details.append(self._detail("Resistance Pressure", "bearish", 0.4, "Current price is close to active resistance, limiting upside room."))

        return score

    def _score_patterns(self, details: list[dict]) -> float:
        pattern = self.pattern_detector.detected_patterns[0] if self.pattern_detector.detected_patterns else None
        if not pattern:
            details.append(self._detail("Pattern Context", "conflict", 0.2, "No high-confidence harmonic pattern is currently active."))
            return 0.0

        direction = 1 if pattern.get("signal") == "buy" else -1
        weight = min(1.1, pattern.get("confidence", 0) / 100 * 1.1)
        details.append(
            self._detail(
                f"{pattern.get('name', 'Pattern')} Pattern",
                "bullish" if direction > 0 else "bearish",
                weight,
                f"Harmonic pattern detected with {pattern.get('confidence', 0):.0f}% confidence near reversal zone.",
            )
        )
        return direction * weight

    def _score_news(self, details: list[dict]) -> float:
        sentiment = self.news_summary.get("sentiment", "neutral")
        impact = self.news_summary.get("impact_label", "Unknown")
        magnitude = {"Low": 0.2, "Medium": 0.45, "High": 0.7, "Unknown": 0.0}.get(impact, 0.0)

        if sentiment == "positive":
            details.append(self._detail("News Flow", "bullish", magnitude, "Recent headlines lean supportive for the selected instrument."))
            return magnitude
        if sentiment == "negative":
            details.append(self._detail("News Flow", "bearish", magnitude, "Recent headlines lean negative for the selected instrument."))
            return -magnitude

        details.append(self._detail("News Flow", "conflict", 0.25, "News flow is mixed or low conviction, so it is not confirming price strongly."))
        return 0.0

    def _entry_zone(self, current: float, atr: float, action: str) -> tuple[float, float]:
        width = atr * 0.45
        if action == "BUY":
            return current - width, current + atr * 0.2
        if action == "SELL":
            return current - atr * 0.2, current + width
        return current - width, current + width

    def _risk_targets(self, current: float, atr: float, action: str) -> tuple[float, float]:
        if action == "BUY":
            return current - atr * 1.55, current + atr * 2.9
        if action == "SELL":
            return current + atr * 1.55, current - atr * 2.9
        return current - atr * 1.15, current + atr * 1.15

    def _confidence(self, score: float, details: list[dict]) -> float:
        bullish = sum(item["weight"] for item in details if item["direction"] == "bullish")
        bearish = sum(item["weight"] for item in details if item["direction"] == "bearish")
        conflict = sum(item["weight"] for item in details if item["direction"] == "conflict")
        edge = abs(bullish - bearish)
        confidence = 52 + edge * 12 + abs(score) * 6 - conflict * 5
        return round(max(45.0, min(92.0, confidence)), 1)

    def _headline_reason(self, details: list[dict], action: str) -> str:
        directional = [item["signal"] for item in details if item["direction"] in {"bullish", "bearish"}]
        if not directional:
            return "Signals are mixed and there is no decisive confluence yet."
        prefix = "Aggressive long setup" if action == "BUY" else "Aggressive short setup" if action == "SELL" else "Mixed setup"
        return f"{prefix} backed by {', '.join(directional[:4])}."

    def _invalidations(self, action: str) -> str:
        if action == "BUY":
            return "Invalidate if price loses nearby demand and closes back under structure support."
        if action == "SELL":
            return "Invalidate if price reclaims nearby supply and closes back above structure resistance."
        return "Wait for structure break plus momentum confirmation before committing."

    def _tp_sl_rationale(self, action: str, atr: float) -> str:
        atr_text = f"{atr:.5f}"
        if action == "WAIT":
            return f"Neutral plan uses a tight ATR envelope ({atr_text}) until direction becomes clearer."
        return f"Stop loss is anchored around 1.55 ATR and take profit around 2.9 ATR to preserve an aggressive but controlled reward profile."

    def _detail(self, signal: str, direction: str, weight: float, description: str) -> dict:
        normalized = max(0.0, min(1.25, float(weight)))
        return {
            "signal": signal,
            "direction": direction,
            "weight": round(normalized, 2),
            "desc": description,
            "strength": math.floor(normalized / 1.25 * 100),
        }

    def _first(self, values: list[dict], from_end: bool = False) -> dict | None:
        if not values:
            return None
        return values[-1] if from_end else values[0]
