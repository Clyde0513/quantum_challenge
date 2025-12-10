from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Pauli
import numpy as np


def guess_peak_from_mps_expectations(
    qasm_path: str,
    max_bond_dimension: int = 64,
    truncation_threshold: float = 1e-3,
):
    """
    Single approximate MPS simulation (no shots) to estimate ⟨Z_i⟩
    and infer the dominant bitstring.

    Returns
    -------
    bitstring : str
        Guessed peak bitstring in Qiskit's usual measurement order.
    z_expectations : np.ndarray
        Array of ⟨Z_i⟩ values for each qubit index i.
    """
    # Load the circuit
    qc = QuantumCircuit.from_qasm_file(qasm_path)
    n = qc.num_qubits
    print(f"Circuit loaded: {n} qubits")

    # MPS simulator with truncation (approximate)
    sim = AerSimulator(method="matrix_product_state")
    sim.set_options(
        matrix_product_state_max_bond_dimension=max_bond_dimension,
        matrix_product_state_truncation_threshold=truncation_threshold,
    )
    print(
        f"Using approximate MPS: "
        f"max_bond_dimension={max_bond_dimension}, "
        f"truncation_threshold={truncation_threshold}"
    )

    # Add instructions to save ⟨Z_i⟩ for each qubit
    qc_ev = qc.copy()
    for i in range(n):
        qc_ev.save_expectation_value(Pauli("Z"), [i], label=f"Z_{i}")

    # Transpile and run (single deterministic simulation)
    qc_ev_t = transpile(qc_ev, sim, optimization_level=1)
    result = sim.run(qc_ev_t, shots = 4000).result()
    data = result.data(0)

    # Collect ⟨Z_i⟩
    z_expectations = np.array([data[f"Z_{i}"] for i in range(n)])
    print("⟨Z⟩ per qubit (qubit index 0..n-1):")
    print(z_expectations)

    # Convert ⟨Z⟩ → bits: +1→0, -1→1 (in LSB-first convention)
    bits_lsb_first = ["0" if z > 0 else "1" for z in z_expectations]

    # Qiskit measurement strings show qubit 0 as the rightmost bit,
    # so we reverse to get the usual bitstring order.
    bitstring = "".join(reversed(bits_lsb_first))

    print("\nGuessed peak bitstring (Qiskit order):", bitstring)
    print("Reversed (LSB→MSB):", bitstring[::-1])

    # Optional: show confidence per bit
    confidences = np.abs(z_expectations)
    print("\nPer-qubit |⟨Z⟩| (closer to 1 = more confident):")
    print(confidences)

    return bitstring, z_expectations

if __name__ == "__main__":
    qasm_file = "P1_little_dimple.qasm"

    guess, z_vals = guess_peak_from_mps_expectations(
        qasm_path=qasm_file,
        max_bond_dimension=256,   
        truncation_threshold=1e-3,  
    )
    
    print("\nFinal guessed peak bitstring:", guess)
    print("Final ⟨Z⟩ values:", z_vals)
