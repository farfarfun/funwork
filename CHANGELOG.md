# Changelog

## [Unreleased] - 2026-08-28

### Changed

- **Breaking:** renamed the package from `notework` to `funwork` to match the
  GitHub repository name. The import name and the PyPI distribution name both change:
  - `import notework` -> `import funwork`
  - `pip install notework` -> `pip install funwork`
- The old `notework` PyPI package will receive one final release that forwards to
  `funwork` (manual follow-up by the repo owner, not part of this change). Note that
  `notework` was never actually published to PyPI, so this forwarding release does not
  apply in practice; see README for the unrelated pre-existing `funwork` 0.0.1 placeholder
  package on PyPI.
