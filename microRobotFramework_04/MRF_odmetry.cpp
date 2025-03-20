#include <iostream>
#include <cmath>
#include <chrono>

class MRF_Odometry {
public:
    MRF_Odometry(double wheel_base, double time_step)
        : x(0.0), y(0.0), theta(0.0), L(wheel_base), dt(time_step) {}

    // Update odometry based on wheel encoder values and IMU orientation
    void updateOdometry(int enc_FL, int enc_FR, int enc_RL, int enc_RR, double imu_yaw) {
        // Convert encoder ticks to velocities
        double v_FL = encoderToVelocity(enc_FL);
        double v_FR = encoderToVelocity(enc_FR);
        double v_RL = encoderToVelocity(enc_RL);
        double v_RR = encoderToVelocity(enc_RR);

        // Compute linear and angular velocity
        double v = (v_FL + v_FR + v_RL + v_RR) / 4.0;
        double omega = ((v_FR + v_RR) - (v_FL + v_RL)) / (2.0 * L);

        // Update position
        x += v * std::cos(theta) * dt;
        y += v * std::sin(theta) * dt;
        theta += omega * dt;

        // Use IMU yaw to correct angle drift
        theta = imu_yaw;

        // Keep theta in range [-π, π]
        theta = std::atan2(std::sin(theta), std::cos(theta));
    }

    // Print current position
    void printOdometry() const {
        std::cout << "X: " << x << "  Y: " << y << "  Theta: " << theta << " rad" << std::endl;
    }

private:
    double x, y, theta; // Robot position (meters) and orientation (radians)
    double L;           // Wheelbase (meters)
    double dt;          // Time step (seconds)

    // Convert encoder ticks to velocity (Example: assume 1000 ticks per meter)
    double encoderToVelocity(int ticks) {
        const double TICKS_PER_METER = 1000.0;
        return ticks / TICKS_PER_METER;
    }
};

int main() {
    MRF_Odometry odom(0.5, 0.1); // Wheelbase = 0.5m, dt = 0.1s

    // Simulated encoder values and IMU yaw (radians)
    int enc_FL = 50, enc_FR = 52, enc_RL = 50, enc_RR = 52;
    double imu_yaw = 0.05; // Example IMU yaw correction

    // Update odometry and print results
    for (int i = 0; i < 10; i++) {
        odom.updateOdometry(enc_FL, enc_FR, enc_RL, enc_RR, imu_yaw);
        odom.printOdometry();
    }

    return 0;
}
