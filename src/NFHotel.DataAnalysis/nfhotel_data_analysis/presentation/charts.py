"""Matplotlib rendering for analysis results. No business logic lives here."""

from __future__ import annotations

import matplotlib.pyplot as plt

from ..application.dtos import MonthlyBookingCount, RepeatedGuestSummary, TravelerTypeSummary


def plot_monthly_bookings(summary: list[MonthlyBookingCount], hotel_name: str) -> None:
    months = [item.month for item in summary]
    canceled = [item.canceled for item in summary]
    not_canceled = [item.not_canceled for item in summary]

    _, ax = plt.subplots(figsize=(10, 6))
    ax.bar(months, not_canceled, label="Not canceled")
    ax.bar(months, canceled, bottom=not_canceled, label="Canceled")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of bookings")
    ax.set_title(f"Monthly Booking and Cancellation Status for {hotel_name}")
    ax.legend()
    plt.show()


def plot_repeated_guests(summary: RepeatedGuestSummary, hotel_name: str) -> None:
    _plot_pie(
        sizes=[summary.not_repeated, summary.repeated],
        labels=["Not Repeated Guest", "Repeated Guest"],
        title=f"Distribution of Repeated Guests at {hotel_name}",
    )


def plot_traveler_type(summary: TravelerTypeSummary, hotel_name: str) -> None:
    _plot_pie(
        sizes=[summary.single, summary.family],
        labels=["Single", "Family"],
        title=f"Distribution of Traveler Type at {hotel_name}",
    )


def _plot_pie(sizes: list[int], labels: list[str], title: str) -> None:
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.axis("equal")
    plt.show()
