"""Composition root: wires the Excel repository to the analysis service and
renders results. This is the only place that decides which infrastructure
implementation to use.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ..application.analysis_service import HotelAnalysisService
from ..domain.booking import HotelType
from ..infrastructure.excel_booking_repository import ExcelBookingRepository
from . import charts

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[3] / "ipynb" / "hotel_bookings.xlsx"


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    repository = ExcelBookingRepository(args.data_path)
    service = HotelAnalysisService(repository)

    for hotel in HotelType:
        bookings = repository.get_by_hotel(hotel)
        if not bookings:
            continue

        print(f"\n=== {hotel.value} ===")
        for stats in service.descriptive_stats(hotel):
            print(stats)

        monthly = service.monthly_booking_summary(hotel)
        charts.plot_monthly_bookings(monthly, hotel.value)

        repeated = service.repeated_guest_summary(hotel)
        charts.plot_repeated_guests(repeated, hotel.value)

        traveler = service.traveler_type_summary(hotel)
        charts.plot_traveler_type(traveler, hotel.value)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NF Hotel booking analysis")
    parser.add_argument("--data-path", type=Path, default=DEFAULT_DATA_PATH)
    return parser.parse_args(argv)


if __name__ == "__main__":
    main()
