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

TOKEN = os.environ.get("DISCORD_TOKEN")

def send_heartbeat(ws, interval_ms):
    interval_sec = interval_ms / 1000.0
    while True:
        time.sleep(interval_sec)
        heartbeat_payload = {"op": 1, "d": None}
        try:
            ws.send(json.dumps(heartbeat_payload))
        except Exception as e:
            print(f"Error enviando heartbeat: {e}")
            break

def on_message(ws, message):
    data = json.loads(message)
    op = data.get("op")

    # Opcode 10: Hello de Discord
    if op == 10:
        heartbeat_interval = data["d"]["heartbeat_interval"]
        
        # Iniciar el envío de heartbeat periódico
        threading.Thread(target=send_heartbeat, args=(ws, heartbeat_interval), daemon=True).start()
        
        # Enviar Identify (Autenticación + Actividad)
        identify_payload = {
            "op": 2,
            "d": {
                "token": TOKEN,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "browser_version": "115.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 223400,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [{
                        "name": "Spotify 24/7",
                        "type": 0,  # 0 = Jugando, 2 = Escuchando, 3 = Viendo
                        "details": "Perfil Activo",
                        "state": "Modo Nube"
                    }],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {}
                }
            }
        }
        ws.send(json.dumps(identify_payload))
        print(">> Autenticación enviada exitosamente a Discord")

def on_error(ws, error):
    print(f"Error WebSocket: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Conexión cerrada: {close_status_code} - {close_msg}")

def run_rpc():
    if not TOKEN:
        print("ERROR: No se encontró la variable DISCORD_TOKEN")
        return

    # Limpiar posibles espacios accidentales en el token
    clean_token = TOKEN.strip().strip('"').strip("'")

    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://gateway.discord.gg/?v=9&encoding=json",
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        except Exception as e:
            print(f"Reconectando... Error: {e}")
        time.sleep(5)

# Iniciar WebSocket en un hilo secundario
threading.Thread(target=run_rpc, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
