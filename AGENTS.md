# Karp–Purbhoo extraction

Keep the README coverage statement precise. This repository contains selected
results, not a certification of the entire KP paper.

Do not introduce user-declared mathematical axioms, proof placeholders, an
external-assumptions layer, or stronger hypotheses in place of missing proofs.
Every result must be proved here or in the pinned Lean/mathlib dependencies.
Inspect exact APIs before use. Record alternative proofs in FORMALIZATION_MAP.md.
Keep the existing declaration names and their original Smallram label comments.

After each integrated change run `lake build` and `python3 scripts/verify.py`.
Keep the recursive audit, including private declarations. Only `Classical.choice`,
`propext`, and `Quot.sound` are permitted foundational logical dependencies.
If changing an extracted source module, document the change and update its source
manifest entry explicitly; never silently present edited code as an original blob.
