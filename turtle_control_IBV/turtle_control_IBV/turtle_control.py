import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class ControlTurtle(Node):

    def __init__(self):
        super().__init__('control_turtle')
        self.init_variables()
        self.init_publishers()
        self.init_subscribers()        

    def init_variables(self):
        self.x = 0.0
        self.x_error = 0.0
        self.x_goal = 5.0        
        self.y = 0.0 
        self.y_error = 5.0
        self.y_goal = 0.0 
        self.k_omega = 1.5 
        self.theta = 0.0 
        self.p = 0.0
        self.alpha = 0.0
        self.v_max = 1.0

    def init_publishers(self):
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def init_subscribers(self):
        self.subscription = self.create_subscription(Pose,'turtle1/pose', self.listener_callback, 10)
        self.subscription_pose = self.create_subscription(Pose2D,'goal',self.goal_callback,10)
        # Prevenir possíveis warnings de variáveis não utilizadas
        self.subscription 
        self.subscription_pose

    def listener_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta
        # self.get_logger().info('Value: "%f"' % self.theta)


    def goal_callback(self, msg):
        self.x_goal = msg.x
        self.y_goal = msg.y

    def timer_callback(self):
        msg = Twist()
        # Calculando primeiramente os erros de localização do robô
        self.x_error = self.x_goal - self.x
        self.y_error = self.y_goal - self.y
        self.get_logger().info('X erro: "%f"' % self.x_error)
        self.get_logger().info('Y erro: "%f"' % self.y_error)

        if not(abs(self.x_error) < 0.15 and (self.y_error) < 0.15):
            self.p = math.sqrt(pow(self.x_error, 2) + pow(self.y_error, 2))
            self.alpha = math.atan2(self.y_error,self.x_error) - (self.theta)
        else:
            self.p = 0.0
            self.alpha = 0.0
        msg.linear.x = self.v_max * math.tanh(self.p)
        msg.linear.y = 0.0
        msg.angular.z = self.k_omega * self.alpha
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    turtle_object = ControlTurtle()

    rclpy.spin(turtle_object)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtle_object.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
