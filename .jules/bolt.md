## 2024-06-25 - Halving Iterations in Commutative Property Search
**Learning:** When searching for combination pairs where the operation is commutative (e.g., finding best R1 || R2 parallel resistors), searching all pairs (N^2) calculates redundant symmetric pairings (e.g., R1=1k, R2=2k and R1=2k, R2=1k).
**Action:** Use `enumerate` and slice the inner loop from the current outer loop index (`for i, r1 in enumerate(values): for r2 in values[i:]`) to halve the total iterations and double performance instantly.
