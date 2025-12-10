Try to crack these circuits in .qasm2 format - they grow in difficulty and points 📈

Crack = find the peak bitstring that has the max amplitude and stands out from the rest of amplitudes! 

To submit the peak bitstring use the submission tab 👆
About bit-order: We are using little endian convention, e.g. qubit-0 is the rightmost bit in the final bitstring (like in qiskit convention). But you don’t have to worry about it - we will count both the peak bitstring and its reverse as correct. In case you got the order wrong - you will see that info as a warning in the submission result.
You can use the below script to load .qasm2 files in qiskit 👇

```
from qiskit import QuantumCircuit

qc = QuantumCircuit.from_qasm_file('P1.qasm')
```

Link to the BlueQubit's Hackathon: https://app.bluequbit.io/hackathons/GFgHTGbTylwmMsCp?tab=problems
