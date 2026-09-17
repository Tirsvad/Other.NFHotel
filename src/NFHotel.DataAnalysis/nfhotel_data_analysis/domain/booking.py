"""Core booking entity and value objects. No pandas or I/O here."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class HotelType(str, Enum):
    RESORT = "Resort Hotel"
    CITY = "City Hotel"


@dataclass(frozen=True)
class Booking:
    booking_id: int
    hotel: HotelType
    is_canceled: bool
    lead_time: int
    booking_date: date
    arrival_date: date
    adults: int
    children: int
    babies: int
    is_repeated_guest: bool
    country: str | None
    market_segment: str

    @property
    def is_family_booking(self) -> bool:
        return (self.adults + self.children + self.babies) > 1

    @property
    def booking_month(self) -> int:
        return self.booking_date.month
