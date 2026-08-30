"""Minimal Phase 4 scoring function for L6-001."""

import logging
import statistics


logger = logging.getLogger(__name__)


def compute_l6_001(
    history: list[float],
    is_missing: bool,
    prev_score: float | None,
    missing_days: int,
) -> tuple[float, int, str | None]:
    """Return the L6-001 score, updated missing-day count, and trend note."""
    if is_missing:
        new_missing_days = missing_days + 1
        new_score = 0.0 if prev_score is None else prev_score * 0.95
        if new_missing_days >= 3:
            logger.warning("L6-001 has been missing for %d consecutive days", new_missing_days)
            new_score = 0.0
        return new_score, new_missing_days, None

    if len(history) != 60:
        raise ValueError("history must contain exactly 60 GPRD_ACT values")

    # MA5 minus MA20 measures the recent trend relative to the broader level.
    ma5 = statistics.fmean(history[-5:])
    ma20 = statistics.fmean(history[-20:])
    # STD60 measures volatility; the 0.1 floor prevents division by near-zero noise.
    std60 = max(statistics.pstdev(history), 0.1)
    raw = (ma5 - ma20) / std60
    new_score = max(-1.0, min(1.0, raw))
    trend_note = "elevated" if raw > 0.5 else "subdued" if raw < -0.5 else None
    return new_score, 0, trend_note
