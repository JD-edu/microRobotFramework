"""
MRF_odometry.py
Python version of the MRF_odometry C++ class for robot odometry calculations
Converted from MRF_odmetry.hpp and MRF_odmetry.cpp (version 04)
Provides position tracking, velocity calculation, and path recording
"""

import math
import time
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Position:
    """Robot position data structure"""
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0  # orientation in radians
    timestamp: float = 0.0

@dataclass
class Velocity:
    """Robot velocity data structure"""
    linear: float = 0.0   # m/s
    angular: float = 0.0  # rad/s
    left_wheel: float = 0.0   # left wheel velocity
    right_wheel: float = 0.0  # right wheel velocity

class MRF_Odometry:
    """
    MicroRobotFramework Odometry class for 2-wheel robot position tracking
    Calculates robot position, orientation, and velocity from encoder data
    """

    def __init__(self, wheel_base: float = 0.2, wheel_radius: float = 0.05, 
                 encoder_resolution: int = 1024):
        """
        Constructor

        Args:
            wheel_base (float): Distance between wheels in meters (default: 0.2m)
            wheel_radius (float): Wheel radius in meters (default: 0.05m)
            encoder_resolution (int): Encoder pulses per revolution (default: 1024)
        """
        # Robot physical parameters
        self.wheel_base = wheel_base
        self.wheel_radius = wheel_radius
        self.encoder_resolution = encoder_resolution

        # Current position and orientation
        self.position = Position()
        self.velocity = Velocity()

        # Previous encoder values for delta calculation
        self.prev_encoder_left = 0
        self.prev_encoder_right = 0
        self.prev_timestamp = time.time()

        # Odometry calculation parameters
        self.distance_per_pulse = (2.0 * math.pi * self.wheel_radius) / self.encoder_resolution

        # Path recording
        self.path_history: List[Position] = []
        self.max_path_length = 1000  # Maximum number of positions to store

        # Statistics
        self.total_distance = 0.0
        self.total_rotation = 0.0

        print(f"✅ MRF_Odometry initialized:")
        print(f"   Wheel base: {self.wheel_base}m")
        print(f"   Wheel radius: {self.wheel_radius}m")
        print(f"   Encoder resolution: {self.encoder_resolution} pulses/rev")
        print(f"   Distance per pulse: {self.distance_per_pulse:.6f}m")

    def update_odometry(self, encoder_left: int, encoder_right: int) -> bool:
        """
        Update odometry calculations with new encoder data

        Args:
            encoder_left (int): Left wheel encoder count
            encoder_right (int): Right wheel encoder count

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            current_time = time.time()
            dt = current_time - self.prev_timestamp

            # Skip if time delta is too small to avoid division by zero
            if dt < 0.001:  # Less than 1ms
                return False

            # Calculate encoder deltas
            delta_left = encoder_left - self.prev_encoder_left
            delta_right = encoder_right - self.prev_encoder_right

            # Handle encoder overflow (assuming 16-bit encoders)
            if abs(delta_left) > 32768:
                if delta_left > 0:
                    delta_left -= 65536
                else:
                    delta_left += 65536

            if abs(delta_right) > 32768:
                if delta_right > 0:
                    delta_right -= 65536
                else:
                    delta_right += 65536

            # Calculate distances traveled by each wheel
            distance_left = delta_left * self.distance_per_pulse
            distance_right = delta_right * self.distance_per_pulse

            # Calculate robot motion
            distance_center = (distance_left + distance_right) / 2.0
            delta_theta = (distance_right - distance_left) / self.wheel_base

            # Update position using differential drive kinematics
            if abs(delta_theta) < 1e-6:  # Straight line motion
                delta_x = distance_center * math.cos(self.position.theta)
                delta_y = distance_center * math.sin(self.position.theta)
            else:  # Curved motion
                radius = distance_center / delta_theta
                delta_x = radius * (math.sin(self.position.theta + delta_theta) - math.sin(self.position.theta))
                delta_y = radius * (-math.cos(self.position.theta + delta_theta) + math.cos(self.position.theta))

            # Update position
            self.position.x += delta_x
            self.position.y += delta_y
            self.position.theta += delta_theta
            self.position.timestamp = current_time

            # Normalize theta to [-pi, pi]
            self.position.theta = self._normalize_angle(self.position.theta)

            # Calculate velocities
            self.velocity.linear = distance_center / dt
            self.velocity.angular = delta_theta / dt
            self.velocity.left_wheel = distance_left / dt
            self.velocity.right_wheel = distance_right / dt

            # Update statistics
            self.total_distance += abs(distance_center)
            self.total_rotation += abs(delta_theta)

            # Record path
            self._record_position()

            # Update previous values
            self.prev_encoder_left = encoder_left
            self.prev_encoder_right = encoder_right
            self.prev_timestamp = current_time

            return True

        except Exception as e:
            print(f"Error updating odometry: {e}")
            return False

    def _normalize_angle(self, angle: float) -> float:
        """
        Normalize angle to [-pi, pi] range

        Args:
            angle (float): Angle in radians

        Returns:
            float: Normalized angle
        """
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def _record_position(self) -> None:
        """Record current position in path history"""
        # Create a copy of current position
        pos_copy = Position(
            x=self.position.x,
            y=self.position.y,
            theta=self.position.theta,
            timestamp=self.position.timestamp
        )

        self.path_history.append(pos_copy)

        # Limit path history size
        if len(self.path_history) > self.max_path_length:
            self.path_history.pop(0)

    def get_position(self) -> Position:
        """Get current robot position"""
        return self.position

    def get_velocity(self) -> Velocity:
        """Get current robot velocity"""
        return self.velocity

    def get_pose(self) -> Tuple[float, float, float]:
        """
        Get current robot pose as tuple

        Returns:
            Tuple[float, float, float]: (x, y, theta)
        """
        return (self.position.x, self.position.y, self.position.theta)

    def get_position_dict(self) -> Dict:
        """Get current position as dictionary"""
        return {
            'x': self.position.x,
            'y': self.position.y,
            'theta': self.position.theta,
            'theta_degrees': math.degrees(self.position.theta),
            'timestamp': self.position.timestamp
        }

    def get_velocity_dict(self) -> Dict:
        """Get current velocity as dictionary"""
        return {
            'linear': self.velocity.linear,
            'angular': self.velocity.angular,
            'angular_degrees': math.degrees(self.velocity.angular),
            'left_wheel': self.velocity.left_wheel,
            'right_wheel': self.velocity.right_wheel
        }

    def get_path_history(self) -> List[Position]:
        """Get recorded path history"""
        return self.path_history.copy()

    def get_statistics(self) -> Dict:
        """Get odometry statistics"""
        return {
            'total_distance': self.total_distance,
            'total_rotation': self.total_rotation,
            'total_rotation_degrees': math.degrees(self.total_rotation),
            'path_points': len(self.path_history),
            'current_position': self.get_position_dict(),
            'current_velocity': self.get_velocity_dict()
        }

    def reset_odometry(self) -> None:
        """Reset odometry to origin"""
        self.position = Position()
        self.velocity = Velocity()
        self.path_history.clear()
        self.total_distance = 0.0
        self.total_rotation = 0.0
        self.prev_timestamp = time.time()
        print("🔄 Odometry reset to origin")

    def set_position(self, x: float, y: float, theta: float) -> None:
        """
        Set robot position manually

        Args:
            x (float): X coordinate in meters
            y (float): Y coordinate in meters
            theta (float): Orientation in radians
        """
        self.position.x = x
        self.position.y = y
        self.position.theta = self._normalize_angle(theta)
        self.position.timestamp = time.time()
        print(f"📍 Position set to: ({x:.3f}, {y:.3f}, {math.degrees(theta):.1f}°)")

    def calculate_distance_to_point(self, target_x: float, target_y: float) -> float:
        """
        Calculate distance from current position to target point

        Args:
            target_x (float): Target X coordinate
            target_y (float): Target Y coordinate

        Returns:
            float: Distance in meters
        """
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        return math.sqrt(dx*dx + dy*dy)

    def calculate_angle_to_point(self, target_x: float, target_y: float) -> float:
        """
        Calculate angle from current position to target point

        Args:
            target_x (float): Target X coordinate
            target_y (float): Target Y coordinate

        Returns:
            float: Angle in radians
        """
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        return math.atan2(dy, dx)

    def get_path_length(self) -> float:
        """
        Calculate total path length from recorded history

        Returns:
            float: Path length in meters
        """
        if len(self.path_history) < 2:
            return 0.0

        total_length = 0.0
        for i in range(1, len(self.path_history)):
            prev_pos = self.path_history[i-1]
            curr_pos = self.path_history[i]

            dx = curr_pos.x - prev_pos.x
            dy = curr_pos.y - prev_pos.y
            total_length += math.sqrt(dx*dx + dy*dy)

        return total_length

    def export_path_to_dict(self) -> List[Dict]:
        """
        Export path history as list of dictionaries

        Returns:
            List[Dict]: Path data
        """
        return [
            {
                'x': pos.x,
                'y': pos.y,
                'theta': pos.theta,
                'theta_degrees': math.degrees(pos.theta),
                'timestamp': pos.timestamp
            }
            for pos in self.path_history
        ]

    def __str__(self) -> str:
        """String representation of odometry state"""
        return (f"MRF_Odometry: "
                f"Pos=({self.position.x:.3f}, {self.position.y:.3f}, "
                f"{math.degrees(self.position.theta):.1f}°), "
                f"Vel=({self.velocity.linear:.3f}m/s, "
                f"{math.degrees(self.velocity.angular):.1f}°/s)")
