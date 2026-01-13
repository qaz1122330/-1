from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
import time
import random
import base64
import cv2
import numpy as np

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 模拟视频生成器
class VideoSimulator:
    def get_frame(self):
        # 创建模拟仪表图像
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 240
        
        # 绘制两个模拟仪表
        for i in range(2):
            center_x = 200 + i * 250
            center_y = 240
            radius = 100
            
            # 画外圈
            cv2.circle(frame, (center_x, center_y), radius, (0, 0, 0), 3)
            
            # 画指针（随机角度）
            angle = random.randint(0, 270) - 45
            rad = np.deg2rad(angle)
            x_end = int(center_x + (radius-20) * np.cos(rad))
            y_end = int(center_y + (radius-20) * np.sin(rad))
            cv2.line(frame, (center_x, center_y), (x_end, y_end), (0, 0, 255), 3)
        
        # 转换为base64
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

video_sim = VideoSimulator()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('客户端已连接')
    emit('connection_response', {'data': 'Connected successfully'})

@socketio.on('start_monitoring')
def handle_start_monitoring():
    """开始发送模拟数据"""
    print('开始监控...')
    
    try:
        while True:
            # 生成模拟读数
            readings = []
            for i in range(2):
                value = 50 + random.uniform(-5, 5)
                status = "normal" if value < 80 else "warning" if value < 90 else "danger"
                
                readings.append({
                    "id": i,
                    "value": round(value, 2),
                    "angle": int((value / 100) * 270),
                    "status": status,
                    "confidence": 0.95
                })
            
            # 发送数据到前端
            socketio.emit('meter_data', {
                "timestamp": time.strftime("%H:%M:%S"),
                "readings": readings,
                "frame": video_sim.get_frame()
            })
            
            # 每秒发送5次数据
            socketio.sleep(0.2)
            
    except Exception as e:
        print(f'监控出错: {e}')

if __name__ == '__main__':
    print("🏭 工业仪表读数系统启动成功！")
    print("📡 WebSocket服务运行中...")
    print("🌐 请访问: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
