import numpy as np
import matplotlib.pyplot as plt

#config
dt = 0.001
duration = 10.0
N = int(duration / dt) #10000 samples
np.random.seed(621)
alpha = 0.98

#gyro parameters
bias = 2.0
rw_sigma = 0.005
gyro_noise_sigma = 0.1

#accel parameters
accel_noise_sigma = 1.0
vib_sigma = 3.0
vib_start = 8.0
vib_end = 8.5


#truth
def generate_truth(duration, dt):
    N = int(duration / dt)
    t = np.linspace(0.0, duration, N)
    
    true_rate = np.zeros(N)
    # Phase 1 (0-2s): stationary
    
    true_rate[(t >= 2.0) & (t < 5.0)] = 10.0
    # Phase 2 (2-5s): ramp
    
    # Phase 3 (5-8s): stationary
    
    true_rate[(t >= 8.0) & (t < 8.5)] = -150.0
    # Phase 4 (8-8.5s): flip
    
    # Phase 5 (8.5-10s): stationary
    
    true_angle = np.cumsum(true_rate) * dt
    
    return t, true_rate, true_angle


#sensors
def simulate_gyro(true_rate, bias, rw_sigma, noise_sigma):
    N = len(true_rate)
    white_noise = np.random.normal(0.0, noise_sigma, N)
    rw_steps = np.random.normal(0.0, rw_sigma, N)
    drift = np.cumsum(rw_steps)
    gyro_measured = true_rate + bias + drift + white_noise
    return gyro_measured


def simulate_accel(true_angle, t, noise_sigma, vib_start, vib_end, vib_sigma):
    N = len(true_angle)
    white_noise = np.random.normal(0.0, noise_sigma, N)
    vibration_noise = np.random.normal(0.0, vib_sigma, N)
    mask = (t >= vib_start) & (t < vib_end)
    vibration_noise = vibration_noise * mask
    accel_angle_measured = white_noise + vibration_noise + true_angle
    return accel_angle_measured


# === Estimators ===
def estimate_gyro_only(gyro_measured, dt):
    angle_gyro = np.cumsum(gyro_measured) * dt
    return angle_gyro


def estimate_accel_only(accel_angle_measured):
    angle_accel = accel_angle_measured
    return angle_accel


def complementary_filter(gyro_measured, accel_angle_measured, dt, alpha):
    N = len(gyro_measured)
    angle = np.zeros(N)
    angle[0] = accel_angle_measured[0]
    for i in range(1, N):
        angle[i] = alpha * (angle[i-1] + gyro_measured[i] * dt) + (1 - alpha) * accel_angle_measured[i]
    return angle


#plotting
def plot_results(t, true_angle, angle_gyro, angle_accel, angle_fused):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    #top-left: truth alone
    axes[0, 0].plot(t, true_angle)
    axes[0, 0].set_title("True angle")
    axes[0, 0].set_xlabel("Time (s)")
    axes[0, 0].set_ylabel("Angle (deg)")
    axes[0, 0].grid(True)
    
    #top-right: gyro-only vs truth (drifts)
    axes[0, 1].plot(t, true_angle, label="true angle")
    axes[0, 1].plot(t, angle_gyro, label="gyro-only", alpha=0.7)
    axes[0, 1].set_title("Gyro-only (drifts)")
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("Angle (deg)")
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    #bottom-left: accel-only vs truth (noisy)
    axes[1, 0].plot(t, true_angle, label="true angle")
    axes[1, 0].plot(t, angle_accel, label="accel-only", alpha=0.5)
    axes[1, 0].set_title("Accel-only (noisy)")
    axes[1, 0].set_xlabel("Time (s)")
    axes[1, 0].set_ylabel("Angle (deg)")
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    #bottom-right: fused vs truth (the goal)
    axes[1, 1].plot(t, true_angle, label="true angle", linewidth=2)
    axes[1, 1].plot(t, angle_fused, label="fused", linewidth=2)
    axes[1, 1].set_title("Complementary filter (the goal)")
    axes[1, 1].set_xlabel("Time (s)")
    axes[1, 1].set_ylabel("Angle (deg)")
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.show()


#main 
t, true_rate, true_angle = generate_truth(duration, dt)
gyro_measured = simulate_gyro(true_rate, bias, rw_sigma, gyro_noise_sigma)
accel_angle_measured = simulate_accel(true_angle, t, accel_noise_sigma, vib_start, vib_end, vib_sigma)

angle_gyro = estimate_gyro_only(gyro_measured, dt)
angle_accel = estimate_accel_only(accel_angle_measured)
angle_fused = complementary_filter(gyro_measured, accel_angle_measured, dt, alpha)

plot_results(t, true_angle, angle_gyro, angle_accel, angle_fused)