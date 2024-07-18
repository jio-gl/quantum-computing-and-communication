import cirq
import numpy as np
import random

random.seed(777)

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

def L1_protocol(bit, num_qubits=1000):
    bases = [0, np.pi/4]  # 0°, 45°
    angle = bases[bit]
    ratio = prepare_and_measure(num_qubits, angle)
    threshold = 0.75  # Midpoint between cos²(0°) and cos²(45°)
    return num_qubits, int(ratio > threshold)

def L2_protocol(num_qubits, threshold_bit):
    bases = [0, np.pi/4]  # 0°, 45°
    results = []
    threshold = 0.75
    for angle in bases:
        ratio = prepare_and_measure(num_qubits // 2, angle)
        results.append(abs(int(ratio > threshold) - threshold_bit))
    
    inferred_angle = bases[np.argmin(results)]
    return 0 if inferred_angle == 0 else 1

def run_simulation(num_runs=10000):
    correct_count = 0
    for run in range(num_runs):
        if run % 10 == 0:
            print(f"Run {run + 1}/{num_runs}")
        bit = np.random.randint(0, 2)
        num_qubits, threshold_bit = L1_protocol(bit)
        inferred_bit = L2_protocol(num_qubits, threshold_bit)
        if bit == inferred_bit:
            correct_count += 1
    
    success_rate = correct_count / num_runs
    error_rate = 1 - success_rate
    return success_rate, error_rate

# Run the simulation
num_runs = 200
success_rate, error_rate = run_simulation(num_runs)
print(f"Number of runs: {num_runs}")
print(f"Success rate: {success_rate:.4f}")
print(f"Error rate: {error_rate:.4f}")
