import cirq
import numpy as np
import random

random.seed(777)

def create_bell_pair(qubits):
    """Create a Bell pair using two qubits."""
    circuit = cirq.Circuit()
    circuit.append([
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1])
    ])
    return circuit

def teleport_state(source, alice, bob):
    """Perform quantum teleportation from source to bob via alice."""
    circuit = cirq.Circuit()
    
    # Bell state measurement
    circuit.append([
        cirq.CNOT(source, alice),
        cirq.H(source),
        cirq.measure(source, alice, key='m')
    ])
    
    # Corrections based on measurement
    circuit.append(
        cirq.X(bob).controlled_by(alice),
        cirq.Z(bob).controlled_by(source)
    )
    
    return circuit

def quantum_teleportation(initial_state):
    """Full quantum teleportation protocol."""
    qubits = cirq.LineQubit.range(3)
    source, alice, bob = qubits
    
    circuit = cirq.Circuit()
    
    # Prepare the initial state
    circuit.append(cirq.unitary(initial_state).on(source))
    
    # Create Bell pair between Alice and Bob
    circuit += create_bell_pair([alice, bob])
    
    # Perform teleportation
    circuit += teleport_state(source, alice, bob)
    
    # Measure Bob's qubit
    circuit.append(cirq.measure(bob, key='result'))
    
    return circuit

def run_teleportation(initial_state, num_runs=1000):
    """Run the teleportation protocol multiple times and return statistics."""
    circuit = quantum_teleportation(initial_state)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=num_runs)
    
    # Count how many times we got |0⟩ and |1⟩
    counts = result.histogram(key='result')
    prob_0 = counts[0] / num_runs
    prob_1 = counts[1] / num_runs
    
    return prob_0, prob_1

def main():
    # Define some test states
    states = [
        cirq.unitary(cirq.X**0.25),  # |+⟩ state
        cirq.unitary(cirq.Y**0.25),  # |i⟩ state
        cirq.unitary(cirq.Z**0.25)   # |0⟩ + i|1⟩ state (normalized)
    ]
    
    for i, state in enumerate(states):
        prob_0, prob_1 = run_teleportation(state)
        print(f"State {i+1}:")
        print(f"Probability of measuring |0⟩: {prob_0:.4f}")
        print(f"Probability of measuring |1⟩: {prob_1:.4f}")
        print()

if __name__ == "__main__":
    main()
