# KarpPurbhoo-Lean — selected Karp–Purbhoo results in Lean 4

An independent Lean 4 + mathlib repository for **selected results** from
Steven N. Karp and Kevin Purbhoo,
*Universal Plücker coordinates for the Wronski map and positivity in real Schubert calculus*.

**Journal:** *Journal of the American Mathematical Society* (in press),
[DOI: 10.1090/jams/1087](https://doi.org/10.1090/jams/1087).
**Preprint:** [arXiv:2309.04645](https://arxiv.org/abs/2309.04645),
[version 2, 16 June 2026](https://arxiv.org/abs/2309.04645v2).
These are the journal and preprint references for the same paper.

This repository extracts the Karp–Purbhoo results used by
[Smallram](https://github.com/zhangteng2000/Smallram), together with their complete
local proof dependencies. Coverage is limited to the results listed below.
Both publication references are recorded in [CITATION.bib](CITATION.bib).

## Coverage

Numbering follows arXiv version 2. Names below are in the `ModifiedCartan` namespace.

| Paper result | Formalized content | Lean declaration / source |
| --- | --- | --- |
| Proposition 2.9 | Normalized Plücker-coordinate translation with the exact skew-tableau coefficients | [`Paper.lem_plucker_translation`](ModifiedCartan/PluckerTranslation.lean) |
| Theorem 1.3(i) | Pairwise commutativity of the beta operators at arbitrary complex centers | [`kpBeta_commute`](ModifiedCartan/KPBetaCommutation.lean) |
| Theorem 1.3(ii) | Tableau-coefficient translation identity for the beta operators | [`kpBeta_translation`](ModifiedCartan/KPTranslation.lean) |
| Theorem 1.3(iv) | All centers lie in the generated algebra; this equals the independently defined traditional single-column Bethe algebra | [`kpBeta_mem_generated`](ModifiedCartan/KPTranslation.lean), [`kpGeneratedAlgebra_eq_betheAlgebra`](ModifiedCartan/BetheAlgebraIdentification.lean) |
| Theorem 1.3(v) and Corollary 4.15, in the form required by Smallram | Both directions between nonzero common scalar-action subspaces and the prescribed Wronski fibre; eigenvalues equal normalized Plücker coordinates | [`Paper.lem_KP_correspondence_ii`](ModifiedCartan/KPCorrespondenceEigenspaces.lean) |
| Proposition 2.16 | The normalized character operator is the orthogonal projection onto the isotypic component; includes the constructed Specht representation and its tableau dimension | [`Paper.lem_character_projection`](ModifiedCartan/SymmetricCharacterProjection.lean), [`specht_character_projection`](ModifiedCartan/SpechtCharacterProjection.lean) |

The combined interface is [`ModifiedCartan.Paper.lem_KP_correspondence`](ModifiedCartan/KPCorrespondence.lean).
Its parameters are arbitrary complex numbers, including zero and repeated values;
the number of roots is positive. The Schubert shape and ambient dimension have
their explicit compatibility hypotheses. The exact signatures and logical
dependencies are printed by [verification/KPResults.lean](verification/KPResults.lean).

**Scope:** this release does not claim the complete group-algebra Plücker relations
of Theorem 1.3(iii), the multiplicity statement in 1.3(vi), scheme-theoretic
isomorphisms, or the paper's full positivity and real Schubert-calculus applications.
The correspondence interface asserts the two existence directions; it does not
assert a bijection on all nonzero scalar-action subspaces.

Proof choices and divergences from the paper are recorded in
[FORMALIZATION_MAP.md](FORMALIZATION_MAP.md).

## Build and verify

Prerequisites: Git, Lean's `elan` toolchain manager, and Python 3 for the verification script.

```sh
git clone https://github.com/zhangteng2000/KarpPurbhoo-Lean.git
cd KarpPurbhoo-Lean
lake exe cache get
lake build
python3 scripts/verify.py
```

On Windows, use `python scripts/verify.py` if Python is installed as `python`.
For use in a Lean file, write `import KarpPurbhoo`.

The verifier rebuilds the project, checks the complete extracted import closure and
source hashes, scans project Lean files for prohibited proof placeholders, recursively
audits all imported project declarations (including private declarations), and runs
`#check` and `#print axioms` for the listed results. Its logs are written to
`verification/current/`; the initial verified release record is kept in
[verification/logs](verification/logs).

**No user-declared mathematical axioms or proof placeholders.** The only allowed
foundational logical dependencies are `Classical.choice`, `propext`, and `Quot.sound`.
A literature citation supplies bibliographic context, never a proof assumption.

Lean: `v4.34.0-rc1`.
mathlib: `de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11`.
The exact dependency commits are pinned in `lake-manifest.json`.

## Verification record

The initial release passed **4394 build jobs** and a recursive audit of
**4108 declarations**, including **3423 theorem declarations**. These counts
include supporting mathematics; the KP coverage is exactly the table above.
All ten explicitly checked entry points report only `Classical.choice`,
`propext`, and `Quot.sound`. The source scan found no prohibited placeholders.

The local build reused source-matched verified artifacts and the pinned mathlib
cache. All source files needed to rebuild the project are included. Frozen
evidence: [verification log](verification/logs/initial-verification.log),
[full build log](verification/logs/initial-build.log),
[declaration audit](verification/logs/initial-all-declarations.log), and
[exact theorem signatures and dependencies](verification/logs/initial-kp-results.log).

## Provenance

The 571 supporting source modules were extracted from
[Smallram at e92e331](https://github.com/zhangteng2000/Smallram/tree/e92e33137405545c528c546e4a2e4f9103c63dfb)
without changing their mathematical definitions or proofs. The original Lake package identifier (`Smallram`) and
`ModifiedCartan` and `FewInflection` namespaces and Smallram LaTeX-label comments
are preserved. This repository contains its complete local import closure and
does not require a Smallram checkout. See [PROVENANCE.md](PROVENANCE.md) and the
[source manifest](verification/source-manifest.json).

The originating application is Alexandre Eremenko and Teng Zhang,
*Holomorphic curves of finite lower order with few inflection points*,
[arXiv:2609.38032](https://arxiv.org/abs/2609.38032).
