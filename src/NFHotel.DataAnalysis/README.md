# NFHotel.DataAnalysis

Hotel booking analysis, refactored out of [`src/ipynb/data-analyse-example.ipynb`](../ipynb/data-analyse-example.ipynb)
into a clean-architecture Python package that mirrors the layering used by the
rest of the NFHotel solution (`Domain` / `Application` / `Infrastructure` / `Web`).

## Layers

- `nfhotel_data_analysis/domain` — the `Booking` entity and `HotelType` enum.
  Pure Python, no pandas, no I/O. Business rules (e.g. what counts as a
  "family booking") live here.
- `nfhotel_data_analysis/application` — use cases (`HotelAnalysisService`)
  that compute descriptive stats and the monthly/repeat-guest/traveler-type
  summaries. Depends only on the `BookingRepository` port, so it's unit
  tested with an in-memory fake and no spreadsheet.
- `nfhotel_data_analysis/infrastructure` — `ExcelBookingRepository`, the only
  module that knows about pandas/openpyxl and the source spreadsheet's
  column layout.
- `nfhotel_data_analysis/presentation` — `charts.py` (matplotlib rendering)
  and `cli.py` (the composition root that wires the Excel repository to the
  analysis service and prints/plots the results).

Dependencies point inward: `presentation` → `infrastructure`/`application` →
`domain`. The domain layer has no dependency on pandas or any other layer.

## Running

```bash
pip install -e ".[dev]"
python -m nfhotel_data_analysis.presentation.cli --data-path ../ipynb/hotel_bookings.xlsx
```

## Testing

```bash
pytest
```
