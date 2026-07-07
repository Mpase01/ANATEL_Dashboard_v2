"""Small local demo API for the ANATEL Dashboard frontend.

This server uses only Python's standard library. It exists so the frontend can
exercise the same API contract before local FastAPI/Supabase credentials are
configured.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


DEMO_PROVIDER = {
    "id": 2,
    "cnpj": "10785849000171",
    "name": "NET-UAI INTERNET WIRELESS",
}

DEMO_SUMMARY = {
    "provider_id": 2,
    "cnpj": "10785849000171",
    "name": "NET-UAI INTERNET WIRELESS",
    "period": "2026-05-01",
    "subscriptions_count": 105,
    "fiber_count": 13,
    "fiber_share_percent": 12.38,
    "market_share_percent": 100,
    "municipalities_count": 2,
    "states_count": 1,
    "top_municipality_name": "Lagoa Formosa",
    "top_municipality_state": "MG",
    "growth_percent": 15.38,
}

DEMO_EVOLUTION = [
    {"period": "2026-01-01", "subscriptions_count": 91},
    {"period": "2026-02-01", "subscriptions_count": 81},
    {"period": "2026-03-01", "subscriptions_count": 92},
    {"period": "2026-04-01", "subscriptions_count": 86},
    {"period": "2026-05-01", "subscriptions_count": 105},
]

DEMO_TECHNOLOGIES = [
    {"technology": "ETHERNET", "access_medium": "Radio", "subscriptions_count": 92, "share_percent": 87.62},
    {"technology": "FTTH", "access_medium": "Fibra", "subscriptions_count": 13, "share_percent": 12.38},
]

DEMO_MUNICIPALITIES = [
    {"municipality_name": "Lagoa Formosa", "state": "MG", "municipality_code": "3137502", "subscriptions_count": 84},
    {"municipality_name": "Patos de Minas", "state": "MG", "municipality_code": "3148004", "subscriptions_count": 21},
]


class DemoApiHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({"status": "ok", "mode": "demo_api"})
            return

        if path == "/providers/search":
            query = parse_qs(parsed.query).get("query", [""])[0].strip().lower()
            digits = "".join(character for character in query if character.isdigit())
            matches_name = query in DEMO_PROVIDER["name"].lower()
            matches_cnpj = bool(digits and digits in DEMO_PROVIDER["cnpj"])
            self._send_json([DEMO_PROVIDER] if matches_name or matches_cnpj or not query else [])
            return

        if path == "/providers/2/summary":
            self._send_json(DEMO_SUMMARY)
            return

        if path == "/providers/2/evolution":
            self._send_json(DEMO_EVOLUTION)
            return

        if path == "/providers/2/technologies":
            self._send_json(DEMO_TECHNOLOGIES)
            return

        if path == "/providers/2/municipalities":
            self._send_json(DEMO_MUNICIPALITIES)
            return

        self._send_json({"detail": "Not found"}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, payload: object, *, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DemoApiHandler)
    print("ANATEL demo API running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
