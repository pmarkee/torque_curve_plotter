import argparse
import matplotlib.pyplot as plt
import json

torque_curve = [
    (1000, 30),
    (1100, 36.7),
    (1200, 43.1),
    (1300, 49.1),
    (1400, 54.8),
    (1500, 60.2),
    (1600, 65.3),
    (1700, 70),
    (1800, 74.4),
    (1900, 78.5),
    (2000, 82.3),
    (2100, 85.7),
    (2200, 88.8),
    (2300, 91.6),
    (2400, 94),
    (2500, 96.1),
    (2600, 97.9),
    (2700, 99.4),
    (2800, 100.5),
    (2900, 101.3),
    (3000, 101.8),
    (3100, 102),
    (3200, 102),
    (3300, 101.9),
    (3400, 101.8),
    (3500, 101.7),
    (3600, 101.5),
    (3700, 101.3),
    (3800, 101.1),
    (3900, 100.8),
    (4000, 100.5),
    (4100, 100.2),
    (4200, 99.8),
    (4300, 99.4),
    (4400, 98.9),
    (4500, 98.4),
    (4600, 97.9),
    (4700, 97.3),
    (4800, 96.7),
    (4900, 96.1),
    (5000, 95.4),
    (5100, 94.7),
    (5200, 94),
    (5300, 93.2),
    (5400, 92.4),
    (5500, 91.5),
    (5600, 90.6),
    (5700, 89.7),
    (5800, 88.7),
    (5900, 87.7),
    (6000, 86.7),
    (6100, 85.6),
    (6200, 84.5),
    (6300, 83.4),
    (6400, 81.7),
    (6500, 79.5),
    (6600, 76.7),
    (6700, 73.4),
    (6800, 69.5),
]


def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot torque and power curves.')
    parser.add_argument('--torque', action='store_true', help='Plot torque curve')
    parser.add_argument('--power', action='store_true', help='Plot power curve')
    parser.add_argument('--output', default='torque_and_power_vs_rpm.png', help='Output file path for the graph (default: torque_and_power_vs_rpm.png)')
    return parser.parse_args()


def model1(no_throttle_tq, full_throttle_tq):
    if len(no_throttle_tq) != len(full_throttle_tq):
        return

    def compute(throttle):
        num_samples = len(no_throttle_tq)
        return [get_inbetween_tq(no_throttle_tq[i], full_throttle_tq[i], throttle)
            for i in range(num_samples)]

    def get_inbetween_tq(lower, upper, throttle):
        return lower + (upper - lower) * throttle

    return compute


args = parse_arguments()
if not args.torque and not args.power:
    exit(0)

rpm = [data[0] for data in torque_curve]
full_throttle_tq = [data[1] for data in torque_curve]
no_throttle_tq = [-0.003 * r + 2.55 for r in rpm]

throttle_values = [x/10 for x in range(1, 10)]

model = model1(no_throttle_tq, full_throttle_tq)
inbetween_tq = {throttle: model(throttle) for throttle in throttle_values}

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot torque vs RPM
if args.torque:
    ax1.plot(rpm, no_throttle_tq, marker='o', linestyle='-', color='b', label='Torque (Nm)')
    ax1.plot(rpm, full_throttle_tq, marker='o', linestyle='-', color='b', label='Torque (Nm)')

    for tq in inbetween_tq.values():
        ax1.plot(rpm, tq, marker='o', linestyle='-', color='c', label='Torque (Nm)')
    
    ax1.set_ylabel('Torque (Nm)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

# Create a secondary y-axis for power
if args.power:
    # Calculate power in kW
    full_throttle_power = [(torque * rpm) / 9550 for rpm, torque in torque_curve]
    no_throttle_power = [(torque * rpm) / 9550 for rpm, torque in zip(rpm, no_throttle_tq)]

    inbetween_power = {throttle:
        [(torque * rpm) / 9550 for rpm, torque in zip(rpm, inbetween_tq[throttle])]
        for throttle in throttle_values}

    ax2 = ax1.twinx()
    ax2.plot(rpm, no_throttle_power, marker='o', linestyle='-', color='r', label='Power (kW)')
    ax2.plot(rpm, full_throttle_power, marker='o', linestyle='-', color='r', label='Power (kW)')

    for p in inbetween_power.values():
        ax2.plot(rpm, p, marker='o', linestyle='-', color='y', label='Torque (Nm)')

    ax2.set_ylabel('Power (kW)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

ax1.set_xlabel('RPM')
ax1.grid(True)
fig.tight_layout()

# Save the plot to a file
plt.savefig(args.output)
plt.close()

with open('data.json', 'w') as f:
    output = {
        'rpm_values': rpm,
        0.0: no_throttle_tq,
        1.0: full_throttle_tq,
        **inbetween_tq
    }
    json.dump(output, f)
