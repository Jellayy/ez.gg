"""
Driver for the Server Sent Events message queue used to send ad-hoc messages to the UI

Supported Event Types:

Generic Message:
{
    "event": "display_message",
    "data": {
        "title": str,
        "message": str,
        "type": str('success', 'info', 'warning', 'error'),
        "duration": int(optional)
    }
}

Queue Status Update:
{
    "event": "queue_status_update",
    "data": {
        "status": str('Invalid', 'Searching', other)
    }
}
"""
import json
import logging

from queue import Queue
from flask import Response, Blueprint


sse = Blueprint('sse', __name__)
message_queue = Queue()


def send_event_to_ui(message):
    message_queue.put(message)


def register_routes(app):
    app.register_blueprint(sse)


def format_sse(data: dict, event=None) -> str:
    json_data = json.dumps(data)
    msg = f'data: {json_data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@sse.route('/stream')
async def stream():
    def event_stream():
        while True:
            message = message_queue.get()
            yield format_sse(json.dumps(message), event='broadcast')
    return Response(event_stream(), mimetype="text/event-stream")
