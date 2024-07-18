import cirq
import numpy as np
import random

random.seed(777)

# Using a 3-state classical variable to transfer 1 classical bit over the entangled single qubit pair channel.
# Failed attemp, success rate is not big enough.

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
    bases = [0, np.pi/6, np.pi/3]  # 0°, 30°, 60°
    angle = bases[bit * 2]  # Use 0° and 60° for encoding
    ratio = prepare_and_measure(num_qubits, angle)
    
    # Convert ratio to a 3-state variable
    if ratio > np.cos(np.pi/6)**2:
        return 0
    elif ratio > np.cos(np.pi/3)**2:
        return 1
    else:
        return 2

def L2_protocol(state, num_qubits=1000):
    bases = [0, np.pi/6, np.pi/3]  # 0°, 30°, 60°
    results = []
    for angle in bases:
        measured_ratio = prepare_and_measure(num_qubits // 3, angle)
        results.append(measured_ratio)
    
    # Determine the most likely original state
    if state == 0:
        return 1 if results[0] > results[2] else 0
    elif state == 1:
        return 1 if abs(results[1] - results[0]) < abs(results[1] - results[2]) else 0
    else:  # state == 2
        return 0 if results[2] < results[0] else 1

def run_simulation(num_runs=10000):
    correct_count = 0
    for run in range(num_runs):
        if run % 10 == 0:
            print(f"Run {run + 1}/{num_runs}")
        bit = np.random.randint(0, 2)
        state = L1_protocol(bit)
        inferred_bit = L2_protocol(state)
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
