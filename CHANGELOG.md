# Changelog

## [0.2.3][] - 2019-12-11

[0.2.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud/compare/0.2.2...0.2.3

### Deprecated

-   This extension is now deprecated. Please use the
    chaostoolkit-google-cloud-platform extension instead.

## [0.2.2][] - 2018-05-14

[0.2.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud/compare/0.2.1...0.2.2

### Added

-   Read version from source file without importing

## [0.2.1][] - 2018-04-24

[0.2.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud/compare/0.2.0...0.2.1

### Changed

-   Fixed setup.py to read version from package

## [0.2.0][] - 2018-04-23

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud/compare/0.1.0...0.2.0

### Added

-   Added discovery support for `chaos discover`

### Changed

-   Access token is refreshed when expired
-   No more of decorators to inject services and project context because it
    broke the experiment validation (since those arguments weren't explicitly
    passed on by the user). Good thing is API is leaner and less magical


## [0.1.0][] - 2018-04-13

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud/tree/0.1.0

### Added

-   Initial release
