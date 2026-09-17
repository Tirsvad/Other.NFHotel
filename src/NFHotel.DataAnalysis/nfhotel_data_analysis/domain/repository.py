"""Port for retrieving bookings. Implemented by the infrastructure layer."""

from __future__ import annotations

from typing import Protocol

from .booking import Booking, HotelType


class BookingRepository(Protocol):
    def get_all(self) -> list[Booking]: ...

    def get_by_hotel(self, hotel: HotelType) -> list[Booking]: ...
