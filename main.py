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
    if not TOKEN:
        print("TOKEN NO ENCONTRADO EN VARIABLES DE ENTORNO")
        return
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_open=on_open
    )
    ws.run_forever()

# Iniciar hilo de Discord
threading.Thread(target=run_rpc, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
