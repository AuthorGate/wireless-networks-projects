
import numpy as np
import matplotlib.pyplot as plt

# VANET simplified simulation parameters
ROAD_LENGTH = 1000       # meters
COMM_RANGE = 250         # meters
PACKETS_PER_VEHICLE = 100
VEHICLE_COUNTS = [10, 20, 30, 40, 50]
RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)

pdr_results = []
delay_results = []

for num_vehicles in VEHICLE_COUNTS:
    delivered = 0
    sent = 0
    delays = []

    # Random vehicle positions on a one-dimensional road
    positions = rng.uniform(0, ROAD_LENGTH, num_vehicles)

    for sender in range(num_vehicles):
        for _ in range(PACKETS_PER_VEHICLE):
            # Choose another vehicle as receiver
            receiver = rng.integers(0, num_vehicles - 1)
            if receiver >= sender:
                receiver += 1

            sent += 1
            distance = abs(positions[sender] - positions[receiver])

            # Simplified probability model
            if distance <= COMM_RANGE:
                distance_factor = distance / COMM_RANGE
                congestion_factor = (num_vehicles - 1) / 50

                success_probability = (
                    0.98
                    - 0.20 * distance_factor
                    - 0.35 * congestion_factor
                )
                success_probability = np.clip(
                    success_probability, 0.05, 1.0
                )

                if rng.random() < success_probability:
                    delivered += 1

                    delay_ms = (
                        5
                        + 0.03 * distance
                        + 0.5 * num_vehicles
                        + rng.uniform(0, 5)
                    )
                    delays.append(delay_ms)

    pdr = 100 * delivered / sent
    avg_delay = np.mean(delays) if delays else 0

    pdr_results.append(pdr)
    delay_results.append(avg_delay)

    print(
        f"Vehicles: {num_vehicles}, "
        f"PDR: {pdr:.2f}%, "
        f"Delay: {avg_delay:.2f} ms"
    )

# Graph 1: Packet Delivery Ratio
plt.figure(figsize=(8, 5))
plt.plot(
    VEHICLE_COUNTS, pdr_results,
    marker="o", linewidth=2
)
plt.xlabel("Number of Vehicles")
plt.ylabel("Packet Delivery Ratio (%)")
plt.title("VANET Packet Delivery Ratio vs Vehicle Density")
plt.grid(True)
plt.tight_layout()
plt.savefig("vanet_pdr.png", dpi=300)
plt.close()

# Graph 2: Average End-to-End Delay
plt.figure(figsize=(8, 5))
plt.plot(
    VEHICLE_COUNTS, delay_results,
    marker="s", linewidth=2
)
plt.xlabel("Number of Vehicles")
plt.ylabel("Average Delay (ms)")
plt.title("VANET Average Delay vs Vehicle Density")
plt.grid(True)
plt.tight_layout()
plt.savefig("vanet_delay.png", dpi=300)
plt.close()

print("\nSimulation completed successfully!")
print("Generated: vanet_pdr.png and vanet_delay.png")
