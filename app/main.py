from flaskr import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app, debug=app.config['FLASK_DEBUG'],
                 host=app.config['HOST'], port=8000)
