"""Use cases for analysing hotel bookings.

Operates only on domain entities through the ``BookingRepository`` port, so it
can be unit tested without pandas or a real data file.
"""

from __future__ import annotations

import statistics
from collections import Counter

from ..domain.booking import Booking, HotelType
from ..domain.repository import BookingRepository
from .dtos import (
    MonthlyBookingCount,
    NumericFieldStats,
    RepeatedGuestSummary,
    TravelerTypeSummary,
)

_NUMERIC_FIELDS = ("lead_time", "adults", "children", "babies")


class HotelAnalysisService:
    def __init__(self, repository: BookingRepository) -> None:
        self._repository = repository

    def descriptive_stats(self, hotel: HotelType) -> list[NumericFieldStats]:
        bookings = self._repository.get_by_hotel(hotel)
        return [self._describe_field(bookings, field) for field in _NUMERIC_FIELDS]

    def monthly_booking_summary(self, hotel: HotelType) -> list[MonthlyBookingCount]:
        bookings = self._repository.get_by_hotel(hotel)
        canceled = Counter(b.booking_month for b in bookings if b.is_canceled)
        not_canceled = Counter(b.booking_month for b in bookings if not b.is_canceled)
        months = sorted(set(canceled) | set(not_canceled))
        return [
            MonthlyBookingCount(
                month=month,
                canceled=canceled.get(month, 0),
                not_canceled=not_canceled.get(month, 0),
            )
            for month in months
        ]

    def repeated_guest_summary(self, hotel: HotelType) -> RepeatedGuestSummary:
        bookings = self._repository.get_by_hotel(hotel)
        repeated = sum(1 for b in bookings if b.is_repeated_guest)
        return RepeatedGuestSummary(repeated=repeated, not_repeated=len(bookings) - repeated)

    def traveler_type_summary(self, hotel: HotelType) -> TravelerTypeSummary:
        bookings = self._repository.get_by_hotel(hotel)
        family = sum(1 for b in bookings if b.is_family_booking)
        return TravelerTypeSummary(family=family, single=len(bookings) - family)

    @staticmethod
    def _describe_field(bookings: list[Booking], field: str) -> NumericFieldStats:
        values = sorted(getattr(b, field) for b in bookings)
        return NumericFieldStats(
            field=field,
            count=len(values),
            mean=statistics.fmean(values),
            minimum=values[0],
            p25=_percentile(values, 0.25),
            median=statistics.median(values),
            p75=_percentile(values, 0.75),
            maximum=values[-1],
            std=statistics.stdev(values) if len(values) > 1 else 0.0,
        )


def _percentile(sorted_values: list[float], fraction: float) -> float:
    index = fraction * (len(sorted_values) - 1)
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = index - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight
