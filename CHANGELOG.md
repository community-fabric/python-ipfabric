# Changelog

## 6.0.0 (2022-10-XX)

### Breaking Change

* Snapshot model has changed to use POST which contains more metadata
* GET is still used currently for some missing data
* Initializing of the IPFClient will only get loaded snapshots by default to
  reduce memory as some customers can have over 100 unloaded snapshots

### Feature

* Updates for v6.0
* Will only initialize loaded only snapshots unless `unloaded=True`
* Update Dev Dependencies
* Update for AWS API for multiple regions/AssumeRoles
* Add Lock/Unlock snapshots
* Added get_snapshot(snapshot_id) to find a snapshot_id
* Added Local Attributes
* Added Jobs

### CI/CD

* Do not run functional tests for beta release

## 5.0.16 (2022-11-07)

### Fix

* Fix for the URL formatter.

## 5.0.15 (2022-10-05)

### Feature

* Added ipfabric.settings.SiteSeparation
* Removed ipfabric.tools.UpdateSiteNames as this was removed in 4.4
* Added ipfabric.tools.site_seperation_report.map_devices_to_rules
* See [site_separation_tester.py](examples/tools/site_separation_report.py)

## 5.0.14 (2022-10-04)

### Feature

* Added shared tools for parsing MAC addresses and return IP Fabric Format
* Added examples for parsing MAC and Timestamps.

## 5.0.13 (2022-10-03)

### Feature

* Added tools for Discovery History table

## 5.0.11 (2022-09-20)

### Fix

* Poetry Update

### CI/CD

* Add community-fabric Slack notification

## 5.0.11 (2022-09-20)

### Fix

* Final fix for SSL verification

## 5.0.10 (2022-09-12)

### Feature

* added the ability to add custom loggers
* add python-json-logger to poetry optional dependencies

## 5.0.9 (2022-09-09)

### Fix

* Removed pkg_resources as it was causing some issues on certain OS and Python
  versions
* Updated poetry-core

### CI

* Added more python versions to functional testing.

## 5.0.8 (2022-09-08)

### Fix

* Update python-dontenv

## 5.0.7 (2022-09-07)

### Fix

* Fix for httpx timeout

## 5.0.6 (2022-09-01)

### Fix

* Fix for unverified cert

## 5.0.5 (2022-08-17)

### Fix

* Fix in user/pass auth

## 5.0.4 (2022-08-17)

### Fix

* Fix in Users model
* Added get_user to get information about logged in user during init
* Added count function to tables

## 5.0.3 (2022-08-11)

### Fix

* Deprecate IPF v4.X from package
* Added Technologies to the SDK
* Verification of API Version against IP Fabric Version

## 5.0.2 (2022-08-09)

### Fix

* Remove `importlib-metadata` dependency

## 5.0.1 (2022-07-13)

### Fix

* Do not use count for paging results do to some tables not returning a count.

## 5.0.0 (2022-07-13)

### Feature

* Update package to be compatible with v5.0.0
* Added tools.RestoreIntents which will restore Intents, Groups, & Dashboard
  from a file, another instance, or factory default
* Added all inventory endpoints to inventory (phones, fans, modules,
  powerSupplies, powerSuppliesFans)
* Allow initialization without loaded snapshots
* Added IPFClient.loaded_snapshots and IPFClient.unloaded_snapshots
* Added a Load and Unload snapshot function to Snapshot
  model `ipf.snapshots['ea0da479-6222-4cf6-a0ae-78a610669477'].load(ipf)`
* Added ability to get attributes for a
  snapshot `attributes = ipf.snapshots['$last'].attributes(ipf)`

## 4.4.3 (2022-06-22)

### Feature

* Add get_count function

### CI

* Remove semantic-release and updated GH Actions

## v0.11.0 (2022-05-25)

### Feature

