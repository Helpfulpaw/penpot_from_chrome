import argparse
import os
import sys
import urllib.request
import shutil
import zlib
import struct
import binascii

MANIFEST = '''{
  "manifest_version": 3,
  "name": "HTML to Penpot Converter",
  "version": "1.0",
  "description": "Convert current page into a Penpot .penpot file",
  "permissions": ["activeTab", "scripting", "downloads"],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ],
  "web_accessible_resources": [
    {
      "resources": ["libs/jszip.min.js"],
      "matches": ["<all_urls>"]
    }
  ]
}
'''

POPUP_HTML = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Export to Penpot</title>
</head>
<body>
  <button id="export">Export Current Page</button>
  <script src="popup.js"></script>
</body>
</html>
'''

POPUP_JS = '''document.getElementById('export').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    const tab = tabs[0];
    chrome.tabs.sendMessage(tab.id, {action: 'extractDOM'}, (response) => {
      if (!response) {
        console.error('No response from content script');
        return;
      }
      const script = document.createElement('script');
      script.src = chrome.runtime.getURL('libs/jszip.min.js');
      script.onload = () => {
        const zip = new JSZip();
        zip.file('design.json', JSON.stringify(response.elements, null, 2));
        zip.generateAsync({type: 'blob'}).then((blob) => {
          const url = URL.createObjectURL(blob);
          chrome.downloads.download({url, filename: document.title + '.penpot'});
        });
      };
      document.body.appendChild(script);
    });
  });
});
'''

CONTENT_JS = '''chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'extractDOM') {
    const result = [];
    document.querySelectorAll('h1,h2,h3,p,img').forEach(el => {
      const rect = el.getBoundingClientRect();
      result.push({
        tag: el.tagName.toLowerCase(),
        text: el.innerText || null,
        src: el.src || null,
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height
      });
    });
    sendResponse({elements: result});
  }
});
'''

def log(info):
    print(f"[INFO] {info}")

def error(msg):
    print(f"[ERROR] {msg}")

def confirm(prompt):
    ans = input(f"{prompt} (y/n): ").strip().lower()
    return ans == 'y'

def create_png(path, size, color):
    width = height = size
    r, g, b, a = color
    raw = bytes([0, r, g, b, a] * width) * height
    compressor = zlib.compressobj()
    compressed = compressor.compress(raw) + compressor.flush()
    def chunk(tag, data):
        return struct.pack('!I', len(data)) + tag + data + struct.pack('!I', binascii.crc32(tag + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    log(f"Created icon {path}")

TEMPLATE_ICONS = {
    16: (255, 0, 0, 255),
    48: (0, 255, 0, 255),
    128: (0, 0, 255, 255)
}

def main():
    parser = argparse.ArgumentParser(description='Generate Penpot browser extension')
    parser.add_argument('-o', '--output-dir', default='penpot-extension', help='Output directory')
    parser.add_argument('--jszip-url', default='https://cdn.jsdelivr.net/npm/jszip@3.10.0/dist/jszip.min.js', help='URL to jszip.min.js')
    parser.add_argument('--icons-source-url', help='Directory or URL to load icons from')
    args = parser.parse_args()

    out = args.output_dir
    if os.path.exists(out) and os.listdir(out):
        if not confirm(f"Directory {out} exists and is not empty. Overwrite?"):
            sys.exit(0)
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'libs'), exist_ok=True)
    os.makedirs(os.path.join(out, 'icons'), exist_ok=True)
    log(f"Created directory structure at {out}")

    files = {
        'manifest.json': MANIFEST,
        'popup.html': POPUP_HTML,
        'popup.js': POPUP_JS,
        'content.js': CONTENT_JS
    }
    for name, content in files.items():
        path = os.path.join(out, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"Created {name}")

    jszip_dest = os.path.join(out, 'libs', 'jszip.min.js')
    try:
        urllib.request.urlretrieve(args.jszip_url, jszip_dest)
        log(f"Downloaded jszip to {jszip_dest}")
    except Exception as e:
        error(f"Failed to download jszip: {e}")
        sys.exit(1)

    if args.icons_source_url:
        if os.path.isdir(args.icons_source_url):
            for size in [16, 48, 128]:
                src = os.path.join(args.icons_source_url, f'icon{size}.png')
                dest = os.path.join(out, 'icons', f'icon{size}.png')
                try:
                    shutil.copyfile(src, dest)
                    log(f"Copied icon {src}")
                except Exception as e:
                    error(f"Failed to copy {src}: {e}")
                    create_png(dest, size, TEMPLATE_ICONS[size])
        else:
            base = args.icons_source_url.rstrip('/')
            for size in [16, 48, 128]:
                url = f"{base}/icon{size}.png"
                dest = os.path.join(out, 'icons', f'icon{size}.png')
                try:
                    urllib.request.urlretrieve(url, dest)
                    log(f"Downloaded icon {url}")
                except Exception as e:
                    error(f"Failed to download {url}: {e}")
                    create_png(dest, size, TEMPLATE_ICONS[size])
    else:
        for size in [16, 48, 128]:
            dest = os.path.join(out, 'icons', f'icon{size}.png')
            create_png(dest, size, TEMPLATE_ICONS[size])

    log(f"\u2705 Extension built in {os.path.abspath(out)}")
    log("Load it in Chrome: Extensions -> Load unpacked")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        error('Interrupted')
        sys.exit(1)
