import cirq
import numpy as np

# Quantum Communication is Impossible, this is Attempt #1

def encode_bits(b1, b2):
    return b1 * 2 + b2

def angle_to_bits(angle): # 4 bases
    angles = [0, np.pi/12, np.pi/6, np.pi/4]
    index = np.argmin([abs(angle - a) for a in angles])
    return index // 2, (index) % 2

def prepare_and_measure(num_qubits, angle):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Create superposition
    circuit.append(cirq.H(q) for q in qubits)
    
    # Rotate to measurement basis
    circuit.append(cirq.ry(2 * angle).on(q) for q in qubits)
    
    # Measure
    circuit.append(cirq.measure(*qubits, key='m'))
    
    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    # Count '0's
    measurement = result.measurements['m'][0]
    passes = np.count_nonzero(measurement == 0)
    return passes / num_qubits

def run_simulation(num_runs, threshold):
    correct_count = 0
    for run in range(num_runs):
        if run % 10 == 0:
            print(f"Run {run + 1}/{num_runs}")
        b1, b2 = np.random.randint(0, 2), np.random.randint(0, 2)
        num_qubits, threshold_bit = L1_protocol(b1, b2, threshold=threshold)
        inferred_b1, inferred_b2 = L2_protocol(num_qubits, threshold_bit, threshold=threshold)
        if (b1, b2) == (inferred_b1, inferred_b2):
            correct_count += 1
    
    success_rate = correct_count / num_runs
    return success_rate

# Protocol for Location 1
def L1_protocol(b1, b2, num_qubits=1000, threshold=0.8536):
    bases = [0, np.pi/12, np.pi/6, np.pi/4]
    angle = bases[encode_bits(b1, b2)]
    ratio = prepare_and_measure(num_qubits, angle)
    return num_qubits, int(ratio > threshold)

# Protocol for Location 2
def L2_protocol(num_qubits, threshold_bit, threshold=0.8536):
    bases = [0, np.pi/12, np.pi/6, np.pi/4]
    results = []
    for angle in bases:
        ratio = prepare_and_measure(num_qubits // 4, angle)
        results.append(abs(int(ratio > threshold) - threshold_bit))
    
    inferred_angle = bases[np.argmin(results)]
    return angle_to_bits(inferred_angle)

# Test different thresholds
num_runs = 100
thresholds = np.linspace(0.82, 0.88, 31)  # Test 31 thresholds between 0.82 and 0.88

results = []
for threshold in thresholds:
    success_rate = run_simulation(num_runs, threshold)
    results.append((threshold, success_rate))
    print(f"Threshold: {threshold:.4f}, Success rate: {success_rate:.4f}")

# Find the best threshold
best_threshold, best_success_rate = max(results, key=lambda x: x[1])
print(f"\nBest threshold: {best_threshold:.4f}")
print(f"Best success rate: {best_success_rate:.4f}")

# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot([r[0] for r in results], [r[1] for r in results], 'b-')
plt.scatter([best_threshold], [best_success_rate], color='red', s=100, zorder=5)
plt.xlabel('Threshold')
plt.ylabel('Success Rate')
plt.title('Success Rate vs Threshold')
plt.grid(True)
plt.show()
