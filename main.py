import os
import websocket
import json
import time

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
                    "name": "Spotify",                  # Nombre que saldrá arriba
                    "type": 2,                          # 2 = Escuchando (0=Jugando, 3=Viendo)
                    "details": "Perfil Clean 24/7",     # Texto primera línea
                    "state": "Modo Nube",               # Texto segunda línea
                    "assets": {
                        "large_image": "https://i.imgur.com/tu_imagen_grande.png", 
                        "large_text": "Mi Perfil",
                        "small_image": "https://i.imgur.com/tu_imagen_pequeña.png", 
                        "small_text": "Online"
                    },
                    "buttons": [
                        "Mi Sitio Web",
                        "Mi Red Social"
                    ],
                    "metadata": {
                        "button_urls": [
                            "https://google.com",
                            "https://instagram.com"
                        ]
                    }
                }],
                "status": "online",                      # online, dnd, idle
                "afk": False
            }
        }
    }
    ws.send(json.dumps(auth))

def run():
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_open=on_open
    )
    ws.run_forever()

if __name__ == "__main__":
    run()
