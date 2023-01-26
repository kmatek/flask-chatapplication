from typing import Dict, Any

from flaskr import create_app
from flask_socketio import SocketIO

JsonDict = Dict[str, Any]

app = create_app()
socketio = SocketIO(app)


@socketio.on('event')
def handle_my_custom_event(json: JsonDict, methods: list = ['POST']):
    """handling reciving messages"""
    socketio.emit('message response', json)


if __name__ == '__main__':
    socketio.run(app, debug=app.config['FLASK_DEBUG'],
                 host=app.config['HOST'], port=8000)
