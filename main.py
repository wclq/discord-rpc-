import os
import websocket
import json
import time
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "RPC Active"

TOKEN = os.environ.get("DISCORD_TOKEN")

def on_open(ws):
    # Identificación
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
                    "name": "Spotify 24/7",
                    "type": 2,  # Escuchando
                    "details": "Perfil Activo",
                    "state": "Modo Nube"
                }],
                "status": "online",
                "afk": False
            }
        }
    }
    ws.send(json.dumps(auth))

def run_rpc():
    if not TOKEN:
        return
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_open=on_open
    )
    ws.run_forever()

threading.Thread(target=run_rpc, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
