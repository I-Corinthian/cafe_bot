import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import tkinter as tk
from tkinter import ttk

class NavGoalPublisher(Node):
    def __init__(self):
        super().__init__('nav_goal_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, 'goal_pose', 10)
        # Define preset points: home, kitchen, and tables
        self.points = {
            'home':    {'x': 0.003019, 'y': 0.000008,  'w': 1.0},
            'kitchen': {'x': 1.7344117164611816, 'y': 0.20714068412780762,  'w': 1.0},
            'table1':  {'x': -0.000001, 'y': 0.654509,  'w': 1.0},
            'table2':  {'x': -0.933329, 'y': 0.007827,  'w': 1.0},
            'table3':  {'x': 1.247948,  'y': -0.237344, 'w': 1.0}
        }

    def publish_goal(self, point_name: str):
        """Publish a goal to the goal_pose topic based on the given point name."""
        if point_name not in self.points:
            self.get_logger().error(f"Point {point_name} is not defined!")
            return

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()

        point = self.points[point_name]
        goal.pose.position.x = point['x']
        goal.pose.position.y = point['y']
        goal.pose.position.z = 0.0
        # Set a default orientation (no rotation)
        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = 0.0
        goal.pose.orientation.w = point.get('w', 1.0)

        self.publisher_.publish(goal)
        self.get_logger().info(f"Published goal for '{point_name}': x={point['x']}, y={point['y']}")

class CafeBotUI:
    def __init__(self, node):
        self.node = node
        self.root = tk.Tk()
        self.root.title("Cafe Bot Order System")
        
        # Variables for selections
        self.selected_table = tk.StringVar(value="table1")
        self.selected_food = tk.StringVar(value="Pizza")
        
        # Define available tables and foods
        self.tables = ["table1", "table2", "table3"]
        self.foods = ["Pizza", "Burger", "Salad", "Pasta"]

        # Create the initial order screen
        self.create_order_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_order_screen(self):
        self.clear_screen()
        title = tk.Label(self.root, text="Place Your Order", font=("Helvetica", 16))
        title.pack(pady=10)

        # Table selection dropdown
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=5)
        tk.Label(table_frame, text="Select Table:").pack(side=tk.LEFT, padx=5)
        table_dropdown = ttk.OptionMenu(table_frame, self.selected_table, self.tables[0], *self.tables)
        table_dropdown.pack(side=tk.LEFT)

        # Food selection dropdown
        food_frame = tk.Frame(self.root)
        food_frame.pack(pady=5)
        tk.Label(food_frame, text="Select Food:").pack(side=tk.LEFT, padx=5)
        food_dropdown = ttk.OptionMenu(food_frame, self.selected_food, self.foods[0], *self.foods)
        food_dropdown.pack(side=tk.LEFT)

        # Button to place order
        order_btn = tk.Button(self.root, text="Place Order", command=self.handle_order)
        order_btn.pack(pady=20)

    def handle_order(self):
        # Retrieve user selections (food can be used to update UI or logs)
        table = self.selected_table.get()
        food = self.selected_food.get()
        print(f"Order received: {food} for {table}")
        
        # Step 1: Publish goal to kitchen
        self.node.publish_goal('kitchen')
        self.create_kitchen_screen()

    def create_kitchen_screen(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Robot is in the Kitchen.\nPress 'Food Delivered' when ready.", font=("Helvetica", 16))
        label.pack(pady=20)
        deliver_btn = tk.Button(self.root, text="Food Delivered", command=self.handle_kitchen_delivered)
        deliver_btn.pack(pady=20)

    def handle_kitchen_delivered(self):
        # Step 2: Publish goal to the selected table
        table = self.selected_table.get()
        self.node.publish_goal(table)
        self.create_table_screen(table)

    def create_table_screen(self, table):
        self.clear_screen()
        label = tk.Label(self.root, text=f"Robot has arrived at {table}.\nPress 'Go Home' to return home.", font=("Helvetica", 16))
        label.pack(pady=20)
        home_btn = tk.Button(self.root, text="Go Home", command=self.handle_go_home)
        home_btn.pack(pady=20)

    def handle_go_home(self):
        # Step 3: Publish goal to home and then loop back to initial order screen
        self.node.publish_goal('home')
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Robot is back Home.\nPress 'New Order' to place another order.", font=("Helvetica", 16))
        label.pack(pady=20)
        new_order_btn = tk.Button(self.root, text="New Order", command=self.create_order_screen)
        new_order_btn.pack(pady=20)

    def run(self):
        self.root.mainloop()

def main(args=None):
    rclpy.init(args=args)
    node = NavGoalPublisher()
    ui = CafeBotUI(node)
    try:
        ui.run()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Cafe Bot UI")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
