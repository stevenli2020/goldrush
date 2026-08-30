# L0-001 — Above-Ground Gold Stock

Phase 3 uses the live World Gold Council above-ground-stocks workbook and the
approved Phase 2 parser. The canonical value is `total_above_ground_tonnes`,
with annual observations dated 31 December. The component breakdown remains in
the Phase 2 processed output and is supporting evidence.

The Phase 3 handoff contains one row per annual observation with metric-tonne
units, WGC manifest provenance, `AVAILABLE` status, and `PASS` quality status.
The handoff refuses invalid or unavailable input; it never carries forward or
substitutes a stock value.
