import os
import websocket
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ.get("DISCORD_TOKEN")

# Servidor web simple para que Render reconozca el Web Service Gratuito
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RPC Active")

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def send_heartbeat(ws, interval):
    while True:
        time.sleep(interval)
        heartbeat_g = {"op": 1, "d": None}
        try:
            ws.send(json.dumps(heartbeat_g))
        except:
            break

def on_open(ws):
    auth = {
        "op": 2,
        "d": {
            "token": TOKEN,
            "properties": {
                "$os": "Windows",
                "$browser": "Discord Client",
                "$device": "Desktop"
            },
            "presence": {
                "activities": [{
                    "name": "Spotify",
                    "type": 2,
                    "details": "Perfil Clean 24/7",
                    "state": "Modo Nube",
                    "assets": {
                        "large_image": "https://i.imgur.com/tu_imagen_grande.png",
                        "large_text": "Mi Perfil"
                    }
                }],
                "status": "online",
                "afk": False
            }
        }
    }
    ws.send(json.dumps(auth))

def run_rpc():
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_open=on_open
    )
    ws.run_forever()

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    run_rpc()