* Add username/password
  auth ([`4ae04aa`](https://github.com/community-fabric/python-ipfabric/commit/4ae04aab72f1caa1de897ded32d44c9dd01fd187))
* Add username/password
  auth ([`420b6b1`](https://github.com/community-fabric/python-ipfabric/commit/420b6b17b9c0f9c982acf192ead1bf9f9a374dfc))

## v0.10.8 (2022-04-22)

### Fix

* Test discord
  webhook ([`07c04dd`](https://github.com/community-fabric/python-ipfabric/commit/07c04dd7ec646bb509fc0c580561f4318fdb8374))

## v0.10.7 (2022-04-21)

### Fix

* Update
  docs ([`47049fe`](https://github.com/community-fabric/python-ipfabric/commit/47049fecc5b8bfae151a3b7aabb999e9da685270))

## v0.10.6 (2022-04-21)

### Fix

* Update
  packages ([`8ff5efc`](https://github.com/community-fabric/python-ipfabric/commit/8ff5efcdc4e03d69e64daecc39f9cac48a91f062))

## v0.10.5 (2022-04-21)

### Fix

* Update
  release ([`0fb2627`](https://github.com/community-fabric/python-ipfabric/commit/0fb262789f345ac916235a3457c696e6ecbff62f))
* Update
  release ([`ad00fbd`](https://github.com/community-fabric/python-ipfabric/commit/ad00fbdffbb78eb52b617fd4f49214a377a43acf))

## v0.10.4 (2022-04-21)

### Fix

* Update
  release ([`79e5d0d`](https://github.com/community-fabric/python-ipfabric/commit/79e5d0dc640565b850ba4f89abc49bd9d11cc598))
* Update
  release ([`f2a3079`](https://github.com/community-fabric/python-ipfabric/commit/f2a30799c9e502dd046e978df49de8ddd136b59b))
* Update
  release ([`ba6b599`](https://github.com/community-fabric/python-ipfabric/commit/ba6b599ef54584cdea75a1df3ad3198bfd25a5ba))

## v0.10.3 (2022-04-21)

### Fix

* Update
  release ([`a6fec0c`](https://github.com/community-fabric/python-ipfabric/commit/a6fec0c2fcd3f5a0cd9c7f8bf63d753a6457312d))

## v0.10.2 (2022-04-21)

### Fix

* Update
  black ([`baafd60`](https://github.com/community-fabric/python-ipfabric/commit/baafd607b8e28eb1e0791bc779581064b44323e7))
* Test adding
  vulnerabilities ([`ff0fda1`](https://github.com/community-fabric/python-ipfabric/commit/ff0fda1ae7b27422c147a06047989d41ddee3bdd))
* Config
  again ([`6b3fac9`](https://github.com/community-fabric/python-ipfabric/commit/6b3fac9360831f84224a84083c4e89fe22e4c848))
* Poetry
  update ([`24ca2e9`](https://github.com/community-fabric/python-ipfabric/commit/24ca2e98257531465349e672efc019b11d055031))
* Remove graphing and security as these do not work in v4.3 and
  above. ([`a7b3b35`](https://github.com/community-fabric/python-ipfabric/commit/a7b3b353edf8b1f8df222b12778755df441c6a0c))

## v0.10.1 (2022-04-21)

### Fix

* Updates to fix configs in IPF
  v4.4.1 ([`da3e0b8`](https://github.com/community-fabric/python-ipfabric/commit/da3e0b8241bfd36b57edb6bf3c5ac5066d4fc8b2))

## v0.10.0 (2022-04-21)

### Feature

* Updates to fix configs in IPF
  v4.4.1 ([`fde1016`](https://github.com/community-fabric/python-ipfabric/commit/fde1016c24132c0b503bd5235fa73761c8a45814))

## v0.9.0 (2022-03-23)

### Feature

* Add Vendor API
  Settings. ([`f624a83`](https://github.com/community-fabric/python-ipfabric/commit/f624a834f8d10133c5d03832659cdf30a0312fe2))

## v0.8.9 (2022-03-08)

### Fix

* Run poetry
  update ([`af4ac25`](https://github.com/community-fabric/python-ipfabric/commit/af4ac25119bc0913cb6b15b18eb625a44e466a16))
* Added hosts to
  inventory ([`0c65728`](https://github.com/community-fabric/python-ipfabric/commit/0c657281bb312f24f90bfc95e586419ae6f81c25))

## v0.8.8 (2022-03-03)

### Fix

* Updated NIST search for arista and change unsupported vendors to
  error ([`b603b13`](https://github.com/community-fabric/python-ipfabric/commit/b603b13c30d3b5d7d99c16feab8c63511de262d5))
*
Tests ([`4e57786`](https://github.com/community-fabric/python-ipfabric/commit/4e577866780e037e5adf6941d17c38fe25d59440))

## v0.8.7 (2022-02-24)

### Fix

*
Pager ([`e96ebda`](https://github.com/community-fabric/python-ipfabric/commit/e96ebda2202f8b5eb568ea8c9e22eaf299731ad6))

## v0.8.6 (2022-02-24)

### Fix

* Log
  name. ([`bfa1722`](https://github.com/community-fabric/python-ipfabric/commit/bfa1722760d37b671fc2f8dc5a459eec5e8eb636))
* Log
  name. ([`c3fda38`](https://github.com/community-fabric/python-ipfabric/commit/c3fda38f9ef41991328240ea237c84756a8d396d))

## v0.8.5 (2022-02-23)

### Fix

* Verify was not
  working. ([`58e7b34`](https://github.com/community-fabric/python-ipfabric/commit/58e7b349395ccb124a918f7b20ef18cc15d6a619))

## v0.8.4 (2022-02-18)

### Fix

* Get device
  logs ([`dfd7a33`](https://github.com/community-fabric/python-ipfabric/commit/dfd7a334b0249e202695e02cc3df53dfef120035))

## v0.8.3 (2022-02-18)

### Fix

* Device
  configs ([`a3b2d66`](https://github.com/community-fabric/python-ipfabric/commit/a3b2d66ba17504acccaa246f73aadebee4d79aed))

## v0.8.2 (2022-02-16)

### Fix

* Security
  tests ([`59b4870`](https://github.com/community-fabric/python-ipfabric/commit/59b4870e9d15fc90c0cc88af89d0fb3644362f0e))
* Sitename snapshot for
  v4.3 ([`c033b9b`](https://github.com/community-fabric/python-ipfabric/commit/c033b9bf47d60310874977ec0f8a3a32c21b4823))

## v0.8.1 (2022-02-10)

### Fix

* Added poetry extras to run
  examples. ([`f89d6f9`](https://github.com/community-fabric/python-ipfabric/commit/f89d6f9ad5cc39fb8bc5b7f95949f7a8d8bfcc67))
* Config is now using Serial Number as unique identifier not
  hostname ([`fd18a7d`](https://github.com/community-fabric/python-ipfabric/commit/fd18a7d7c6b821620d606aef61af5d5c029ad4dc))
* Update
  readme ([`b8bac4e`](https://github.com/community-fabric/python-ipfabric/commit/b8bac4e99f2537ee87fd03b50dac163fa2cc667c))
* Remove v4.3 diagrams and added back
  examples ([`76f0952`](https://github.com/community-fabric/python-ipfabric/commit/76f095202fc749fbce6f26a6a9d39ef5dd9c5394))

### Documentation

* Added examples for Intent
  Reporting ([`8f425d3`](https://github.com/community-fabric/python-ipfabric/commit/8f425d330c53d995be3e93fc360a842fae785525))

## v0.8.0 (2022-02-08)

### Feature

* Remove Python
  3.6 ([`1d8e6ea`](https://github.com/community-fabric/python-ipfabric/commit/1d8e6ea192d23397ca08bd9b0303e8f6a0923039))

### Fix

* Add example requirements as
  optional ([`5434eb4`](https://github.com/community-fabric/python-ipfabric/commit/5434eb42bcc31e3311f3c478e375a0cfe00ec89a))

## v0.7.18 (2022-02-02)

### Fix

*
Slack ([`43203ac`](https://github.com/community-fabric/python-ipfabric/commit/43203ac47aa1e609be961a51d8378c7078a0755e))

## v0.7.0 (2022-02-01)

### Feature

* Graphs will be removed in next breaking
  release ([`7e39f9b`](https://github.com/community-fabric/python-ipfabric/commit/7e39f9be2be5c277e191de25cae25a52a929a8c4))

## v0.6.0 (2022-01-31)

### Feature

* Run
  black ([`dce4a1a`](https://github.com/community-fabric/python-ipfabric/commit/dce4a1a6c2cc3a0a3eab857c18572d961b9456b4))
* Added port syntax
  checking ([`7453b8e`](https://github.com/community-fabric/python-ipfabric/commit/7453b8e71e167ad391d35a8ee221f4ef85147558))
* Simplified Constant
  parameters. ([`652ed29`](https://github.com/community-fabric/python-ipfabric/commit/652ed291908a575a3463f790466060a81c5db470))
* Remove grouping as users only use
  siteName. ([`175043b`](https://github.com/community-fabric/python-ipfabric/commit/175043b5d7b2014580ef82e0e6fb27f6ac8005fc))
* Updated v4.3 graphing with
  tests. ([`b0a56e3`](https://github.com/community-fabric/python-ipfabric/commit/b0a56e3630ef9d8fcee1d7ff200dda36a549be64))
* Updates for v4.3
  diagrams ([`f002d91`](https://github.com/community-fabric/python-ipfabric/commit/f002d91ba65c213f4949e5ae777fbf4bdc7d79aa))
* V4.3
  diagrams ([`4fb3082`](https://github.com/community-fabric/python-ipfabric/commit/4fb308208381adeb58362dfcc5f8a68d9cc1ba25))

## v0.5.0 (2022-01-27)

### Feature

* Added
  black ([`b4f3de4`](https://github.com/community-fabric/python-ipfabric/commit/b4f3de4ae8b9bf09eead334b3c1e451115b82091))

### Documentation

* Updated
  README ([`89eac20`](https://github.com/community-fabric/python-ipfabric/commit/89eac2004df0f51f272baf562da38bc4549d6424))

## v0.4.9 (2022-01-21)

### Fix

* CVE
  nx-os ([`7e47df8`](https://github.com/community-fabric/python-ipfabric/commit/7e47df8c999551fcaaa2e68d3e819d66078c8236))

## v0.4.8 (2022-01-21)

### Fix

* CVE
  nx-os ([`fb58d6a`](https://github.com/community-fabric/python-ipfabric/commit/fb58d6aee472502a743d62dec08ace3c2671e673))

## v0.4.7 (2022-01-21)

### Fix

* CVE
  searches ([`7ca91d4`](https://github.com/community-fabric/python-ipfabric/commit/7ca91d44d3f3c426f634b9021af5497b25e5f7b2))

## v0.4.6 (2022-01-14)

### Fix

* CVE URL
  data ([`41762bc`](https://github.com/community-fabric/python-ipfabric/commit/41762bc2e0321e981e77c8158161261a8f336c8b))

## v0.4.5 (2022-01-13)

### Fix

* Default pagination limit. Was told 10k was not great for
  performance ([`edd5ae4`](https://github.com/community-fabric/python-ipfabric/commit/edd5ae432fa4cce73c5b1170f7e992bb1cad73cc))

## v0.4.4 (2022-01-12)

### Fix

* Intent
  descriptions ([`25d6c96`](https://github.com/community-fabric/python-ipfabric/commit/25d6c96eccfb6c105bed891107dfb8cedc8580fd))

## v0.4.3 (2022-01-05)

### Fix

* Snapshot
  model ([`864d4c9`](https://github.com/community-fabric/python-ipfabric/commit/864d4c99e0acc3880cbaa56430e10b701ba768d8))

## v0.4.2 (2022-01-04)

### Fix

* CVE for
  hashing ([`6e81c94`](https://github.com/community-fabric/python-ipfabric/commit/6e81c9416c36213903895606a8ebe2d50408e549))

## v0.4.1 (2022-01-04)

### Fix

* CVE for
  descriptions ([`c805e99`](https://github.com/community-fabric/python-ipfabric/commit/c805e99a766e9b22879c52f99cac24103c64fc13))
* CVE for
  descriptions ([`7302a8f`](https://github.com/community-fabric/python-ipfabric/commit/7302a8fb56b013506e28a1292b3a0fc320d8aa0a))
* CVE for
  descriptions ([`4353106`](https://github.com/community-fabric/python-ipfabric/commit/4353106d9fa852371df16a4c69eb0c012bfc32bb))

## v0.4.0 (2021-12-30)

### Feature

* Added .env support and reworked environment
  variables ([`dc7b7f9`](https://github.com/community-fabric/python-ipfabric/commit/dc7b7f9011c4251bbf4e8caacc00795ee37271eb))

### Fix

* Dont
  env ([`b872bd3`](https://github.com/community-fabric/python-ipfabric/commit/b872bd3bc1f7f219a7557e5161b26034d8bbfe43))

## v0.3.2 (2021-12-21)

### Fix

*
Tests ([`b49e7fb`](https://github.com/community-fabric/python-ipfabric/commit/b49e7fb60e8bb13499d96d39e0c6f54079814254))
*
Tests ([`1e04368`](https://github.com/community-fabric/python-ipfabric/commit/1e04368975185a38054f3cd9ead0e07191fe1ac2))
*
CVE ([`87c7d7e`](https://github.com/community-fabric/python-ipfabric/commit/87c7d7efae9be6d72a9bf9769a2a4d8d4e11915d))
* Intent comparison name
  changes ([`1059227`](https://github.com/community-fabric/python-ipfabric/commit/105922748eaf7cff38e5fb5afa42b9b3d409429f))
* Intent comparison name
  changes ([`7439482`](https://github.com/community-fabric/python-ipfabric/commit/7439482a85727f7feba0c85480dedcfb091f912b))

### Documentation

* Added compare intent
  docs. ([`f8ee33d`](https://github.com/community-fabric/python-ipfabric/commit/f8ee33d786bdb6bf1e9604812886f41899ad5efa))

## v0.3.1 (2021-12-16)

### Fix

* Added reverse to intent compare and some more
  explanations ([`fe26b3f`](https://github.com/community-fabric/python-ipfabric/commit/fe26b3f1955f30285c9390c70264b9785a336cfb))

## v0.3.0 (2021-12-08)

### Feature

* Pull builtin checks from IP
  Fabric ([`0f4d385`](https://github.com/community-fabric/python-ipfabric/commit/0f4d3853c7b7313c0d60953f8ccc0b9bf2ab6217))

### Fix

* Fix graphing a site(
  s) ([`1df418e`](https://github.com/community-fabric/python-ipfabric/commit/1df418ed34b87e60340faecb6c2790d46b026eac))

## v0.2.4 (2021-12-08)

### Fix

* Fix for
  usermgmt ([`7777dc8`](https://github.com/community-fabric/python-ipfabric/commit/7777dc867398540cf9274badcd82129bbfb4b94c))

## v0.2.3 (2021-12-08)

### Fix

* Fix for snapshot missing
  version ([`d09b1b1`](https://github.com/community-fabric/python-ipfabric/commit/d09b1b1fb2daf147924690acd14f49446e4675ab))
* Fix for users by
  id ([`e5edaf7`](https://github.com/community-fabric/python-ipfabric/commit/e5edaf73a93cc50e175c46bb181a0336740f3360))

## v0.2.2 (2021-12-08)

### Fix

* Fix for unloaded
  snapshots ([`9aca3fd`](https://github.com/community-fabric/python-ipfabric/commit/9aca3fdb27a3f3a1a3dd4cbd4faad3417398048e))

## v0.2.1 (2021-12-07)

### Fix

* Added more data to
  snapshots ([`1f58a63`](https://github.com/community-fabric/python-ipfabric/commit/1f58a638edaddcfc588763558629412bcbfe07e1))

## v0.2.0 (2021-12-06)

### Feature

* Made comparison a
  dictionary ([`4b4258d`](https://github.com/community-fabric/python-ipfabric/commit/4b4258d6d19ceac6dc6e890b136a666d7b981818))
* Added a comparison for snapshot
  intents ([`b8028d5`](https://github.com/community-fabric/python-ipfabric/commit/b8028d5888726923a1f71f1642f15224e0b72a2d))
* Intent
  Checks ([`c606802`](https://github.com/community-fabric/python-ipfabric/commit/c6068028f972b00c57e24a63099f586f640eb0b2))

## v0.1.0 (2021-12-03)

### Feature

* Added
  Tokens ([`e0c4471`](https://github.com/community-fabric/python-ipfabric/commit/e0c4471588ac91f336d8e39d6e740aedb4bc34e4))

## v0.0.18 (2021-12-03)

### Fix

* Added log download to
  config ([`213baf2`](https://github.com/community-fabric/python-ipfabric/commit/213baf29b1b6314dca779cb63087547f2f3d0d11))

## v0.0.17 (2021-12-03)

### Fix

*
Test ([`fb941d8`](https://github.com/community-fabric/python-ipfabric/commit/fb941d81913cb984732f60af28f87f1c579a1c97))
*
Test ([`8be9b5d`](https://github.com/community-fabric/python-ipfabric/commit/8be9b5dd05ec290716ad2f46985bcf6329a68bd5))
*
Pipeline ([`4fcf5d1`](https://github.com/community-fabric/python-ipfabric/commit/4fcf5d1580bde480a13be6ff59148b2d969df41f))

## v0.0.16 (2021-12-02)

## v0.0.6 (2021-11-22)

### Fix

* Pipeline
  fixes. ([`5da0fd8`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/5da0fd8312d3d16047761c0a5ecae3717fa9fc2b))
* Pipeline
  fixes. ([`92ccba9`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/92ccba9c75d564b201d005ad29c855baef15555e))
* Pipeline
  fixes. ([`4b0fa7f`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/4b0fa7ffca27c242cc8a2a18fc610e3fcb054c75))
*
Pipeline ([`459c53d`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/459c53dd63f203b9f5970c25c10223637efcbee3))
*
Pipeline ([`c50b6b9`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/c50b6b99dbec6f3d9aa8bd3850dadeac9b7bcd43))
* Fix for running
  snapshots. ([`dda26f8`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/dda26f87e2cedc183b64c0d7020ec770f13bda92))
*
Workflow ([`6ca00f7`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/6ca00f7c9e8c9e5ea56cff234bd492d98891c576))
* Fix for
  releases ([`81ecb06`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/81ecb066a449dea196fc800cf0c828fde6707df2))
* For
  python3.8 ([`3092790`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/3092790bead16dc77d2eed97a4db53737270efa8))
* Github
  actions ([`15e55cb`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/15e55cbd5f41fa53663ed12d60f90951cb2c46cb))
* Github
  actions ([`412a790`](https://github.com/justinjeffery-ipf/python-ipfabric/commit/412a790d33689a73c8f5303920aab97781f30168))
