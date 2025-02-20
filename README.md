# Cafe Bot 

This project demonstrates a simple ROS2-based navigation system for a cafe robot using TurtleBot2 and the Nav2 stack. The robot navigates to preset locations in a cafe environment including **Home**, **Kitchen**, and several **Tables**. It features a user-friendly Tkinter GUI where users can select an order, and the robot will autonomously navigate through the following sequence:

1. **Kitchen:** When an order is placed, the robot first moves from Home to the Kitchen.
2. **Delivery:** After a confirmation (via the GUI), the robot then goes to the selected table (Table1, Table2, or Table3) to deliver the order.
3. **Return Home:** Finally, once the delivery is confirmed, the robot returns back Home, ready for the next order.

## How to Run the Project

Run the following commands in separate terminals (or in sequence as required) to start the simulation, the navigation stack, and the interactive navigation node:

1. **Launch the simulation environment:**
   ```bash
   ros2 launch cafe_bot launch_sim.launch.py
   ```

2. **Launch the navigation stack:**
   ```bash
   ros2 launch cafe_bot nav_launch.py
   ```

3. **Run the navigation goal publisher (with the GUI):**
   ```bash
   ros2 run cafe_bot nav_goal_publisher
   ```

## Overview

- **Programming Language:** Python
- **ROS2 Distribution:** Humble
- **User Interface:** A simple Tkinter GUI for order placement.
- **Navigation Flow:**
  - Order received: Robot goes from Home to Kitchen.
  - Food ready: Robot moves to the selected Table.
  - Delivery complete: Robot returns Home.
- **Preset Points:**
  - **Home**
  - **Kitchen**
  - **Table1**, **Table2**, **Table3**

This project serves as a basic demonstration of integrating ROS2 navigation with a graphical user interface for interactive robotic applications. Enjoy experimenting with Cafe Bot!
