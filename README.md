# Quantum Computing and Cryptography

Ideas on Quantum Computing, Cryptography and Communication Algorithms.

Powered by Google Cirq and Python.

![image](https://github.com/user-attachments/assets/d9feaed5-cd4c-4725-8c11-1f7a60b5dbcc)

## Is Faster-than-Light Quantum Communication Possible?

According to bibliography Quantum Communication is impossible with information rate larger than a classical channel: *Quantum Information, Computation and cryptography, Benatti, Fannes, Floreanini, Petritis: pp 210 - theorem HSV and Lemma 1*

- Our protocols prepare 1000 entangled qubit pairs that are separated and sent to 2 locations (L1 and L2).
- We want to sent two classical bits `b1` and `b2` from L1 to L2.
- But we send only another bit `b3` using the quantum protocol for location L1.
- Can the operator of the quantum protocol for location L2 decode the original two bits `b1` and `b2`?
- You can repeat this protocol to estimate the success rate...

1. Failed Attemp #1: What is the best threshold? <img width="995" alt="image" src="https://github.com/user-attachments/assets/6ee7069b-2e97-4e61-a83e-313a396baa29">

1. Failed Attemp #2
```bash
Number of runs: 1000
Success rate: 0.2440
Error rate: 0.7560
```
1. Failed Attempt #3
```
Number of runs: 1000
Overall success rate: 0.5230
Success rate for b1: 0.5240
Success rate for b2: 0.5300
Overall error rate: 0.4770
```
