from initialize import lcu
import json

async def main():
    if lcu.lcu_found:
        rito_ws = await lcu.connect_ws()

    await rito_ws.send(json.dumps([5, "json_events"]))

    while True:
        message = rito_ws.receive()
        print(message)
