# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-file HTML prototype (`lease_extractor_prototype.html`) that extracts commercial real estate lease terms from raw text and renders them in a structured UI. No build step, no dependencies, no server — open the file directly in a browser.

## How to run

Open `lease_extractor_prototype.html` directly in a browser. No build or install required.

## Architecture

Everything lives in one file with three logical layers:

**Extraction engine (`extract()`)** — Pure regex/heuristic parser. Takes raw lease text and returns a structured `D` object with fields like `landlord_name`, `tenant_name`, `property_address`, `commencement_date`, `expiration_date`, `lease_type`, `security_deposit`, `rent_schedule`, `total_rent`, `avg_rate`. Helper functions: `extractDate()` for date parsing with multiple format fallbacks, `parseW()` for written-number amounts (e.g. "three thousand"), `buildSeasonal()` for seasonal rent schedules (high Nov–Mar / low Apr–Oct).

**State** — Single global `D` holds the parsed data object. `null` when no lease is loaded. UI reads from `D` on every re-render; dropdowns and inputs in the selectors panel override extracted values at render time without mutating `D`.

**Render layer** — `render(d)` calls `renderBroker()`, `renderProperty()`, `renderTransaction()`, `renderRentSchedule()`. Transaction data merges extracted `D` values with the selectors panel (agreement type, deal type, lease type, commission units) so user overrides are applied live. `renderTransaction()` is also re-run whenever a selector changes.

## Programmatic data loading (Claude integration)

The intended workflow when Claude reads a lease PDF: Claude calls `window.loadLeaseData(data)` directly in the browser console with a structured JSON object matching the `D` schema. This bypasses the regex extractor entirely and populates the UI from Claude's own parsing. The `rent_schedule` array items need: `start`, `end`, `monthly_rent` (formatted string like `"$4,500.00"`), `months`, `total` (number).

## CSV export

`getCSV()` serializes the current state of `D` plus selector panel values into a flat CSV row. Headers are hardcoded. `copyCSV()` and `downloadCSV()` both call `getCSV()`.

## Key data shape

```js
// D object structure
{
  landlord_name, tenant_name, property_address, suite, sqft, prop_type,
  commencement_date,   // "MM/DD/YYYY"
  expiration_date,     // "MM/DD/YYYY"
  term_months,         // integer
  lease_type,          // "NNN" | "Gross" | "Modified Gross" | "Modified Net" | "Full Service" | "Ground Lease"
  security_deposit,    // "$X,XXX.XX" string or null
  total_rent,          // number (sum of rent_schedule totals)
  avg_rate,            // "X.XX" string ($/SF/Year)
  rent_schedule: [{ start, end, monthly_rent, months, total }]
}
```
