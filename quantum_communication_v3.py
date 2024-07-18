import cirq
import numpy as np
import random

random.seed(777)

def encode_bits(b1, b2):
    return b1 * 2 + b2

def angle_to_bits(angle):
    angles = [0, np.pi/6, np.pi/3, np.pi/2]  # 0°, 30°, 60°, 90°
    index = np.argmin([abs(angle - a) for a in angles])
    return index // 2, index % 2

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

# Protocol for Location 1
def L1_protocol(b1, b2, num_qubits=1000):
    bases = [0, np.pi/6, np.pi/3, np.pi/2]  # 0°, 30°, 60°, 90°
    angle = bases[encode_bits(b1, b2)]
    ratio = prepare_and_measure(num_qubits, angle)
    threshold = np.sqrt(0.75 * 0.25)  # Approximately 0.4330
    #threshold = np.cos(np.deg2rad(60))**2
    return num_qubits, int(ratio > threshold)

# Protocol for Location 2
def L2_protocol(num_qubits, threshold_bit):
    bases = [0, np.pi/6, np.pi/3, np.pi/2]  # 0°, 30°, 60°, 90°
    results = []
    threshold = np.sqrt(0.75 * 0.25)  # Approximately 0.4330
    #threshold = np.cos(np.deg2rad(60))**2
    for angle in bases:
        ratio = prepare_and_measure(num_qubits // 4, angle)
        results.append(abs(int(ratio > threshold) - threshold_bit))
    
    inferred_angle = bases[np.argmin(results)]
    return angle_to_bits(inferred_angle)

def run_simulation(num_runs=10000):
    correct_count = 0
    correct_count_b1 = 0
    correct_count_b2 = 0
    for run in range(num_runs):
        if run % 10 == 0:
            print(f"Run {run + 1}/{num_runs}")
        b1, b2 = np.random.randint(0, 2), np.random.randint(0, 2)
        num_qubits, threshold_bit = L1_protocol(b1, b2)
        inferred_b1, inferred_b2 = L2_protocol(num_qubits, threshold_bit)
        if b1 == inferred_b1:
            correct_count_b1 += 1
        if b2 == inferred_b2:
            correct_count_b2 += 1
        if (b1, b2) == (inferred_b1, inferred_b2):
            correct_count += 1
    
    success_rate = correct_count / num_runs
    success_rate_b1 = correct_count_b1 / num_runs
    success_rate_b2 = correct_count_b2 / num_runs
    error_rate = 1 - success_rate
    return success_rate, success_rate_b1, success_rate_b2, error_rate

# Run the simulation
num_runs = 1000
success_rate, success_rate_b1, success_rate_b2, error_rate = run_simulation(num_runs)
print(f"Number of runs: {num_runs}")
print(f"Overall success rate: {success_rate:.4f}")
print(f"Success rate for b1: {success_rate_b1:.4f}")
print(f"Success rate for b2: {success_rate_b2:.4f}")
print(f"Overall error rate: {error_rate:.4f}")
