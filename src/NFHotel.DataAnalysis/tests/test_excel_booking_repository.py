from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from nfhotel_data_analysis.domain.booking import HotelType
from nfhotel_data_analysis.infrastructure.excel_booking_repository import (
    ExcelBookingRepository,
)


@pytest.fixture
def sample_workbook(tmp_path: Path) -> Path:
    frame = pd.DataFrame(
        [
            {
                "booking_id": 1,
                "hotel": "Resort Hotel",
                "is_canceled": 0,
                "lead_time": 15,
                "booking_date": pd.Timestamp("2019-01-10"),
                "arrival_date": pd.Timestamp("2019-02-01"),
                "adults": 2,
                "children": float("nan"),
                "babies": 0,
                "is_repeated_guest": 0,
                "country": None,
                "market_segment": "Direct",
            },
            {
                "booking_id": 2,
                "hotel": "City Hotel",
                "is_canceled": 1,
                "lead_time": 30,
                "booking_date": pd.Timestamp("2019-03-05"),
                "arrival_date": pd.Timestamp("2019-04-01"),
                "adults": 1,
                "children": 1.0,
                "babies": 0,
                "is_repeated_guest": 1,
                "country": "Portugal",
                "market_segment": "Online TA",
            },
        ]
    )
    path = tmp_path / "bookings.xlsx"
    frame.to_excel(path, index=False)
    return path


def test_get_all_maps_rows_to_booking_entities(sample_workbook: Path):
    repository = ExcelBookingRepository(sample_workbook)

    bookings = repository.get_all()

    assert len(bookings) == 2
    first = bookings[0]
    assert first.booking_id == 1
    assert first.hotel is HotelType.RESORT
    assert first.is_canceled is False
    assert first.booking_date == date(2019, 1, 10)
    assert first.children == 0
    assert first.country is None


def test_get_by_hotel_filters_to_requested_hotel(sample_workbook: Path):
    repository = ExcelBookingRepository(sample_workbook)

    city_bookings = repository.get_by_hotel(HotelType.CITY)

    assert len(city_bookings) == 1
    assert city_bookings[0].booking_id == 2
    assert city_bookings[0].is_repeated_guest is True
