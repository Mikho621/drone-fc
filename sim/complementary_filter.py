import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
duration = 10.0
N = int(duration / dt) #10000 samples
np.random.seed(621)
alpha = 0.98

# Gyro model parameters
bias = 2.0
rw_sigma = 0.005
gyro_noise_sigma = 0.1

# Accel model parameters
accel_noise_sigma = 1.0
vib_sigma = 3.0
vib_start = 8.0
vib_end = 8.5

def generate_truth(duration, dt):
    N = int(duration / dt)
    t = np.linspace(0.0, duration, N)
    
    true_rate = np.zeros(N)
    # Phase 1 (0-2s): stationary — implicit zero
    
    true_rate[(t >= 2.0) & (t < 5.0)] = 10.0
    # Phase 2 (2-5s): ramp
    
    # Phase 3 (5-8s): stationary — implicit zero
    
    true_rate[(t >= 8.0) & (t < 8.5)] = -150.0
    # Phase 4 (8-8.5s): flip
    
    # Phase 5 (8.5-10s): stationary — implicit zero
    
    true_angle = np.cumsum(true_rate) * dt
    
    return t, true_rate, true_angle

t, true_rate, true_angle = generate_truth(duration, dt)

plt.plot(t, true_angle)
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.grid(True)
plt.show()

def simulate_gyro(true_rate, bias, rw_sigma, noise_sigma):
    N = len(true_rate)
    white_noise = np.random.normal(0.0, noise_sigma, N)
    rw_steps = np.random.normal(0.0, rw_sigma, N)
    drift = np.cumsum(rw_steps)
    gyro_measured = true_rate + bias + drift + white_noise
    return gyro_measured

gyro_measured = simulate_gyro(true_rate, bias, rw_sigma, gyro_noise_sigma)

plt.figure()
plt.plot(t, true_rate, label="true rate")
plt.plot(t, gyro_measured, label="measured gyro", alpha=0.6)
plt.xlabel("Time (s)")
plt.ylabel("Rate (deg/s)")
plt.legend()
plt.grid(True)
plt.show()

def simulate_accel(true_angle, t, noise_sigma, vib_start, vib_end, vib_sigma):
    N = len(true_angle)
    white_noise = np.random.normal(0.0, noise_sigma, N)
    vibration_noise = np.random.normal(0.0, vib_sigma, N)
    mask = (t >= vib_start) & (t < vib_end)
    vibration_noise = vibration_noise * mask
    accel_angle_measured = white_noise + vibration_noise + true_angle
    return accel_angle_measured

accel_angle_measured = simulate_accel(true_angle, t, accel_noise_sigma, vib_start, vib_end, vib_sigma)

plt.figure()
plt.plot(t, true_angle, label="true angle")
plt.plot(t, accel_angle_measured, label="measured accel", alpha=0.6)
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.legend()
plt.grid(True)
plt.show()

def estimate_gyro_only(gyro_measured, dt):
    angle_gyro = np.cumsum(gyro_measured) * dt
    return angle_gyro

angle_gyro = estimate_gyro_only(gyro_measured, dt)

plt.figure()
plt.plot(t, true_angle, label='True angle')
plt.plot(t, angle_gyro, label='Gyro-only estimate')
plt.xlabel('Time (s)')
plt.ylabel('Angle (deg)')
plt.title('Gyro-only integration vs truth')
plt.legend()
plt.grid(True)
plt.show()

def estimate_accel_only(accel_angle_measured):
    angle_accel = accel_angle_measured
    return angle_accel

angle_accel = estimate_accel_only(accel_angle_measured)

plt.figure()
plt.plot(t, true_angle, label='True angle')
plt.plot(t, angle_accel, label='Accel-only estimate', alpha=0.6)
plt.xlabel('Time (s)')
plt.ylabel('Angle (deg)')
plt.title('Accel-only vs truth')
plt.legend()
plt.grid(True)
plt.show()