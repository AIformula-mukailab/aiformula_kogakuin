import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver')
        self.subscription = self.create_subscription(
            Image,
            '/aiformula_sensing/zed_node/left/image_rect_color',
            self.listener_callback,
            10)
        self.br = CvBridge()
        self.image_dir = './images'  # 保存するディレクトリのパス
        os.makedirs(self.image_dir, exist_ok=True)
        self.image_count = 0

    def listener_callback(self, msg):
        cv_image = self.br.imgmsg_to_cv2(msg, "bgr8")
        img_path = os.path.join(self.image_dir, f'image_{self.image_count:04d}.jpg')
        cv2.imwrite(img_path, cv_image)
        self.image_count += 1
        self.get_logger().info(f'Saved {img_path}')

def main(args=None):
    rclpy.init(args=args)
    image_saver = ImageSaver()
    rclpy.spin(image_saver)
    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
