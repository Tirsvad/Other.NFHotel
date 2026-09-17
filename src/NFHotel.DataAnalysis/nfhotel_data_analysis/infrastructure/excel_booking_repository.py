"""Excel-backed implementation of the BookingRepository port.

This is the only module allowed to know about pandas/openpyxl and the shape
of the source spreadsheet; everything upstream works with ``Booking`` entities.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from ..domain.booking import Booking, HotelType


class ExcelBookingRepository:
    def __init__(self, file_path: Path | str) -> None:
        self._file_path = Path(file_path)
        self._bookings: list[Booking] | None = None

    def get_all(self) -> list[Booking]:
        if self._bookings is None:
            frame = pd.read_excel(self._file_path)
            self._bookings = [self._to_booking(row) for row in frame.to_dict(orient="records")]
        return self._bookings

    def get_by_hotel(self, hotel: HotelType) -> list[Booking]:
        return [booking for booking in self.get_all() if booking.hotel == hotel]

    @staticmethod
    def _to_booking(row: dict[str, Any]) -> Booking:
        return Booking(
            booking_id=int(row["booking_id"]),
            hotel=HotelType(row["hotel"]),
            is_canceled=bool(row["is_canceled"]),
            lead_time=int(row["lead_time"]),
            booking_date=pd.Timestamp(row["booking_date"]).date(),
            arrival_date=pd.Timestamp(row["arrival_date"]).date(),
            adults=int(row["adults"]),
            children=int(row["children"]) if pd.notna(row["children"]) else 0,
            babies=int(row["babies"]),
            is_repeated_guest=bool(row["is_repeated_guest"]),
            country=str(row["country"]) if pd.notna(row["country"]) else None,
            market_segment=str(row["market_segment"]),
        )
