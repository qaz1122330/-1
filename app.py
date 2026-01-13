from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('客户端已连接')

if __name__ == '__main__':
    print("🏭 工业仪表读数系统启动")
    print("🌐 访问 http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
