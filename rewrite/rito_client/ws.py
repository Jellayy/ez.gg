from initialize import lcu
import json
from websockets.asyncio.client import connect
import websockets
import ssl
from rito_client.queue import queue_handler
import logging

async def connect_ws(lcu):
    uri = f"wss://riot:{lcu._lcu_token}@127.0.0.1:{lcu._lcu_port}"

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    return uri, ssl_context

async def main():
    if lcu.lcu_found:
        print(lcu._lcu_auth)
        uri, ssl_context = await connect_ws(lcu)

        async with connect(uri, ssl=ssl_context, max_size=None) as rito_ws:
            message = json.dumps([5, "OnJsonApiEvent"])
            await rito_ws.send(message=message)

            try:
                await rito_ws.send(message=message)
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed normally.")
            except Exception as e:
                print(f"An error occurred: {e}")

            while True:
                try:
                    message = await rito_ws.recv()
                    if not message:
                        logging.debug("Received empty message")
                    else:
                        message = json.loads(message)
                        # handle queue pop
                        if message[2].get("uri") == "/lol-matchmaking/v1/ready-check":
                            await queue_handler(message, lcu)

                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed normally.")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break