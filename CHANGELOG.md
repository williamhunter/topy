# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add `pytest` module that tests all examples in the `examples/` directory.
- Add GitHub action to trigger `pytest` on pull request and push to `master`.
- Add GitHub action to upload package to PyPI on release.
- Add `conda.yml` to quickly install `ToPy` dependencies.
### Fixed
- Use `'Agg'` backend in matplotlib if no display was detected.
### Refactored
- Use `setuptools` instead of `distutils` for setup.
- Use `python3` compatible code in various functions.
- Rename `CHANGES.md` to `CHANGELOG.md`.

## [v0.3.2]
### Added
- Speed improvements, some refactoring, new functionality -
by Ivan Sosnovik

## [v0.2.3]
### Added
- Added create_2d_msh function to visualisation.py, see 2D problems
Tutorial 1 for an explanation of how it is used.

## [v0.2.2]
### Refactored
- Cleaned up by moving ToPy source code files to their own directory
- Added a docs folder and added master's dissertation to it
- Deleted a few files that weren't needed (such as MS sln file)
- Fixed a few typos in READMEs and INSTALL

## [v0.2.1]
### Refactored
- Moved ToPy from Google Code to GitHub.
- Updated files, moved a few things around, renamed/deleted a few, etc.
No changes to the core.

## [v0.1.1]
### Fixed
- SymPy related: All *_K.py files in data directory, corrected
TypeError: 'Symbol' object is not iterable
