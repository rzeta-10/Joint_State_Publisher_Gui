#!/usr/bin/env python

import rospy
import tkinter as tk
from sensor_msgs.msg import JointState

class JointStatePublisherGUI:
    def __init__(self):
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        self.initial_joint_positions = [0.0] * len(self.joint_names)
        self.joint_positions = self.initial_joint_positions.copy()
        self.joint_velocities = [0.0] * (len(self.joint_names) - 2)  # Velocity only for joint1 to joint4
        rospy.init_node('joint_state_publisher_gui')

        self.publisher = rospy.Publisher('/joint_states', JointState, queue_size=10)

        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('Joint State Publisher GUI')

        # Add headings
        position_label = tk.Label(self.root, text='Position')
        position_label.grid(row=0, column=1, padx=10, pady=5)

        velocity_label = tk.Label(self.root, text='Velocity')
        velocity_label.grid(row=0, column=2, padx=10, pady=5)

        self.position_scale_vars = [tk.DoubleVar(value=0.0) for _ in range(len(self.joint_names))]
        self.velocity_scale_vars = [tk.DoubleVar(value=0.0) for _ in range(len(self.joint_names) - 2)]

        self.position_scales = []
        self.velocity_scales = []

        for i, joint_name in enumerate(self.joint_names):
            joint_label = tk.Label(self.root, text=joint_name)
            joint_label.grid(row=i + 1, column=0, padx=10, pady=5, sticky=tk.W)

            position_scale = tk.Scale(self.root, from_=-180.0, to=180.0, resolution=0.01, variable=self.position_scale_vars[i], orient=tk.HORIZONTAL)
            position_scale.grid(row=i + 1, column=1, padx=10, pady=5)

            # Create velocity scales only for joint1 to joint4
            if i < len(self.joint_names) - 2:
                velocity_scale = tk.Scale(self.root, from_=-10.0, to=10.0, resolution=0.01, variable=self.velocity_scale_vars[i], orient=tk.HORIZONTAL)
                velocity_scale.grid(row=i + 1, column=2, padx=10, pady=5)
                self.velocity_scales.append(velocity_scale)

            self.position_scales.append(position_scale)

        publish_button = tk.Button(self.root, text='Publish', command=self.publish_joint_states)
        publish_button.grid(row=len(self.joint_names) + 1, column=1, pady=10)

        reset_button = tk.Button(self.root, text='Reset', command=self.reset_joint_states)
        reset_button.grid(row=len(self.joint_names) + 1, column=2, pady=10)

        # Bind keyboard events to update values
        self.root.bind('<Key>', self.update_values)

        self.root.mainloop()

    def publish_joint_states(self):
        for i, position_scale_var in enumerate(self.position_scale_vars):
            self.joint_positions[i] = position_scale_var.get()

        for i, velocity_scale_var in enumerate(self.velocity_scale_vars):
            self.joint_velocities[i] = velocity_scale_var.get()

        joint_state_msg = JointState()
        joint_state_msg.name = self.joint_names
        joint_state_msg.position = self.joint_positions
        joint_state_msg.velocity = self.joint_velocities

        self.publisher.publish(joint_state_msg)
        rospy.loginfo('Joint states published: {}'.format(joint_state_msg))

    def reset_joint_states(self):
        for i in range(len(self.joint_names)):
            self.position_scale_vars[i].set(self.initial_joint_positions[i])
            if i < len(self.joint_names) - 2:
                self.velocity_scale_vars[i].set(0.0)

    def update_values(self, event):
        # Update values using keyboard input
        key = event.char
        if key.isdigit():
            index = int(key) - 1
            if 0 <= index < len(self.joint_names):
                self.position_scales[index].focus_set()
                self.position_scales[index].set(float(event.char))
                # Only set the velocity scale if it exists (joint1 to joint4)
                if index < len(self.joint_names) - 2:
                    self.velocity_scales[index].focus_set()
                    self.velocity_scales[index].set(float(event.char))

if __name__ == '__main__':
    try:
        joint_state_publisher_gui = JointStatePublisherGUI()
    except rospy.ROSInterruptException:
        pass
