import os
import json
import time
import threading
import websocket
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "RPC Server Active"

# Limpieza estricta del token
TOKEN = os.environ.get("DISCORD_TOKEN", "").strip().strip('"').strip("'").strip("[").strip("]")

def send_heartbeat(ws, interval_ms):
    interval_sec = interval_ms / 1000.0
    while True:
        time.sleep(interval_sec)
        heartbeat_payload = {"op": 1, "d": None}
        try:
            ws.send(json.dumps(heartbeat_payload))
        except Exception as e:
            print(f"Error en heartbeat: {e}")
            break

def on_message(ws, message):
    data = json.loads(message)
    op = data.get("op")

    if op == 10:  # Opcode 10: Hello
        heartbeat_interval = data["d"]["heartbeat_interval"]
        threading.Thread(target=send_heartbeat, args=(ws, heartbeat_interval), daemon=True).start()
        
        # Payload de identificación ajustado a la API v10
        identify_payload = {
            "op": 2,
            "d": {
                "token": TOKEN,
                "capabilities": 8189,
                "properties": {
                    "os": "Windows",
                    "browser": "Discord Client",
                    "release_channel": "stable",
                    "client_version": "1.0.9015",
                    "os_version": "10.0.19045",
                    "os_arch": "x64",
                    "system_locale": "es-ES",
                    "client_build_number": 210000
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [{
                        "name": "Spotify",
                        "type": 0,  # 0 = Jugando, 2 = Escuchando, 3 = Viendo
                        "details": "Perfil Clean 24/7",
                        "state": "Modo Nube"
                    }],
                    "afk": False
                },
                "compress": False
            }
        }
        ws.send(json.dumps(identify_payload))
        print(">> Identificación enviada con éxito a Discord Gateway v10")

def on_error(ws, error):
    print(f"Error WebSocket: {error}")

def run_rpc():
    if not TOKEN:
        print("ERROR: La variable DISCORD_TOKEN está vacía.")
        return

    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://gateway.discord.gg/?v=10&encoding=json",
                on_message=on_message,
                on_error=on_error
            )
            ws.run_forever()
        except Exception as e:
            print(f"Reconectando por error: {e}")
        time.sleep(5)

threading.Thread(target=run_rpc, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
