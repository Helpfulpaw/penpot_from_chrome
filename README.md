# Penpot Exporter Prototype

An early Chrome Extension Manifest V3 experiment for exploring how a webpage could be captured and converted into an artifact that can be recreated in Penpot.

> **Status:** incomplete proof of concept. The extension currently opens a popup and dispatches an `export` message to the active tab. It does **not** yet extract the page, create a Penpot-compatible file, or import anything into Penpot.

## What exists today

- A Manifest V3 browser-extension scaffold
- A popup with an export action
- A content script that receives the export message
- A helper script for downloading local icon and JSZip assets

The current runtime path is deliberately small:

```text
Popup button
    -> chrome.tabs.sendMessage(...)
    -> content script receives { action: "export" }
    -> placeholder console message
```

## What is not implemented

- DOM, style, layout, or component extraction
- Font, image, SVG, and asset collection
- Normalization of browser layout into Penpot concepts
- Generation of a Penpot-compatible artifact
- Penpot API authentication or import
- Progress reporting and user-facing errors
- Automated tests and release packaging

## Load the prototype locally

1. Clone the repository.
2. Fetch the placeholder assets:

```bash
python3 download_missing_files.py
```

3. Open `chrome://extensions` in Chrome.
4. Enable **Developer mode**.
5. Select **Load unpacked** and choose the `penpot-extension/` directory.
6. Open a normal webpage and click the extension action.

At this stage, clicking **Export** only sends the message and writes a placeholder entry to the page console.

## Security and release constraints

The current manifest injects a content script into `<all_urls>` and requests access to the active tab. That is acceptable for a local experiment but too broad for distribution. Before any release:

- restrict host permissions to the minimum required scope;
- document exactly what page data is collected;
- keep captured data local unless the user explicitly initiates transmission;
- review and pin all downloaded third-party assets;
- add tests for messaging, extraction, and failure handling.

## Suggested implementation stages

1. Define a small supported subset: text, boxes, spacing, colors, and basic images.
2. Produce a neutral intermediate representation independent of Penpot.
3. Add deterministic DOM and computed-style extraction.
4. Build a converter from the intermediate representation to a supported Penpot import path.
5. Add visual comparison fixtures and regression tests.
6. Narrow permissions, document privacy behavior, and package a reproducible release.

## Repository map

```text
.
├── download_missing_files.py
└── penpot-extension/
    ├── manifest.json
    ├── popup.html
    ├── popup.js
    ├── content.js
    ├── icons/
    └── libs/
```

## License

No license has been selected yet. Treat the repository as a research prototype until licensing and third-party asset provenance are documented.
