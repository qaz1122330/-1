import numpy as np

class MeterDetector:
    """仪表检测与读数模拟器"""
    
    def __init__(self):
        self.meter_count = 2
    
    def process_frame(self, frame_data=None):
        """处理帧数据（模拟版）"""
        import time
        
        # 模拟两个仪表的读数
        readings = []
        for i in range(self.meter_count):
            # 模拟读数（45-55之间波动）
            import random
            value = 50 + random.uniform(-5, 5)
            
            # 判断状态
            if value > 90:
                status = "danger"
            elif value > 80:
                status = "warning"
            else:
                status = "normal"
            
            readings.append({
                "id": i,
                "value": round(value, 2),
                "angle": int((value / 100) * 270),
                "status": status,
                "confidence": 0.92
            })
        
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "readings": readings,
            "frame": None  # 实际项目中这里是base64编码的图像
        }
