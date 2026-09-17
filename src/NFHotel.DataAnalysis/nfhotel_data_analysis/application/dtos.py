"""Result objects returned by analysis use cases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NumericFieldStats:
    field: str
    count: int
    mean: float
    minimum: float
    p25: float
    median: float
    p75: float
    maximum: float
    std: float


@dataclass(frozen=True)
class MonthlyBookingCount:
    month: int
    canceled: int
    not_canceled: int


@dataclass(frozen=True)
class RepeatedGuestSummary:
    repeated: int
    not_repeated: int


@dataclass(frozen=True)
class TravelerTypeSummary:
    family: int
    single: int
