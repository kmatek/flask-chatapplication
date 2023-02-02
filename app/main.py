from typing import Dict, Any

from flaskr import create_app
from flask_socketio import SocketIO

from flaskr.db import Database

JsonDict = Dict[str, Any]

app = create_app()
socketio = SocketIO(app)


@socketio.on('event')
def handle_my_custom_event(json: JsonDict, methods: list = ['POST']) -> None:
    """handling reciving messages"""
    if 'name' in json:
        db = Database()
        db.save_message(json)

    socketio.emit('message response', json)


if __name__ == '__main__':
    socketio.run(app, debug=app.config['FLASK_DEBUG'],
                 host=app.config['HOST'], port=8000)
