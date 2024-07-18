import cirq
import numpy as np

## Quantum Communication is Theoretically Impossible, this is failed attempt #2

def encode_bits(b1, b2):
    return b1 * 2 + b2

def angle_to_bits(angle):
    angles = [0, np.pi/8, np.pi/4, 3*np.pi/8]  # 0°, 22.5°, 45°, 67.5°
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

def L1_protocol(b1, b2, num_qubits=1000):
    bases = [0, np.pi/8, np.pi/4, 3*np.pi/8]  # 0°, 22.5°, 45°, 67.5°
    angle = bases[encode_bits(b1, b2)]
    ratio = prepare_and_measure(num_qubits, angle)
    #threshold = 0.7071  # cos^2(22.5°), midway between 0° and 45°
    threshold = np.cos(np.deg2rad(22.5))**2
    return num_qubits, int(ratio > threshold)

def L2_protocol(num_qubits, threshold_bit, threshold=0.8536): # 0.8536 # old 0.7071
    bases = [0, np.pi/8, np.pi/4, 3*np.pi/8]  # 0°, 22.5°, 45°, 67.5°
    results = []
    threshold = np.cos(np.deg2rad(22.5))**2
    for angle in bases:
        ratio = prepare_and_measure(num_qubits // 4, angle)
        results.append(abs(int(ratio > threshold) - threshold_bit))
    
    inferred_angle = bases[np.argmin(results)]
    return angle_to_bits(inferred_angle)

def run_simulation(num_runs=10000):
    correct_count = 0
    for run in range(num_runs):
        if run % 10 == 0:
            print(f"Run {run + 1}/{num_runs}")
        b1, b2 = np.random.randint(0, 2), np.random.randint(0, 2)
        num_qubits, threshold_bit = L1_protocol(b1, b2)
        inferred_b1, inferred_b2 = L2_protocol(num_qubits, threshold_bit)
        if (b1, b2) == (inferred_b1, inferred_b2):
            correct_count += 1
    
    success_rate = correct_count / num_runs
    error_rate = 1 - success_rate
    return success_rate, error_rate

# Run the simulation
num_runs = 1000
success_rate, error_rate = run_simulation(num_runs)
print(f"Number of runs: {num_runs}")
print(f"Success rate: {success_rate:.4f}")
print(f"Error rate: {error_rate:.4f}")
