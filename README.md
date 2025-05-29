# Penpot Extension Generator

This repository contains a script to generate a browser extension that converts the current page to a Penpot `.penpot` file.

## Requirements
* Python 3.10+

## Usage
Run the generator script:

```bash
python create_extension.py
```

Optional arguments:

- `-o, --output-dir` – directory to create the extension in (default `penpot-extension`).
- `--jszip-url` – URL to download `jszip.min.js`.
- `--icons-source-url` – local directory or URL containing `icon16.png`, `icon48.png` and `icon128.png`.

If the target directory exists, you will be asked whether to overwrite it.

After running the script, load the generated extension in Chrome/Edge via **Extensions → Load unpacked**.
