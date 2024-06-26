# Changelog

## [0.3.1](https://github.com/engeir/volcano-base/compare/v2.0.5...v0.3.1) (2024-06-26)


### ⚠ BREAKING CHANGES

* **cesm load:** use a regex class object to specify files to find
* **ob16:** rewrite into a class ([#53](https://github.com/engeir/volcano-base/issues/53))

### Features

* **cesm load:** use a regex class object to specify files to find ([793c0a9](https://github.com/engeir/volcano-base/commit/793c0a90b8536eb8b299c12ad0bf692f633d51e7))
* **cesm2:** implement functions that download NIRD archive ([35c1955](https://github.com/engeir/volcano-base/commit/35c1955036542fccf4d3d03098c008d5ccd8e689))
* **down:** add RF control to downloadable datasets (FSNTOA) ([8566ec9](https://github.com/engeir/volcano-base/commit/8566ec955593f19aaf1bd8aac1aa621fee25b57f))
* **load:** implement strategy to load OB16 output data ([1765da9](https://github.com/engeir/volcano-base/commit/1765da915100c8894ab8dfe06ca08fa1be4f1aba))
* **load:** load full ensemble and mean RF and T arrays from OB16 ([3b68bfb](https://github.com/engeir/volcano-base/commit/3b68bfb3e0da4c89170cac80e64b910a770f3d6d))
* **manipulate:** add array to list operation wrapper ([a4d7439](https://github.com/engeir/volcano-base/commit/a4d7439b8abf663e291c6055f6b10906c37ce529))
* **manipulate:** add function that finds sampling rate ([47f7e49](https://github.com/engeir/volcano-base/commit/47f7e49431596faf0404ded5b39135693265f05a))
* **manipulate:** add function to subtract based on time series tail ([02ff1f1](https://github.com/engeir/volcano-base/commit/02ff1f101f0037f025f22faa0b64a82c41695485))
* **ob16:** add an optional progress bar when loading data ([d4b253d](https://github.com/engeir/volcano-base/commit/d4b253d6e7b7cf9c789e6720d0277271386ff80a))
* **ob16:** add SO2 decay to aligned arrays ([278bfaa](https://github.com/engeir/volcano-base/commit/278bfaae9ffcaef5d6d942f7021f178520c0e1b8))
* **ob16:** remove xr.align in favour of normal slice ([e6f71e9](https://github.com/engeir/volcano-base/commit/e6f71e93f3b5c7d4908f070260048c3a1a402446))
* publish package to pypi ([205df5e](https://github.com/engeir/volcano-base/commit/205df5ebc3404f1d4e7c26386abe473e82f2b3e1))
* **time series:** add subtract_climatology function ([5a70b59](https://github.com/engeir/volcano-base/commit/5a70b59b3f4b234fc48b94c73b70955e74a71563))
* **time series:** add weighted_month_mean ([f4a9a94](https://github.com/engeir/volcano-base/commit/f4a9a94b980d5b8c5304460dc6d3800026665614))
* **time series:** adds approx_align function ([5b82d25](https://github.com/engeir/volcano-base/commit/5b82d25a75f13938f2efc125c24e88b3833be14a))


### Bug Fixes

* **cesm2 load:** use match group 'ensemble', since this matches with the data attrs ([51579ff](https://github.com/engeir/volcano-base/commit/51579ff59ea0733ed6ef3c8aab3e6210812afde4))
* checkout repo... ([3ecf38d](https://github.com/engeir/volcano-base/commit/3ecf38d3b4df1b46b3b5a80fb019d10708be09b3))
* **ci:** install rye without prompting ([668a7c1](https://github.com/engeir/volcano-base/commit/668a7c1ecdd072e664a08e504fb829dfa0b3d081))
* **ci:** make rye command available ([f762fa3](https://github.com/engeir/volcano-base/commit/f762fa3cc7ce7f696bd83b6ee5a76d47d933489b))
* **ci:** make rye command available for build step ([b9e0753](https://github.com/engeir/volcano-base/commit/b9e0753b5167e27c31459212d90e8835de8f3359))
* **ci:** make sure rye manages virtualenv ([3ad9cb3](https://github.com/engeir/volcano-base/commit/3ad9cb34c0e8e05c7f7cc002f4ed307a91d1ad5f))
* **ci:** use rye directly, via mise did not work ([082989c](https://github.com/engeir/volcano-base/commit/082989c95f85994638dd251a8a923582ea66bd94))
* **deps:** need h5netcdf and dask to load xarrays in FindFiles ([f1d6644](https://github.com/engeir/volcano-base/commit/f1d66445ba9c2fce04f68134808c0a2127d13779))
* evaluate mise activate command ([520cb83](https://github.com/engeir/volcano-base/commit/520cb8349e4a590350922a8daa287c2b7e79a0a0))
* **FindFiles:** keep most recent was not removing all old files ([ea594a2](https://github.com/engeir/volcano-base/commit/ea594a2f91c62bcdaf151646c186b2bece19a828))
* forgot name change in config.py ([aa3c894](https://github.com/engeir/volcano-base/commit/aa3c8945cade1704bd55c8222ba027fe9c432a10))
* **get_median:** keep xarray attributes after operation ([f6d998e](https://github.com/engeir/volcano-base/commit/f6d998e2bc101edd710a91a37e3827e04f56be62))
* **imports:** allow easier access from the load module ([c3d48ff](https://github.com/engeir/volcano-base/commit/c3d48ffce22dfab891c3548dd8f0c692e2d35f67))
* **imports:** incorrect module path ([c849137](https://github.com/engeir/volcano-base/commit/c8491373d070dd0d6fcf03c75df9466d9bbc449a))
* keep only essential commands ([455fcf9](https://github.com/engeir/volcano-base/commit/455fcf997658e715a11874733721161f4d700139))
* **manipulate:** add func to module init ([b7e7a01](https://github.com/engeir/volcano-base/commit/b7e7a016bcd1f49879b797cb54140f0fdbdfe8be))
* **manipulate:** add sample_rate function as entry point in module ([d4e9995](https://github.com/engeir/volcano-base/commit/d4e99957d109db22b8a228105dfc31e185a16802))
* **manipulate:** get_median accepts arbitrary dimensions provided one is time ([9197a72](https://github.com/engeir/volcano-base/commit/9197a7276d4f3423dcace0fdb434d76f39f57162))
* **manipulate:** mean_flatten should copy the dims list input parameter ([9623f4a](https://github.com/engeir/volcano-base/commit/9623f4a9fa54b0743da80e2f4b5556aa83fdf6a4))
* mise activate bash ([d43ae0a](https://github.com/engeir/volcano-base/commit/d43ae0a3f5850c7249c7cacb43cc12805cdefd95))
* mise must be activated ([084adcb](https://github.com/engeir/volcano-base/commit/084adcb9f4c5c14e21d53d6b24e46b51deb67c70))
* mise tasks are experimental and must be activated ([4ab703b](https://github.com/engeir/volcano-base/commit/4ab703bef07ce41fc37dcd0a6e856865cc4f1e0f))
* move commands around ([38aac4c](https://github.com/engeir/volcano-base/commit/38aac4c54fe22127f685ac7e9a28ae207647fa72))
* need mise activate bash evaluated ([2b64909](https://github.com/engeir/volcano-base/commit/2b64909f23e52e672ae325463412185b73dd8ba3))
* not a fix, just forcing release ([1870b4a](https://github.com/engeir/volcano-base/commit/1870b4a771e4024c7d30215141ba72674210f45a))
* **ob16:** apply groupby operation from variable, not string ([397fb83](https://github.com/engeir/volcano-base/commit/397fb83cc394119fb33357a9d598463cd959d93f))
* **ob16:** expose the temperature control signal as a class attribute ([d0f6a19](https://github.com/engeir/volcano-base/commit/d0f6a19b8ae03ea24d5a8d624f35940627db02c8))
* **ob16:** incorrectly assigned SO2 RF-aligned to SO2 temp-aligned ([c7587b7](https://github.com/engeir/volcano-base/commit/c7587b7d461f4d008b1f151ee9a6874fbbe04a77))
* **ob16:** must consider that SO2 original is only in monthly resolution ([549d1a4](https://github.com/engeir/volcano-base/commit/549d1a455e99e167626d17118eaeb00c5ff51cb2))
* **ob16:** progress file load should not use length to all files ([2e0c044](https://github.com/engeir/volcano-base/commit/2e0c044319f5f6686430dba4d89dccf010d117aa))
* **ob16:** re-align arrays for monthly data ([2913bc1](https://github.com/engeir/volcano-base/commit/2913bc1d9f4f28488fdf7fb34c9565f9c5f92920))
* **ob16:** remove climatology from the control temperature ([fd87b01](https://github.com/engeir/volcano-base/commit/fd87b01deee2ad74db03dd6715d672027d55d0b1))
* **ob16:** scale colum SO2 so unit adjusts from kg/m2 to Tg (per Earth surface) ([7c82515](https://github.com/engeir/volcano-base/commit/7c8251584e8787d18bc964ead685e86efc5a3ef8))
* **ob16:** so2 start one index (month) earlier ([539cf70](https://github.com/engeir/volcano-base/commit/539cf700cbdf66640119f92ee8b721cd8a1cce4b))
* release v0.3.1 ([3609997](https://github.com/engeir/volcano-base/commit/36099977e3412e6f50884f0e9c1ec69362e3be08))
* rename project to publish to PyPI ([ac9cb16](https://github.com/engeir/volcano-base/commit/ac9cb16049bd6a6b85cd5955b15b604b26e06ae2))
* style in workflow ([5bc93eb](https://github.com/engeir/volcano-base/commit/5bc93ebf819cd50bdd6a61997080303e34906ea3))
* **time series:** expose approx_aligned to main module ([27399e1](https://github.com/engeir/volcano-base/commit/27399e14159419838acad1b5d6b143e63bd2d28e))
* **time series:** expose subtract_climatology to the manipulate module ([1d48f98](https://github.com/engeir/volcano-base/commit/1d48f98ae91677221ce576c63d834414627041f8))
* update workflow ([1c6de7a](https://github.com/engeir/volcano-base/commit/1c6de7ab20a2a97cc66f1629bda08f53646d2bb7))
* workflow ([38069e0](https://github.com/engeir/volcano-base/commit/38069e0c7e13b72d7101a02ef61ecec1c33cf73b))


### Miscellaneous

* **cesm2 load:** do not create parent directories ([5e59dcd](https://github.com/engeir/volcano-base/commit/5e59dcdd78b069f70c525de05d1883f6f05baa09))
* **cesm2 load:** print path of where we look for files ([7e57d94](https://github.com/engeir/volcano-base/commit/7e57d947eb01b3367a7062b78f954a798be1c238))
* **deps-dev:** bump pre-commit from 3.6.0 to 3.6.1 ([#41](https://github.com/engeir/volcano-base/issues/41)) ([462404a](https://github.com/engeir/volcano-base/commit/462404a0c856b727eeff6ae902753eb0c8a07ec2))
* **deps-dev:** bump pydoclint from 0.3.9 to 0.4.0 ([#38](https://github.com/engeir/volcano-base/issues/38)) ([89b1e45](https://github.com/engeir/volcano-base/commit/89b1e45bbc3089248c984681175adbc0628f5aa8))
* **deps-dev:** bump pytest from 7.4.4 to 8.0.0 ([#31](https://github.com/engeir/volcano-base/issues/31)) ([d1e7bc9](https://github.com/engeir/volcano-base/commit/d1e7bc90a01f3abaa25dcb42484a8ee5a9de2d6a))
* **deps-dev:** bump ruff from 0.1.13 to 0.1.14 ([#27](https://github.com/engeir/volcano-base/issues/27)) ([9485f8c](https://github.com/engeir/volcano-base/commit/9485f8c2a3e0b13787b1edba55a1f116a9fb5c85))
* **deps-dev:** bump ruff from 0.1.14 to 0.1.15 ([#32](https://github.com/engeir/volcano-base/issues/32)) ([4886693](https://github.com/engeir/volcano-base/commit/488669379a29720901dd81853e44c61a1c4b793b))
* **deps-dev:** bump ruff from 0.1.15 to 0.2.0 ([#34](https://github.com/engeir/volcano-base/issues/34)) ([ad98e24](https://github.com/engeir/volcano-base/commit/ad98e244e2cfd97943af1ae3c75660efcc89564e))
* **deps-dev:** bump ruff from 0.2.0 to 0.2.1 ([#36](https://github.com/engeir/volcano-base/issues/36)) ([cc3aa64](https://github.com/engeir/volcano-base/commit/cc3aa64fe72ad9e516aec267ba9efe7fd6d76b48))
* **deps-dev:** bump types-requests ([#29](https://github.com/engeir/volcano-base/issues/29)) ([406a4ed](https://github.com/engeir/volcano-base/commit/406a4ed92a1454d281faf3e6cfb0be32a8c45038))
* **deps-dev:** bump xdoctest from 1.1.2 to 1.1.3 ([#33](https://github.com/engeir/volcano-base/issues/33)) ([f41ebac](https://github.com/engeir/volcano-base/commit/f41ebac8e2f85456640567e16009e02d93234120))
* **deps:** bump actions/checkout from 3 to 4 ([#25](https://github.com/engeir/volcano-base/issues/25)) ([704027c](https://github.com/engeir/volcano-base/commit/704027cce8d534d719d3858117ebb0b0a9dea3c6))
* **deps:** bump google-github-actions/release-please-action ([#2](https://github.com/engeir/volcano-base/issues/2)) ([a467020](https://github.com/engeir/volcano-base/commit/a46702077c64893429f6ff6606bc120f32699f13))
* **deps:** bump numpy from 1.26.3 to 1.26.4 ([#35](https://github.com/engeir/volcano-base/issues/35)) ([0fe395e](https://github.com/engeir/volcano-base/commit/0fe395edc8cddf766b38a6263b25b0b6eaaacfe6))
* **deps:** bump pypa/gh-action-pypi-publish from 1.8.11 to 1.8.12 ([#52](https://github.com/engeir/volcano-base/issues/52)) ([a5d03f9](https://github.com/engeir/volcano-base/commit/a5d03f927bc9f8925e34a36800a59c81f69c588a))
* **deps:** bump pypa/gh-action-pypi-publish from 1.8.12 to 1.8.14 ([#64](https://github.com/engeir/volcano-base/issues/64)) ([58e3b17](https://github.com/engeir/volcano-base/commit/58e3b17fb324871c73cfc6eb055d14955139e78c))
* **deps:** bump pypa/gh-action-pypi-publish from 1.8.14 to 1.9.0 ([#80](https://github.com/engeir/volcano-base/issues/80)) ([f5e6486](https://github.com/engeir/volcano-base/commit/f5e6486fca255aca30720b301f316c81fb70ae08))
* **deps:** bump scipy from 1.11.4 to 1.12.0 ([#26](https://github.com/engeir/volcano-base/issues/26)) ([69c3c73](https://github.com/engeir/volcano-base/commit/69c3c738fe39ae1162756edda63cd799e3ac68ac))
* **deps:** bump xarray from 2023.12.0 to 2024.1.0 ([#24](https://github.com/engeir/volcano-base/issues/24)) ([d98e61d](https://github.com/engeir/volcano-base/commit/d98e61df2b07efb89607a99c7d52cd4b41164810))
* **deps:** bump xarray from 2024.1.0 to 2024.1.1 ([#28](https://github.com/engeir/volcano-base/issues/28)) ([03e3e3b](https://github.com/engeir/volcano-base/commit/03e3e3baff2b3631e61daad31916cd8736830522))
* **docs:** fix docstrings in subtract_climatology ([7e689e6](https://github.com/engeir/volcano-base/commit/7e689e6091231d71d728e157530d6df7c6a171d7))
* edit release-please config ([e2903ef](https://github.com/engeir/volcano-base/commit/e2903efce67e1d4882e022f52e891e5d14b8c4be))
* **FindFiles:** add __repr__ ([86b33bf](https://github.com/engeir/volcano-base/commit/86b33bff39b3ba926ff54637536fefa048d93ee3))
* fix comment ([b3e8232](https://github.com/engeir/volcano-base/commit/b3e8232b51f54aca2eca932f10f4d9b7b8703457))
* fix? ([61419f7](https://github.com/engeir/volcano-base/commit/61419f767cf27bd0f2bb59d900309dff4c27d9c4))
* fix?? ([659504a](https://github.com/engeir/volcano-base/commit/659504ae340b0057ff73647208bae656ca8e2b13))
* **github:** remoe name of release please step ([011d659](https://github.com/engeir/volcano-base/commit/011d6597640b76151516f3feb8b9cfddcb5db74c))
* initial commit ([b2d9381](https://github.com/engeir/volcano-base/commit/b2d93814d8bf10f35b939e55df9fb8b1fe27e178))
* **main:** release 0.1.0 ([#1](https://github.com/engeir/volcano-base/issues/1)) ([3204cb8](https://github.com/engeir/volcano-base/commit/3204cb8693dacafe33b419196307fec78954d589))
* **main:** release 0.1.1 ([#3](https://github.com/engeir/volcano-base/issues/3)) ([271bd63](https://github.com/engeir/volcano-base/commit/271bd63def4360040f4416a6624a022733d569d8))
* **main:** release 0.2.0 ([#5](https://github.com/engeir/volcano-base/issues/5)) ([c7d313a](https://github.com/engeir/volcano-base/commit/c7d313a3ae17cc4ad9658914f617ba4f6e23b83f))
* **main:** release 0.2.1 ([#6](https://github.com/engeir/volcano-base/issues/6)) ([6fc8abc](https://github.com/engeir/volcano-base/commit/6fc8abc340d67608f7e49be195751c7e44bb66f4))
* **main:** release 0.2.10 ([#15](https://github.com/engeir/volcano-base/issues/15)) ([885dfe6](https://github.com/engeir/volcano-base/commit/885dfe6f9e1903b0917ddfbdb26ddb8d6a4a3fca))
* **main:** release 0.2.11 ([#16](https://github.com/engeir/volcano-base/issues/16)) ([6386297](https://github.com/engeir/volcano-base/commit/6386297992919953d1c63d8b755fce21ebecad87))
* **main:** release 0.2.12 ([#17](https://github.com/engeir/volcano-base/issues/17)) ([0133b6d](https://github.com/engeir/volcano-base/commit/0133b6d968ab2ed57fecc64c282912b65457b702))
* **main:** release 0.2.2 ([#7](https://github.com/engeir/volcano-base/issues/7)) ([9f5119a](https://github.com/engeir/volcano-base/commit/9f5119abe478cd20f985c6f2052691f3934a88c8))
* **main:** release 0.2.3 ([#8](https://github.com/engeir/volcano-base/issues/8)) ([3a1d877](https://github.com/engeir/volcano-base/commit/3a1d877560171b9015a8b0fc37235bafdd796e2c))
* **main:** release 0.2.4 ([#9](https://github.com/engeir/volcano-base/issues/9)) ([ee2e1bf](https://github.com/engeir/volcano-base/commit/ee2e1bf2f286eccaf2f48e93904a517441718412))
* **main:** release 0.2.5 ([#10](https://github.com/engeir/volcano-base/issues/10)) ([9e51f8e](https://github.com/engeir/volcano-base/commit/9e51f8ed29c6209c976f21f3df43116647a9d386))
* **main:** release 0.2.6 ([#11](https://github.com/engeir/volcano-base/issues/11)) ([8503369](https://github.com/engeir/volcano-base/commit/85033690839784f9897953ad2af7325f569392cd))
* **main:** release 0.2.7 ([#12](https://github.com/engeir/volcano-base/issues/12)) ([b2d1e3d](https://github.com/engeir/volcano-base/commit/b2d1e3dc38d0b1d901d3a10b8dcd75ed272e37ab))
* **main:** release 0.2.8 ([#13](https://github.com/engeir/volcano-base/issues/13)) ([9723e54](https://github.com/engeir/volcano-base/commit/9723e542425a53f7a0512651f418571fad2df829))
* **main:** release 0.2.9 ([#14](https://github.com/engeir/volcano-base/issues/14)) ([f40bb58](https://github.com/engeir/volcano-base/commit/f40bb58b2a47fa3a6104c686e0a5a2d78c947dc7))
* **main:** release 0.3.0 ([#19](https://github.com/engeir/volcano-base/issues/19)) ([fb927d7](https://github.com/engeir/volcano-base/commit/fb927d7cde9c83fc77359eda9c07f046bad80291))
* **main:** release 0.3.1 ([#20](https://github.com/engeir/volcano-base/issues/20)) ([1feaeae](https://github.com/engeir/volcano-base/commit/1feaeae2f88a70a51b9e176cd2434aea87fe47f0))
* **main:** release 0.3.2 ([#21](https://github.com/engeir/volcano-base/issues/21)) ([933b45f](https://github.com/engeir/volcano-base/commit/933b45f29e1c8bb5c79cad7f656d93486c5061c1))
* **main:** release 0.3.3 ([#22](https://github.com/engeir/volcano-base/issues/22)) ([170e50b](https://github.com/engeir/volcano-base/commit/170e50b7f2dbbe29c34bee0df1176cf0c8b00a08))
* **main:** release 0.4.0 ([#23](https://github.com/engeir/volcano-base/issues/23)) ([e66527f](https://github.com/engeir/volcano-base/commit/e66527f1f9ddb312eb76ad933c811ba1ab23a0cb))
* **main:** release 0.5.0 ([#30](https://github.com/engeir/volcano-base/issues/30)) ([ba3232c](https://github.com/engeir/volcano-base/commit/ba3232c628fee37dac8a770306bb258084c6e1d4))
* **main:** release 0.6.0 ([#39](https://github.com/engeir/volcano-base/issues/39)) ([eb032e6](https://github.com/engeir/volcano-base/commit/eb032e647c95850c925f36cccc6ed345c5fd334d))
* **main:** release 0.6.1 ([#40](https://github.com/engeir/volcano-base/issues/40)) ([8501278](https://github.com/engeir/volcano-base/commit/85012782aabb217b906a54e1d4791cc0120feedc))
* **main:** release 0.7.0 ([#42](https://github.com/engeir/volcano-base/issues/42)) ([51f9522](https://github.com/engeir/volcano-base/commit/51f9522f233a6d9a790227b90d6b513ecef86da9))
* **main:** release 0.7.1 ([#43](https://github.com/engeir/volcano-base/issues/43)) ([a06b1e2](https://github.com/engeir/volcano-base/commit/a06b1e28c156915a9953040382c17a8e9bedf851))
* **main:** release 0.8.0 ([#45](https://github.com/engeir/volcano-base/issues/45)) ([40d2ffb](https://github.com/engeir/volcano-base/commit/40d2ffbbe3df924a039d835513627e73349efb7c))
* **main:** release 0.8.1 ([#46](https://github.com/engeir/volcano-base/issues/46)) ([4e8f6f5](https://github.com/engeir/volcano-base/commit/4e8f6f5fd10ad76bbe3cc0561c5c9a0824ac0f28))
* **main:** release 0.8.2 ([#47](https://github.com/engeir/volcano-base/issues/47)) ([ccefd9c](https://github.com/engeir/volcano-base/commit/ccefd9c4069ef203b76d4317d7988aa21ddb25a7))
* **main:** release 0.8.3 ([#48](https://github.com/engeir/volcano-base/issues/48)) ([cfc654b](https://github.com/engeir/volcano-base/commit/cfc654b04fb2f19637ef5cc5dc6a7b0720d0fcce))
* **main:** release 0.8.4 ([#49](https://github.com/engeir/volcano-base/issues/49)) ([76c437d](https://github.com/engeir/volcano-base/commit/76c437d928008fd90833e08512c6ecb1f59d2c40))
* **main:** release 0.8.5 ([#50](https://github.com/engeir/volcano-base/issues/50)) ([89490e6](https://github.com/engeir/volcano-base/commit/89490e6d9f2457c3d636d916c30bad42b8eb24a8))
* **main:** release 0.8.6 ([#51](https://github.com/engeir/volcano-base/issues/51)) ([038ee0e](https://github.com/engeir/volcano-base/commit/038ee0e8db3b1656dee6f5401ef869d6ccf599d3))
* **main:** release 1.0.0 ([#54](https://github.com/engeir/volcano-base/issues/54)) ([b81cdc7](https://github.com/engeir/volcano-base/commit/b81cdc73db29d9a18e1c177ce0956cc89c731c7c))
* **main:** release 1.1.0 ([#55](https://github.com/engeir/volcano-base/issues/55)) ([ca1b40b](https://github.com/engeir/volcano-base/commit/ca1b40bb05deec9810638d1c28dc0de63f3fcb16))
* **main:** release 1.2.0 ([#56](https://github.com/engeir/volcano-base/issues/56)) ([1be211b](https://github.com/engeir/volcano-base/commit/1be211b3ee2b7d89eebac129108673873898c3b6))
* **main:** release 1.2.1 ([#57](https://github.com/engeir/volcano-base/issues/57)) ([cf53839](https://github.com/engeir/volcano-base/commit/cf538399cf7eb2eecdb685fcecf117779ae97c9b))
* **main:** release 1.3.0 ([#58](https://github.com/engeir/volcano-base/issues/58)) ([11b316b](https://github.com/engeir/volcano-base/commit/11b316b3f385a033e8e0e9713f4f8a168e5ae0c8))
* **main:** release 1.4.0 ([#59](https://github.com/engeir/volcano-base/issues/59)) ([cca0ae9](https://github.com/engeir/volcano-base/commit/cca0ae9eb7982aabd3373cc9084674696215573d))
* **main:** release 1.4.1 ([#60](https://github.com/engeir/volcano-base/issues/60)) ([3a51bcf](https://github.com/engeir/volcano-base/commit/3a51bcf5e9b9fa6eb9e46891425f25fff34c92d1))
* **main:** release 1.4.2 ([#61](https://github.com/engeir/volcano-base/issues/61)) ([d86b46e](https://github.com/engeir/volcano-base/commit/d86b46e982f4dcad978c87fc87375d5dbe0e307d))
* **main:** release 1.4.3 ([#62](https://github.com/engeir/volcano-base/issues/62)) ([9c4f37e](https://github.com/engeir/volcano-base/commit/9c4f37eaa70a5bbf4194adb708f59ff14a88368a))
* **main:** release 1.4.4 ([#63](https://github.com/engeir/volcano-base/issues/63)) ([86a7ae8](https://github.com/engeir/volcano-base/commit/86a7ae842e95f2632b92bbc219ae125542c69900))
* **main:** release 1.5.0 ([#65](https://github.com/engeir/volcano-base/issues/65)) ([0162e51](https://github.com/engeir/volcano-base/commit/0162e514561d4d0e3eaa2947f7a9d55246e1500e))
* **main:** release 1.5.1 ([#66](https://github.com/engeir/volcano-base/issues/66)) ([74f8f55](https://github.com/engeir/volcano-base/commit/74f8f5516d399f4ac756ef2a74f7f664c0321c78))
* **main:** release 1.6.0 ([#67](https://github.com/engeir/volcano-base/issues/67)) ([df10da1](https://github.com/engeir/volcano-base/commit/df10da1453e41d098db832e60ad097f55152649e))
* **main:** release 1.6.1 ([#68](https://github.com/engeir/volcano-base/issues/68)) ([a6e4db2](https://github.com/engeir/volcano-base/commit/a6e4db2c4833b21fe0d2245dc2c08b618830f415))
* **main:** release 1.6.2 ([#69](https://github.com/engeir/volcano-base/issues/69)) ([58572b4](https://github.com/engeir/volcano-base/commit/58572b455ae865ca90f4317221dfad8a98628615))
* **main:** release 1.7.0 ([#70](https://github.com/engeir/volcano-base/issues/70)) ([78128a8](https://github.com/engeir/volcano-base/commit/78128a89da718493f80df3151dbb522ab5ef863e))
* **main:** release 1.8.0 ([#71](https://github.com/engeir/volcano-base/issues/71)) ([2bb632a](https://github.com/engeir/volcano-base/commit/2bb632af872c49509f98b24f1109c1134f327384))
* **main:** release 1.8.1 ([#72](https://github.com/engeir/volcano-base/issues/72)) ([685c2c5](https://github.com/engeir/volcano-base/commit/685c2c5cb4ee60b489fb0de3840d95799109521a))
* **main:** release 1.8.2 ([#73](https://github.com/engeir/volcano-base/issues/73)) ([8e8e04b](https://github.com/engeir/volcano-base/commit/8e8e04bb2a3021c4a5bf9639b4af2040d7c2f999))
* **main:** release 1.8.3 ([#74](https://github.com/engeir/volcano-base/issues/74)) ([02d293d](https://github.com/engeir/volcano-base/commit/02d293d199e0aa59239fcd07e9cdf7445bfe8ea3))
* **main:** release 1.8.4 ([#75](https://github.com/engeir/volcano-base/issues/75)) ([a05f480](https://github.com/engeir/volcano-base/commit/a05f4807c15738b1cd2b9529fa5f99596b81e5ac))
* **main:** release 2.0.0 ([#76](https://github.com/engeir/volcano-base/issues/76)) ([b62a0ef](https://github.com/engeir/volcano-base/commit/b62a0ef96b9a285cf16d23046389c92699a293d7))
* **main:** release 2.0.1 ([#77](https://github.com/engeir/volcano-base/issues/77)) ([4a8751c](https://github.com/engeir/volcano-base/commit/4a8751cb0bf08af8d4135da17de50648b4e96042))
* **main:** release 2.0.2 ([#78](https://github.com/engeir/volcano-base/issues/78)) ([ae63e77](https://github.com/engeir/volcano-base/commit/ae63e779b2fde22b0d5e9a51dc0bfb590506f68a))
* **main:** release 2.0.3 ([#79](https://github.com/engeir/volcano-base/issues/79)) ([55dced1](https://github.com/engeir/volcano-base/commit/55dced1046c17ff8b381c98c3f82cd8909e0453d))
* **main:** release 2.0.4 ([#81](https://github.com/engeir/volcano-base/issues/81)) ([569e3b4](https://github.com/engeir/volcano-base/commit/569e3b423448721802e5d93e494a7643f430a1c7))
* **main:** release 2.0.5 ([#83](https://github.com/engeir/volcano-base/issues/83)) ([e0fbca3](https://github.com/engeir/volcano-base/commit/e0fbca34875ccecab843755ff74e96d935ede779))
* move files next to action ([a1ed365](https://github.com/engeir/volcano-base/commit/a1ed365b4c48f674af9e9db328f7cb14acca464a))
* **ob16:** allow returning full so2, rf, temp arrays, not just peaks ([b945b2b](https://github.com/engeir/volcano-base/commit/b945b2b1d33559911e868128cac17aebcca00243))
* release 0.2.0 ([d1241e2](https://github.com/engeir/volcano-base/commit/d1241e246d0609bcbf2728e58d9c0778055b7023))
* release 0.2.0 ([8c9f017](https://github.com/engeir/volcano-base/commit/8c9f0172cadb3ac4c61f218c821cb9128b9487c7))
* release 0.3.1 ([14d5708](https://github.com/engeir/volcano-base/commit/14d57086cb36947e7fbc0ca24c3a8a0d331e2545))
* remove all but release-please ([d9de05f](https://github.com/engeir/volcano-base/commit/d9de05fc9c2bb8ee17bbdc122266bcb570f29d7a))
* remove old commented code ([9603244](https://github.com/engeir/volcano-base/commit/9603244825c521aaa3aa9df47b5ede6102a9eb1e))
* remove old comments ([a15c5bc](https://github.com/engeir/volcano-base/commit/a15c5bc868f6087b753ca98519ba68bd4e4d67c0))
* remove old config options ([73943c0](https://github.com/engeir/volcano-base/commit/73943c082a522b24c53e371e060e8b914b37924c))
* rename ([6294987](https://github.com/engeir/volcano-base/commit/6294987d85352de12e1322edbde53620b2655037))
* rename release-please config file ([e927694](https://github.com/engeir/volcano-base/commit/e927694a6193bacadfcc1d1cfdb842a25c7c9a3b))
* update ([78baf9f](https://github.com/engeir/volcano-base/commit/78baf9fbb754b45b7518e631fbd902ad4083375e))
* update release-please config ([05cd0bd](https://github.com/engeir/volcano-base/commit/05cd0bdc2f9daa4a9da2b3db841c759fe24e4bbd))
* update release.yml ([edb528c](https://github.com/engeir/volcano-base/commit/edb528c29be84bfe99c1c331c26910789cb1f562))


### Styles

* format toml and md with dprint ([5302a0b](https://github.com/engeir/volcano-base/commit/5302a0b4b346f1e944152d13dd17ff58c496a503))
* **mypy:** add stub files with stubgen ([cebdcd9](https://github.com/engeir/volcano-base/commit/cebdcd90040f03e50422ffb7b845162aee19ad5e))
* **ruff lint:** add preview mode ([131d843](https://github.com/engeir/volcano-base/commit/131d843930460790b98b4de9499fa0e7884bc755))
* **ruff:** fix lint errors enforced by preview mode ([861a151](https://github.com/engeir/volcano-base/commit/861a151d98c4a7043891bc828e8caa6511697088))


### Code Refactoring

* **cesm2 load:** better error message that hints to where files can be dowloaded ([404c952](https://github.com/engeir/volcano-base/commit/404c9521f58e57df48f3c8b32bcfb0ba17fa7ffb))
* **load:** loop inside list extend ([3d759f8](https://github.com/engeir/volcano-base/commit/3d759f8ebf4c42bda6db2b2757a6890ebf1e169b))
* **ob16:** move warning about peak finding to where this is done ([265a922](https://github.com/engeir/volcano-base/commit/265a9228056b2cdf85ffdfbb667ccb6e33d1b58a))
* **ob16:** rewrite into a class ([#53](https://github.com/engeir/volcano-base/issues/53)) ([aac6001](https://github.com/engeir/volcano-base/commit/aac600170551712bb75fdc0eb917d3e580c4befe))


### Continuous Integration

* add build and publish steps ([94359c8](https://github.com/engeir/volcano-base/commit/94359c8571b0bc830306159c35ba054ad76ab1c4))
* add path in release-please-config file ([84c8232](https://github.com/engeir/volcano-base/commit/84c8232fe20579862718476dc692395740808116))
* fix release-please config ([7bd1f7f](https://github.com/engeir/volcano-base/commit/7bd1f7f63e73b89cc40d55c31de0581a0ab0e755))
* **fix:** install rye with mise, then build ([af15abf](https://github.com/engeir/volcano-base/commit/af15abfdf5653dd6d054b6cbd67c7e5c9a205d28))
* **github:** downgrade release-please ([06651c3](https://github.com/engeir/volcano-base/commit/06651c32a285c101fe97886fce24d859738492ba))
* **github:** go back to using release-please-action v3 ([ffd74f2](https://github.com/engeir/volcano-base/commit/ffd74f204d66ab8da225d139b4e5bcc25b760a53))
* **github:** try fix the release-please action ([6cff292](https://github.com/engeir/volcano-base/commit/6cff292ab780898c296bdb71f3e82b7488e44980))
* **release:** try fix the release-please issue ([7efdd01](https://github.com/engeir/volcano-base/commit/7efdd01b6a529220d2fd737a56d1f07b0f600b59))
* **rye:** update mise tasks to use rye over poetry ([1cfae44](https://github.com/engeir/volcano-base/commit/1cfae44fdf61e65a3f740d5693aaf3b72b5a378a))
* **test:** set up publish to test.pypi.org ([d84fb84](https://github.com/engeir/volcano-base/commit/d84fb842c0229b583aeee9c52b05b10e9e1584b1))
* try quoting boolean values ([670f305](https://github.com/engeir/volcano-base/commit/670f30521043dc60729da4e4d70d0c923c5e64eb))
* update ([157954d](https://github.com/engeir/volcano-base/commit/157954dda39475f7ac446076e60dcd73503e1c97))
* update bootstrap-sha ([09d5feb](https://github.com/engeir/volcano-base/commit/09d5febdf6d012cb4de87b768f1fc8b19111d68b))
* update release-please config file ([c3a7d1d](https://github.com/engeir/volcano-base/commit/c3a7d1d31a366a2b2aa61a3bed8bf88418d97da5))
* update release-please to v4 ([acc89a9](https://github.com/engeir/volcano-base/commit/acc89a988db5ecbe1f8bdec75b3f71c37cf416a5))
* update repo name of release-please action ([c6a1b85](https://github.com/engeir/volcano-base/commit/c6a1b85db21c20f888b9c18090ae63e32cd8720c))
* update workflow ([ca199d6](https://github.com/engeir/volcano-base/commit/ca199d6378bcee6dbe6a0610baf369331e010e5c))


### Build System

* **deps-dev:** add plotting stuff for easier checking ([a221d0b](https://github.com/engeir/volcano-base/commit/a221d0ba3734f1516c4f4585f8c175de459385b3))
* **deps-dev:** bump ruff from 0.2.1 to 0.3.7 ([3d3ebf8](https://github.com/engeir/volcano-base/commit/3d3ebf86ce0cdcfaa8d1f51cf5559a642a17ca83))
* **deps:** update all ([8f01131](https://github.com/engeir/volcano-base/commit/8f011314b8b6008c4196823cb6fcdd2634d7f3b6))
* **deps:** update all dependencies ([86a32f9](https://github.com/engeir/volcano-base/commit/86a32f9cd68790e9e5779a133212b6ee3c7df470))
* **rye:** use rye with uv instead of poetry ([df41e62](https://github.com/engeir/volcano-base/commit/df41e62579f09e883e782a8bc92e0fe6e57dd8b3))


### Documentation

* **down:** add note in docstring about usage ([90ea57e](https://github.com/engeir/volcano-base/commit/90ea57ea8c726a083c2fd733b378a7d0e8d6555b))
* **time series:** refine warning message in `shift_arrays` ([100bcc0](https://github.com/engeir/volcano-base/commit/100bcc07e8c6e21c3080ec37efa92d48fb766a95))
* **time_series:** improve docstring for sampling_rate function ([3378404](https://github.com/engeir/volcano-base/commit/33784043f364eac0eb707119ec7929590eda41a4))

## [2.0.5](https://github.com/engeir/volcano-base/compare/v2.0.4...v2.0.5) (2024-06-26)


### Continuous Integration

* **fix:** install rye with mise, then build ([af15abf](https://github.com/engeir/volcano-base/commit/af15abfdf5653dd6d054b6cbd67c7e5c9a205d28))

## [2.0.4](https://github.com/engeir/volcano-base/compare/v2.0.3...v2.0.4) (2024-06-26)


### Miscellaneous

* **deps:** bump pypa/gh-action-pypi-publish from 1.8.14 to 1.9.0 ([#80](https://github.com/engeir/volcano-base/issues/80)) ([f5e6486](https://github.com/engeir/volcano-base/commit/f5e6486fca255aca30720b301f316c81fb70ae08))
* remove old commented code ([9603244](https://github.com/engeir/volcano-base/commit/9603244825c521aaa3aa9df47b5ede6102a9eb1e))


### Styles

* **mypy:** add stub files with stubgen ([cebdcd9](https://github.com/engeir/volcano-base/commit/cebdcd90040f03e50422ffb7b845162aee19ad5e))

## [2.0.3](https://github.com/engeir/volcano-base/compare/v2.0.2...v2.0.3) (2024-04-26)


### Bug Fixes

* **FindFiles:** keep most recent was not removing all old files ([ea594a2](https://github.com/engeir/volcano-base/commit/ea594a2f91c62bcdaf151646c186b2bece19a828))


### Build System

* **deps:** update all ([8f01131](https://github.com/engeir/volcano-base/commit/8f011314b8b6008c4196823cb6fcdd2634d7f3b6))

## [2.0.2](https://github.com/engeir/volcano-base/compare/v2.0.1...v2.0.2) (2024-04-19)


### Bug Fixes

* **cesm2 load:** use match group 'ensemble', since this matches with the data attrs ([51579ff](https://github.com/engeir/volcano-base/commit/51579ff59ea0733ed6ef3c8aab3e6210812afde4))

## [2.0.1](https://github.com/engeir/volcano-base/compare/v2.0.0...v2.0.1) (2024-04-19)


### Bug Fixes

* **manipulate:** get_median accepts arbitrary dimensions provided one is time ([9197a72](https://github.com/engeir/volcano-base/commit/9197a7276d4f3423dcace0fdb434d76f39f57162))
* **manipulate:** mean_flatten should copy the dims list input parameter ([9623f4a](https://github.com/engeir/volcano-base/commit/9623f4a9fa54b0743da80e2f4b5556aa83fdf6a4))


### Styles

* **ruff lint:** add preview mode ([131d843](https://github.com/engeir/volcano-base/commit/131d843930460790b98b4de9499fa0e7884bc755))
* **ruff:** fix lint errors enforced by preview mode ([861a151](https://github.com/engeir/volcano-base/commit/861a151d98c4a7043891bc828e8caa6511697088))


### Build System

* **deps-dev:** bump ruff from 0.2.1 to 0.3.7 ([3d3ebf8](https://github.com/engeir/volcano-base/commit/3d3ebf86ce0cdcfaa8d1f51cf5559a642a17ca83))
* **deps:** update all dependencies ([86a32f9](https://github.com/engeir/volcano-base/commit/86a32f9cd68790e9e5779a133212b6ee3c7df470))

## [2.0.0](https://github.com/engeir/volcano-base/compare/v1.8.4...v2.0.0) (2024-04-09)


### ⚠ BREAKING CHANGES

* **cesm load:** use a regex class object to specify files to find

### Features

* **cesm load:** use a regex class object to specify files to find ([793c0a9](https://github.com/engeir/volcano-base/commit/793c0a90b8536eb8b299c12ad0bf692f633d51e7))

## [1.8.4](https://github.com/engeir/volcano-base/compare/v1.8.3...v1.8.4) (2024-04-08)


### Bug Fixes

* **ob16:** scale colum SO2 so unit adjusts from kg/m2 to Tg (per Earth surface) ([7c82515](https://github.com/engeir/volcano-base/commit/7c8251584e8787d18bc964ead685e86efc5a3ef8))


### Miscellaneous

* **cesm2 load:** print path of where we look for files ([7e57d94](https://github.com/engeir/volcano-base/commit/7e57d947eb01b3367a7062b78f954a798be1c238))

## [1.8.3](https://github.com/engeir/volcano-base/compare/v1.8.2...v1.8.3) (2024-04-03)


### Miscellaneous

* **cesm2 load:** do not create parent directories ([5e59dcd](https://github.com/engeir/volcano-base/commit/5e59dcdd78b069f70c525de05d1883f6f05baa09))

## [1.8.2](https://github.com/engeir/volcano-base/compare/v1.8.1...v1.8.2) (2024-04-03)


### Code Refactoring

* **cesm2 load:** better error message that hints to where files can be dowloaded ([404c952](https://github.com/engeir/volcano-base/commit/404c9521f58e57df48f3c8b32bcfb0ba17fa7ffb))

## [1.8.1](https://github.com/engeir/volcano-base/compare/v1.8.0...v1.8.1) (2024-03-22)


### Bug Fixes

* **time series:** expose subtract_climatology to the manipulate module ([1d48f98](https://github.com/engeir/volcano-base/commit/1d48f98ae91677221ce576c63d834414627041f8))

## [1.8.0](https://github.com/engeir/volcano-base/compare/v1.7.0...v1.8.0) (2024-03-22)


### Features

* **time series:** add subtract_climatology function ([5a70b59](https://github.com/engeir/volcano-base/commit/5a70b59b3f4b234fc48b94c73b70955e74a71563))


### Miscellaneous

* **docs:** fix docstrings in subtract_climatology ([7e689e6](https://github.com/engeir/volcano-base/commit/7e689e6091231d71d728e157530d6df7c6a171d7))

## [1.7.0](https://github.com/engeir/volcano-base/compare/v1.6.2...v1.7.0) (2024-03-21)


### Features

* **down:** add RF control to downloadable datasets (FSNTOA) ([8566ec9](https://github.com/engeir/volcano-base/commit/8566ec955593f19aaf1bd8aac1aa621fee25b57f))

## [1.6.2](https://github.com/engeir/volcano-base/compare/v1.6.1...v1.6.2) (2024-03-19)


### Documentation

* **time series:** refine warning message in `shift_arrays` ([100bcc0](https://github.com/engeir/volcano-base/commit/100bcc07e8c6e21c3080ec37efa92d48fb766a95))

## [1.6.1](https://github.com/engeir/volcano-base/compare/v1.6.0...v1.6.1) (2024-03-15)


### Bug Fixes

* **time series:** expose approx_aligned to main module ([27399e1](https://github.com/engeir/volcano-base/commit/27399e14159419838acad1b5d6b143e63bd2d28e))

## [1.6.0](https://github.com/engeir/volcano-base/compare/v1.5.1...v1.6.0) (2024-03-15)


### Features

* **time series:** adds approx_align function ([5b82d25](https://github.com/engeir/volcano-base/commit/5b82d25a75f13938f2efc125c24e88b3833be14a))


### Code Refactoring

* **load:** loop inside list extend ([3d759f8](https://github.com/engeir/volcano-base/commit/3d759f8ebf4c42bda6db2b2757a6890ebf1e169b))

## [1.5.1](https://github.com/engeir/volcano-base/compare/v1.5.0...v1.5.1) (2024-03-13)


### Bug Fixes

* **ob16:** apply groupby operation from variable, not string ([397fb83](https://github.com/engeir/volcano-base/commit/397fb83cc394119fb33357a9d598463cd959d93f))

## [1.5.0](https://github.com/engeir/volcano-base/compare/v1.4.4...v1.5.0) (2024-03-12)


### Features

* **cesm2:** implement functions that download NIRD archive ([35c1955](https://github.com/engeir/volcano-base/commit/35c1955036542fccf4d3d03098c008d5ccd8e689))


### Miscellaneous

* **deps:** bump pypa/gh-action-pypi-publish from 1.8.12 to 1.8.14 ([#64](https://github.com/engeir/volcano-base/issues/64)) ([58e3b17](https://github.com/engeir/volcano-base/commit/58e3b17fb324871c73cfc6eb055d14955139e78c))
* **FindFiles:** add __repr__ ([86b33bf](https://github.com/engeir/volcano-base/commit/86b33bff39b3ba926ff54637536fefa048d93ee3))

## [1.4.4](https://github.com/engeir/volcano-base/compare/v1.4.3...v1.4.4) (2024-03-08)


### Bug Fixes

* **ob16:** remove climatology from the control temperature ([fd87b01](https://github.com/engeir/volcano-base/commit/fd87b01deee2ad74db03dd6715d672027d55d0b1))

## [1.4.3](https://github.com/engeir/volcano-base/compare/v1.4.2...v1.4.3) (2024-03-08)


### Bug Fixes

* **ob16:** expose the temperature control signal as a class attribute ([d0f6a19](https://github.com/engeir/volcano-base/commit/d0f6a19b8ae03ea24d5a8d624f35940627db02c8))

## [1.4.2](https://github.com/engeir/volcano-base/compare/v1.4.1...v1.4.2) (2024-03-06)


### Code Refactoring

* **ob16:** move warning about peak finding to where this is done ([265a922](https://github.com/engeir/volcano-base/commit/265a9228056b2cdf85ffdfbb667ccb6e33d1b58a))


### Continuous Integration

* **github:** go back to using release-please-action v3 ([ffd74f2](https://github.com/engeir/volcano-base/commit/ffd74f204d66ab8da225d139b4e5bcc25b760a53))

## [1.4.1](https://github.com/engeir/volcano-base/compare/v1.4.0...v1.4.1) (2024-03-06)


### Bug Fixes

* **ob16:** so2 start one index (month) earlier ([539cf70](https://github.com/engeir/volcano-base/commit/539cf700cbdf66640119f92ee8b721cd8a1cce4b))

## [1.4.0](https://github.com/engeir/volcano-base/compare/v1.3.0...v1.4.0) (2024-03-06)


### Features

* **time series:** add weighted_month_mean ([f4a9a94](https://github.com/engeir/volcano-base/commit/f4a9a94b980d5b8c5304460dc6d3800026665614))


### Bug Fixes

* **ob16:** incorrectly assigned SO2 RF-aligned to SO2 temp-aligned ([c7587b7](https://github.com/engeir/volcano-base/commit/c7587b7d461f4d008b1f151ee9a6874fbbe04a77))
* **ob16:** re-align arrays for monthly data ([2913bc1](https://github.com/engeir/volcano-base/commit/2913bc1d9f4f28488fdf7fb34c9565f9c5f92920))


### Documentation

* **time_series:** improve docstring for sampling_rate function ([3378404](https://github.com/engeir/volcano-base/commit/33784043f364eac0eb707119ec7929590eda41a4))

## [1.3.0](https://github.com/engeir/volcano-base/compare/v1.2.1...v1.3.0) (2024-03-05)


### Features

* **ob16:** remove xr.align in favour of normal slice ([e6f71e9](https://github.com/engeir/volcano-base/commit/e6f71e93f3b5c7d4908f070260048c3a1a402446))

## [1.2.1](https://github.com/engeir/volcano-base/compare/v1.2.0...v1.2.1) (2024-03-04)


### Bug Fixes

* **ob16:** must consider that SO2 original is only in monthly resolution ([549d1a4](https://github.com/engeir/volcano-base/commit/549d1a455e99e167626d17118eaeb00c5ff51cb2))

## [1.2.0](https://github.com/engeir/volcano-base/compare/v1.1.0...v1.2.0) (2024-03-04)


### Features

* **ob16:** add SO2 decay to aligned arrays ([278bfaa](https://github.com/engeir/volcano-base/commit/278bfaae9ffcaef5d6d942f7021f178520c0e1b8))


### Bug Fixes

* **ob16:** progress file load should not use length to all files ([2e0c044](https://github.com/engeir/volcano-base/commit/2e0c044319f5f6686430dba4d89dccf010d117aa))

## [1.1.0](https://github.com/engeir/volcano-base/compare/v1.0.0...v1.1.0) (2024-03-04)


### Features

* **ob16:** add an optional progress bar when loading data ([d4b253d](https://github.com/engeir/volcano-base/commit/d4b253d6e7b7cf9c789e6720d0277271386ff80a))

## [1.0.0](https://github.com/engeir/volcano-base/compare/v0.8.6...v1.0.0) (2024-03-01)


### ⚠ BREAKING CHANGES

* **ob16:** rewrite into a class ([#53](https://github.com/engeir/volcano-base/issues/53))

### Code Refactoring

* **ob16:** rewrite into a class ([#53](https://github.com/engeir/volcano-base/issues/53)) ([aac6001](https://github.com/engeir/volcano-base/commit/aac600170551712bb75fdc0eb917d3e580c4befe))

## [0.8.6](https://github.com/engeir/volcano-base/compare/v0.8.5...v0.8.6) (2024-02-16)


### Bug Fixes

* **ci:** use rye directly, via mise did not work ([082989c](https://github.com/engeir/volcano-base/commit/082989c95f85994638dd251a8a923582ea66bd94))

## [0.8.5](https://github.com/engeir/volcano-base/compare/v0.8.4...v0.8.5) (2024-02-16)


### Bug Fixes

* **manipulate:** add sample_rate function as entry point in module ([d4e9995](https://github.com/engeir/volcano-base/commit/d4e99957d109db22b8a228105dfc31e185a16802))

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
