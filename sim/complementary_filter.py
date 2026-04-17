import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
duration = 10.0
N = int(duration / dt) #10000 samples

alpha = 0.98

def generate_truth(duration, dt):
    N = int(duration / dt)
    t = np.linspace(0.0, duration, N)
    
    true_rate = np.zeros(N)
    # Phase 1 (0-2s): stationary
    
    true_rate[(t >= 2.0) & (t <= 5.0)] = 10.0
    # Phase 2 (2-5s): ramp
    
    true_rate[(t > 5.0 ) & (t  <= 8.0)] = 0.0
    # Phase 3 (5-8s): stationary
    
    true_rate[(t > 8.0) & (t <= 8.5)] = -150.0
    # Phase 4 (8-8.5s): flip
    
    true_rate[(t > 8.5) & (t <= 10.0)] = 0
    # Phase 5 (8.5-10s): stationary
    
    true_angle = np.cumsum(true_rate) * dt
    
    return t, true_rate, true_angle

t, true_rate, true_angle = generate_truth(duration, dt)
plt.plot (t, true_angle)
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.grid(True)
plt.show()