# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2021-02-16
### Added
- `Python 3.8` is now supported.
- `Python 3.9` is now supported.

### Changed
- The package layout is not flat anymore.  Replace `import bencode` with
  `from clot import bencode` in your code to accommodate this change.

### Removed
- `Python 3.5` is no longer supported.

### Fixed
- `python path/setup.py install` no longer throws an exception trying to
  locate the package's `__init__.py` file.

## [1.0.0] - 2019-02-23
### Added
- Python 3.7 is now supported.

### Changed
- ValueError raised by decode(bytes) now has 2 arguments.

  The first one is an error message as usual. The second one is an
  offset in the original bytes where the error happened.

### Removed
- `Python 3.4` is no longer supported.

## [0.1.0] - 2017-07-30
- Initial release.

[Unreleased]: https://github.com/elliptical/clot/compare/2.0.0...HEAD
[2.0.0]: https://github.com/elliptical/clot/compare/1.0.0...2.0.0
[1.0.0]: https://github.com/elliptical/clot/compare/0.1.0...1.0.0
[0.1.0]: https://github.com/elliptical/clot/releases/tag/0.1.0
