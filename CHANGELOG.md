# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit/chaostoolkit-google-cloud/compare/0.2.0...HEAD

## [0.2.0][] - 2018-04-23

[0.2.0]: https://github.com/chaostoolkit/chaostoolkit-google-cloud/tree/0.2.0

### Added

-   Added discovery support for `chaos discover`

### Changed

-   Access token is refreshed when expired
-   No more of decorators to inject services and project context because it
    broke the experiment validation (since those arguments weren't explicitly
    passed on by the user). Good thing is API is leaner and less magical


## [0.1.0][] - 2018-04-13

[0.1.0]: https://github.com/chaostoolkit/chaostoolkit-google-cloud/tree/0.1.0

### Added

-   Initial release
