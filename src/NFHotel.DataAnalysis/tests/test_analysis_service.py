from __future__ import annotations

from datetime import date

from nfhotel_data_analysis.application.analysis_service import HotelAnalysisService
from nfhotel_data_analysis.application.dtos import (
    MonthlyBookingCount,
    RepeatedGuestSummary,
    TravelerTypeSummary,
)
from nfhotel_data_analysis.domain.booking import Booking, HotelType


class FakeBookingRepository:
    def __init__(self, bookings: list[Booking]) -> None:
        self._bookings = bookings

    def get_all(self) -> list[Booking]:
        return self._bookings

    def get_by_hotel(self, hotel: HotelType) -> list[Booking]:
        return [b for b in self._bookings if b.hotel == hotel]


def make_booking(**overrides) -> Booking:
    defaults: dict = dict(
        booking_id=1,
        hotel=HotelType.RESORT,
        is_canceled=False,
        lead_time=10,
        booking_date=date(2019, 1, 15),
        arrival_date=date(2019, 2, 1),
        adults=2,
        children=0,
        babies=0,
        is_repeated_guest=False,
        country="Portugal",
        market_segment="Direct",
    )
    defaults.update(overrides)
    return Booking(**defaults)


def test_monthly_booking_summary_groups_by_month_and_cancellation():
    bookings = [
        make_booking(booking_date=date(2019, 1, 5), is_canceled=False),
        make_booking(booking_date=date(2019, 1, 20), is_canceled=True),
        make_booking(booking_date=date(2019, 2, 3), is_canceled=False),
    ]
    service = HotelAnalysisService(FakeBookingRepository(bookings))

    summary = service.monthly_booking_summary(HotelType.RESORT)

    assert summary == [
        MonthlyBookingCount(month=1, canceled=1, not_canceled=1),
        MonthlyBookingCount(month=2, canceled=0, not_canceled=1),
    ]


def test_monthly_booking_summary_only_includes_requested_hotel():
    bookings = [
        make_booking(hotel=HotelType.RESORT, booking_date=date(2019, 1, 1)),
        make_booking(hotel=HotelType.CITY, booking_date=date(2019, 1, 1)),
    ]
    service = HotelAnalysisService(FakeBookingRepository(bookings))

    summary = service.monthly_booking_summary(HotelType.CITY)

    assert summary == [MonthlyBookingCount(month=1, canceled=0, not_canceled=1)]


def test_repeated_guest_summary_counts_repeated_and_new_guests():
    bookings = [
        make_booking(is_repeated_guest=True),
        make_booking(is_repeated_guest=False),
        make_booking(is_repeated_guest=False),
    ]
    service = HotelAnalysisService(FakeBookingRepository(bookings))

    assert service.repeated_guest_summary(HotelType.RESORT) == RepeatedGuestSummary(
        repeated=1, not_repeated=2
    )


def test_traveler_type_summary_classifies_family_vs_single():
    bookings = [
        make_booking(adults=2, children=1, babies=0),  # family
        make_booking(adults=1, children=0, babies=0),  # single
    ]
    service = HotelAnalysisService(FakeBookingRepository(bookings))

    assert service.traveler_type_summary(HotelType.RESORT) == TravelerTypeSummary(
        family=1, single=1
    )


def test_descriptive_stats_computes_expected_aggregates_for_lead_time():
    bookings = [make_booking(lead_time=value) for value in (0, 10, 20, 30, 40)]
    service = HotelAnalysisService(FakeBookingRepository(bookings))

    stats = next(s for s in service.descriptive_stats(HotelType.RESORT) if s.field == "lead_time")

    assert stats.count == 5
    assert stats.mean == 20
    assert stats.minimum == 0
    assert stats.median == 20
    assert stats.maximum == 40
