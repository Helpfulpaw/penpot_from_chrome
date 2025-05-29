# Penpot from Chrome

This repository contains a browser extension that exports designs directly to Penpot.
The previous Python helper service has been removed.

## Status
Work in progress. The extension lives in the `penpot-extension/` directory.

## Development
Clone the repo and install dependencies with `npm install`. Load the extension in Chrome using the `penpot-extension/` folder. When testing the popup, make sure the active tab is a normal webpage (not a Chrome Web Store or `chrome://` page) so that the content script can receive messages.

If any icon or library files are missing, run `python download_missing_files.py` to fetch them.
