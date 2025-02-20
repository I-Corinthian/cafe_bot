import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/i_corinthian/Documents/ros/ros_assesment/ros2_ws/install/cafe_bot'
