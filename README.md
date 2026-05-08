# Lease Extractor

A single-file browser prototype that extracts commercial real estate lease terms from raw text and renders them in a structured UI.

## Usage

Open `index.html` directly in a browser — no build step, no server, no dependencies.

Paste raw lease text into the input area and click **Extract**. The tool parses fields like landlord/tenant names, property address, lease dates, rent schedule, and total consideration.

## Claude integration

When Claude reads a lease PDF, it can call `window.loadLeaseData(data)` in the browser console with a structured JSON object to bypass the regex extractor and populate the UI directly from Claude's parsing.

## Export

Use **Copy CSV** or **Download CSV** to export the extracted data as a flat CSV row for use in a spreadsheet or CRM.
