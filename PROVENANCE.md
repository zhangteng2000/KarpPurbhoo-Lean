# Source provenance

- Upstream: https://github.com/zhangteng2000/Smallram
- Exact source commit: `e92e33137405545c528c546e4a2e4f9103c63dfb`.
- Selected roots: `ModifiedCartan.KPCorrespondence`, `ModifiedCartan.PluckerTranslation`, `ModifiedCartan.SpechtCharacterProjection`.
- Complete local transitive import closure: **571 modules**
  (**558** under `ModifiedCartan`, **13** under `FewInflection`).
- The extracted `.lean` source bytes are the original Git blobs, unchanged.
- [source-manifest.json](verification/source-manifest.json) records each source
  path, SHA256 and direct imports; the verifier checks it.

New repository-specific files are the package configuration, aggregate imports,
documentation, bibliography, verification entry points and verification script.
The reusable namespaces remain unchanged so the exact original declarations can
be found and compared. The historical Smallram label comments identify their
original application; the README maps them to KP's arXiv v2 theorem numbers.

The package has no path dependency on Smallram. Its only direct external Lake
dependency is mathlib, with all dependency commits recorded in the manifest.
Generated `.lake` files, local caches and scratch files are excluded from Git.

The authors of the cited mathematical paper are Steven N. Karp and Kevin Purbhoo.
That bibliographic attribution does not imply their authorship or endorsement of
this Lean repository.

The internal Lake package identifier remains `Smallram` to preserve compatibility
with the extracted modules and their existing verified build artifacts. The
repository and public aggregate import are `KarpPurbhoo-Lean` and `KarpPurbhoo`,
respectively. The initial local verification reused source-matched project
artifacts and the pinned mathlib cache, then reran the independent package build
and complete declaration audit. These caches are not distributed or required.
