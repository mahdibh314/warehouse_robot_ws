import threading

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from fastapi.middleware.cors import CORSMiddleware
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

from fastapi import FastAPI
import uvicorn

from fastapi.responses import StreamingResponse
import time


class DashboardNode(Node):
    def __init__(self):
        super().__init__('dashboard_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.timer = self.create_timer(0.1, self.publish_velocity)
        self.subscription = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )
        self.image_subscription = self.create_subscription(
            Image, '/image_raw', self.image_callback, 10
        )
        self.bridge = CvBridge()
        self.latest_frame = None
        self.last_position = {'x': 0.0, 'y': 0.0}
        self.get_logger().info('Dashboard node started')

    def set_velocity(self, linear_x, angular_z):
        self.current_linear = linear_x
        self.current_angular = angular_z

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = self.current_linear
        msg.angular.z = self.current_angular
        self.cmd_vel_publisher.publish(msg)

    def odom_callback(self, msg):
        self.last_position['x'] = msg.pose.pose.position.x
        self.last_position['y'] = msg.pose.pose.position.y
    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        success, jpeg = cv2.imencode('.jpg', cv_image)
        if success:
            self.latest_frame = jpeg.tobytes()
ros_node = None
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def read_root():
    return {'status': 'Warehouse robot dashboard is running'}


@app.post('/move')
def move(linear_x: float, angular_z: float):
    ros_node.set_velocity(linear_x, angular_z)
    return {'linear_x': linear_x, 'angular_z': angular_z}


@app.post('/stop')
def stop():
    ros_node.set_velocity(0.0, 0.0)
    return {'status': 'stopped'}

@app.get('/status')
def status():
    return {'position': ros_node.last_position}

@app.get('/video_feed')
def video_feed():
    def generate():
        while True:
            if ros_node.latest_frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + ros_node.latest_frame + b'\r\n')
            time.sleep(0.05)

    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

def ros_spin_thread():
    rclpy.spin(ros_node)


def main(args=None):
    global ros_node
    rclpy.init(args=args)
    ros_node = DashboardNode()

    spin_thread = threading.Thread(target=ros_spin_thread, daemon=True)
    spin_thread.start()

    uvicorn.run(app, host='0.0.0.0', port=8000)

    ros_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

