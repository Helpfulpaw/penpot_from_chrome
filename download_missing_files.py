import os
import sys
from urllib.request import urlopen

FILES = {
    "penpot-extension/icons/icon16.png": "https://raw.githubusercontent.com/penpot/penpot-desktop/main/assets/icons/icon16.png",
    "penpot-extension/icons/icon48.png": "https://raw.githubusercontent.com/penpot/penpot-desktop/main/assets/icons/icon48.png",
    "penpot-extension/icons/icon128.png": "https://raw.githubusercontent.com/penpot/penpot-desktop/main/assets/icons/icon128.png",
    "penpot-extension/libs/jszip.min.js": "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.0/jszip.min.js"
}


def download(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with urlopen(url) as resp, open(path, "wb") as out:
        out.write(resp.read())


def main():
    for path, url in FILES.items():
        if os.path.exists(path) and os.path.getsize(path) > 20:
            continue
        try:
            print(f"Fetching {url} -> {path}")
            download(url, path)
        except Exception as e:
            print(f"Failed to download {url}: {e}")


if __name__ == "__main__":
    main()
