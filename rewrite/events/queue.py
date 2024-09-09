import json
import requests
import logging

class Queue:
    def __init__(self, client):
        self.client = client

    async def queue_pop_status(self) -> bool:
        uri = "lol-matchmaking/v1/ready-check"
        response = self.client.get(uri)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("state") == "InProgress" and response_json.get("playerResponse") == "None":
                logging.debug(f"Queue Popped: {response.text}")
                return True
        return False
    
    async def queue_accept(self) -> bool:
        uri = "lol-matchmaking/v1/ready-check/accept"
        response = self.client.post(uri)
        logging.debug(f"Queue Acceptor: {response.text}")
        if response.status_code == 204:
            logging.debug(f"Queue Acceptor: Queue Accepted! (status {response.status_code})")
            return True
        else:
            logging.error(f"Queue Acceptor: Queue unable to be accepted with status: {response.status_code}")
            return False
        



async def queue_handler(message, client):
    logging.debug(f"Queue Handler: {message}")
    queue = Queue(client)
    if await queue.queue_pop_status():
        logging.debug("Queue Handler: Queue Popped")
        await queue.queue_accept()
        logging.debug("Queue Handler: Queue Accepted")
    
