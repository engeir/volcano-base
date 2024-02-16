# Changelog

## [0.8.4](https://github.com/engeir/volcano-base/compare/v0.8.3...v0.8.4) (2024-02-16)


### Bug Fixes

* **ci:** make rye command available for build step ([b9e0753](https://github.com/engeir/volcano-base/commit/b9e0753b5167e27c31459212d90e8835de8f3359))

## [0.8.3](https://github.com/engeir/volcano-base/compare/v0.8.2...v0.8.3) (2024-02-16)


### Bug Fixes

* **ci:** make sure rye manages virtualenv ([3ad9cb3](https://github.com/engeir/volcano-base/commit/3ad9cb34c0e8e05c7f7cc002f4ed307a91d1ad5f))

## [0.8.2](https://github.com/engeir/volcano-base/compare/v0.8.1...v0.8.2) (2024-02-16)


### Bug Fixes

* **ci:** make rye command available ([f762fa3](https://github.com/engeir/volcano-base/commit/f762fa3cc7ce7f696bd83b6ee5a76d47d933489b))

## [0.8.1](https://github.com/engeir/volcano-base/compare/v0.8.0...v0.8.1) (2024-02-16)


### Bug Fixes

* **ci:** install rye without prompting ([668a7c1](https://github.com/engeir/volcano-base/commit/668a7c1ecdd072e664a08e504fb829dfa0b3d081))

## [0.8.0](https://github.com/engeir/volcano-base/compare/v0.7.1...v0.8.0) (2024-02-16)


### Features

* **manipulate:** add function that finds sampling rate ([47f7e49](https://github.com/engeir/volcano-base/commit/47f7e49431596faf0404ded5b39135693265f05a))

## [0.7.1](https://github.com/engeir/volcano-base/compare/v0.7.0...v0.7.1) (2024-02-13)


### Bug Fixes

* **get_median:** keep xarray attributes after operation ([f6d998e](https://github.com/engeir/volcano-base/commit/f6d998e2bc101edd710a91a37e3827e04f56be62))

## [0.7.0](https://github.com/engeir/volcano-base/compare/v0.6.1...v0.7.0) (2024-02-13)


### Features

* **manipulate:** add array to list operation wrapper ([a4d7439](https://github.com/engeir/volcano-base/commit/a4d7439b8abf663e291c6055f6b10906c37ce529))

## [0.6.1](https://github.com/engeir/volcano-base/compare/v0.6.0...v0.6.1) (2024-02-12)


### Bug Fixes

* **manipulate:** add func to module init ([b7e7a01](https://github.com/engeir/volcano-base/commit/b7e7a016bcd1f49879b797cb54140f0fdbdfe8be))

## [0.6.0](https://github.com/engeir/volcano-base/compare/v0.5.0...v0.6.0) (2024-02-12)


### Features

* **manipulate:** add function to subtract based on time series tail ([02ff1f1](https://github.com/engeir/volcano-base/commit/02ff1f101f0037f025f22faa0b64a82c41695485))


### Bug Fixes

* **deps:** need h5netcdf and dask to load xarrays in FindFiles ([f1d6644](https://github.com/engeir/volcano-base/commit/f1d66445ba9c2fce04f68134808c0a2127d13779))

## [0.5.0](https://github.com/engeir/volcano-base/compare/v0.4.0...v0.5.0) (2024-01-30)


### Features

* **load:** load full ensemble and mean RF and T arrays from OB16 ([3b68bfb](https://github.com/engeir/volcano-base/commit/3b68bfb3e0da4c89170cac80e64b910a770f3d6d))


### Documentation

* **down:** add note in docstring about usage ([90ea57e](https://github.com/engeir/volcano-base/commit/90ea57ea8c726a083c2fd733b378a7d0e8d6555b))

## [0.4.0](https://github.com/engeir/volcano-base/compare/v0.3.3...v0.4.0) (2024-01-18)


### Features

* **load:** implement strategy to load OB16 output data ([1765da9](https://github.com/engeir/volcano-base/commit/1765da915100c8894ab8dfe06ca08fa1be4f1aba))

## [0.3.3](https://github.com/engeir/volcano-base/compare/v0.3.2...v0.3.3) (2024-01-18)


### Bug Fixes

* **imports:** allow easier access from the load module ([c3d48ff](https://github.com/engeir/volcano-base/commit/c3d48ffce22dfab891c3548dd8f0c692e2d35f67))

## [0.3.2](https://github.com/engeir/volcano-base/compare/v0.3.1...v0.3.2) (2024-01-18)


### Bug Fixes

* forgot name change in config.py ([aa3c894](https://github.com/engeir/volcano-base/commit/aa3c8945cade1704bd55c8222ba027fe9c432a10))

## [0.3.1](https://github.com/engeir/volcano-base/compare/v0.3.0...v0.3.1) (2024-01-18)


### Features

* publish package to pypi ([205df5e](https://github.com/engeir/volcano-base/commit/205df5ebc3404f1d4e7c26386abe473e82f2b3e1))


### Bug Fixes

* checkout repo... ([3ecf38d](https://github.com/engeir/volcano-base/commit/3ecf38d3b4df1b46b3b5a80fb019d10708be09b3))
* evaluate mise activate command ([520cb83](https://github.com/engeir/volcano-base/commit/520cb8349e4a590350922a8daa287c2b7e79a0a0))
* **imports:** incorrect module path ([c849137](https://github.com/engeir/volcano-base/commit/c8491373d070dd0d6fcf03c75df9466d9bbc449a))
* keep only essential commands ([455fcf9](https://github.com/engeir/volcano-base/commit/455fcf997658e715a11874733721161f4d700139))
* mise activate bash ([d43ae0a](https://github.com/engeir/volcano-base/commit/d43ae0a3f5850c7249c7cacb43cc12805cdefd95))
* mise must be activated ([084adcb](https://github.com/engeir/volcano-base/commit/084adcb9f4c5c14e21d53d6b24e46b51deb67c70))
* mise tasks are experimental and must be activated ([4ab703b](https://github.com/engeir/volcano-base/commit/4ab703bef07ce41fc37dcd0a6e856865cc4f1e0f))
* move commands around ([38aac4c](https://github.com/engeir/volcano-base/commit/38aac4c54fe22127f685ac7e9a28ae207647fa72))
* need mise activate bash evaluated ([2b64909](https://github.com/engeir/volcano-base/commit/2b64909f23e52e672ae325463412185b73dd8ba3))
* not a fix, just forcing release ([1870b4a](https://github.com/engeir/volcano-base/commit/1870b4a771e4024c7d30215141ba72674210f45a))
* release v0.3.1 ([3609997](https://github.com/engeir/volcano-base/commit/36099977e3412e6f50884f0e9c1ec69362e3be08))
* rename project to publish to PyPI ([ac9cb16](https://github.com/engeir/volcano-base/commit/ac9cb16049bd6a6b85cd5955b15b604b26e06ae2))
* style in workflow ([5bc93eb](https://github.com/engeir/volcano-base/commit/5bc93ebf819cd50bdd6a61997080303e34906ea3))
* update workflow ([1c6de7a](https://github.com/engeir/volcano-base/commit/1c6de7ab20a2a97cc66f1629bda08f53646d2bb7))
* workflow ([38069e0](https://github.com/engeir/volcano-base/commit/38069e0c7e13b72d7101a02ef61ecec1c33cf73b))


### Miscellaneous Chores

* release 0.2.0 ([d1241e2](https://github.com/engeir/volcano-base/commit/d1241e246d0609bcbf2728e58d9c0778055b7023))
* release 0.2.0 ([8c9f017](https://github.com/engeir/volcano-base/commit/8c9f0172cadb3ac4c61f218c821cb9128b9487c7))
* release 0.3.1 ([14d5708](https://github.com/engeir/volcano-base/commit/14d57086cb36947e7fbc0ca24c3a8a0d331e2545))

## [0.3.0](https://github.com/engeir/volcano-base/compare/v0.2.12...v0.3.0) (2024-01-18)


### Features

* publish package to pypi ([205df5e](https://github.com/engeir/volcano-base/commit/205df5ebc3404f1d4e7c26386abe473e82f2b3e1))


### Bug Fixes

* rename project to publish to PyPI ([ac9cb16](https://github.com/engeir/volcano-base/commit/ac9cb16049bd6a6b85cd5955b15b604b26e06ae2))

## [0.2.12](https://github.com/engeir/volcano-core/compare/v0.2.11...v0.2.12) (2024-01-18)


### Bug Fixes

* move commands around ([38aac4c](https://github.com/engeir/volcano-core/commit/38aac4c54fe22127f685ac7e9a28ae207647fa72))

## [0.2.11](https://github.com/engeir/volcano-core/compare/v0.2.10...v0.2.11) (2024-01-18)


### Bug Fixes

* need mise activate bash evaluated ([2b64909](https://github.com/engeir/volcano-core/commit/2b64909f23e52e672ae325463412185b73dd8ba3))

## [0.2.10](https://github.com/engeir/volcano-core/compare/v0.2.9...v0.2.10) (2024-01-18)


### Bug Fixes

* keep only essential commands ([455fcf9](https://github.com/engeir/volcano-core/commit/455fcf997658e715a11874733721161f4d700139))

## [0.2.9](https://github.com/engeir/volcano-core/compare/v0.2.8...v0.2.9) (2024-01-18)


### Bug Fixes

* checkout repo... ([3ecf38d](https://github.com/engeir/volcano-core/commit/3ecf38d3b4df1b46b3b5a80fb019d10708be09b3))

## [0.2.8](https://github.com/engeir/volcano-core/compare/v0.2.7...v0.2.8) (2024-01-18)


### Bug Fixes

* workflow ([38069e0](https://github.com/engeir/volcano-core/commit/38069e0c7e13b72d7101a02ef61ecec1c33cf73b))

## [0.2.7](https://github.com/engeir/volcano-core/compare/v0.2.6...v0.2.7) (2024-01-18)


### Bug Fixes

* update workflow ([1c6de7a](https://github.com/engeir/volcano-core/commit/1c6de7ab20a2a97cc66f1629bda08f53646d2bb7))

## [0.2.6](https://github.com/engeir/volcano-core/compare/v0.2.5...v0.2.6) (2024-01-18)


### Bug Fixes

* evaluate mise activate command ([520cb83](https://github.com/engeir/volcano-core/commit/520cb8349e4a590350922a8daa287c2b7e79a0a0))

## [0.2.5](https://github.com/engeir/volcano-core/compare/v0.2.4...v0.2.5) (2024-01-17)


### Bug Fixes

* mise activate bash ([d43ae0a](https://github.com/engeir/volcano-core/commit/d43ae0a3f5850c7249c7cacb43cc12805cdefd95))

## [0.2.4](https://github.com/engeir/volcano-core/compare/v0.2.3...v0.2.4) (2024-01-17)


### Bug Fixes

* mise must be activated ([084adcb](https://github.com/engeir/volcano-core/commit/084adcb9f4c5c14e21d53d6b24e46b51deb67c70))

## [0.2.3](https://github.com/engeir/volcano-core/compare/v0.2.2...v0.2.3) (2024-01-17)


### Bug Fixes

* mise tasks are experimental and must be activated ([4ab703b](https://github.com/engeir/volcano-core/commit/4ab703bef07ce41fc37dcd0a6e856865cc4f1e0f))

## [0.2.2](https://github.com/engeir/volcano-core/compare/v0.2.1...v0.2.2) (2024-01-17)


### Bug Fixes

* style in workflow ([5bc93eb](https://github.com/engeir/volcano-core/commit/5bc93ebf819cd50bdd6a61997080303e34906ea3))

## [0.2.1](https://github.com/engeir/volcano-core/compare/v0.2.0...v0.2.1) (2024-01-17)


### Bug Fixes

* not a fix, just forcing release ([1870b4a](https://github.com/engeir/volcano-core/commit/1870b4a771e4024c7d30215141ba72674210f45a))

## [0.2.0](https://github.com/engeir/volcano-core/compare/v0.1.0...v0.2.0) (2024-01-17)


### Bug Fixes

* **imports:** incorrect module path ([c849137](https://github.com/engeir/volcano-core/commit/c8491373d070dd0d6fcf03c75df9466d9bbc449a))


### Miscellaneous Chores

* release 0.2.0 ([d1241e2](https://github.com/engeir/volcano-core/commit/d1241e246d0609bcbf2728e58d9c0778055b7023))
* release 0.2.0 ([8c9f017](https://github.com/engeir/volcano-core/commit/8c9f0172cadb3ac4c61f218c821cb9128b9487c7))

## [0.1.1](https://github.com/engeir/volcano-core/compare/v0.1.0...v0.1.1) (2024-01-17)


### Continuous Integration

* **test:** set up publish to test.pypi.org ([d84fb84](https://github.com/engeir/volcano-core/commit/d84fb842c0229b583aeee9c52b05b10e9e1584b1))

## 0.1.0 (2024-01-17)


### Miscellaneous

* initial commit ([b2d9381](https://github.com/engeir/volcano-core/commit/b2d93814d8bf10f35b939e55df9fb8b1fe27e178))
