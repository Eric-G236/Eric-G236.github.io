"""A tiny local editor for the personal homepage.

Run:
    py web.py

It starts a local server, opens your browser, and lets you edit the content
stored in data.json. When you save, index.html is regenerated automatically.
"""

import base64
import glob
import json
import os
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import build


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
EDITOR_PATH = os.path.join(BASE_DIR, "editor.html")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")


class EditorHandler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path):
        full = os.path.normpath(os.path.join(BASE_DIR, path))
        if not full.startswith(BASE_DIR) or not os.path.isfile(full):
            self._send(404, "Not found")
            return
        content_type = "text/html; charset=utf-8" if path.endswith(".html") else "application/octet-stream"
        with open(full, "rb") as handle:
            self._send(200, handle.read(), content_type)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/editor.html"):
            self._serve_file("editor.html")
        elif path == "/api/data":
            with open(DATA_PATH, "rb") as handle:
                self._send(200, handle.read(), "application/json; charset=utf-8")
        elif path == "/index.html":
            build.generate()
            self._serve_file("index.html")
        else:
            self._send(404, "Not found")

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)

        if path == "/api/upload":
            self._handle_upload(raw)
            return

        if path != "/api/data":
            self._send(404, "Not found")
            return

        try:
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("数据格式必须是 JSON 对象")
        except Exception as exc:
            self._send(400, json.dumps({"ok": False, "error": str(exc)}), "application/json; charset=utf-8")
            return

        with open(DATA_PATH, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

        try:
            build.generate()
        except Exception as exc:
            self._send(500, json.dumps({"ok": False, "error": str(exc)}), "application/json; charset=utf-8")
            return

        self._send(200, json.dumps({"ok": True}), "application/json; charset=utf-8")

    def _handle_upload(self, raw):
        try:
            payload = json.loads(raw.decode("utf-8"))
            data_url = payload.get("data", "")
        except Exception:
            self._send(400, json.dumps({"ok": False, "error": "无法解析上传数据"}), "application/json; charset=utf-8")
            return

        if not data_url.startswith("data:") or "," not in data_url:
            self._send(400, json.dumps({"ok": False, "error": "无效的图片数据"}), "application/json; charset=utf-8")
            return

        meta, b64 = data_url.split(",", 1)
        mime = meta.split(";")[0].split(":")[1] if ":" in meta else ""
        ext_map = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/webp": "webp",
            "image/gif": "gif",
        }
        ext = ext_map.get(mime)
        if not ext:
            self._send(400, json.dumps({"ok": False, "error": "仅支持 JPG、PNG、WebP、GIF 图片"}), "application/json; charset=utf-8")
            return

        try:
            content = base64.b64decode(b64)
        except Exception:
            self._send(400, json.dumps({"ok": False, "error": "图片解码失败"}), "application/json; charset=utf-8")
            return

        for old_ext in ("jpg", "jpeg", "png", "webp", "gif"):
            for old_path in glob.glob(os.path.join(BASE_DIR, f"photo.{old_ext}")):
                try:
                    os.remove(old_path)
                except OSError:
                    pass

        filename = f"photo.{ext}"
        with open(os.path.join(BASE_DIR, filename), "wb") as handle:
            handle.write(content)

        self._send(200, json.dumps({"ok": True, "filename": filename}), "application/json; charset=utf-8")

    def log_message(self, format, *args):
        print(format % args)


def main():
    host = "127.0.0.1"
    server = None
    for port in range(8765, 8780):
        try:
            server = HTTPServer((host, port), EditorHandler)
            break
        except OSError:
            continue
    if server is None:
        print("无法启动编辑器：8765-8779 端口都被占用。")
        return

    url = f"http://{host}:{port}/editor.html"
    print("个人主页编辑器已启动：", url)
    print("关闭编辑器请回到这个窗口按 Ctrl+C。")
    if os.environ.get("EDITOR_NO_BROWSER") != "1":
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
