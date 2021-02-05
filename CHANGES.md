# Changelog

## 1.0.0

* Drop Python 2.7 support

## 0.6.0

- Minor fixups and improvements
- Pin geoip2 and maxminddb versions to ensure Python 2.7 compatibility
- Update `resolve` action to use `getaddrinfo` instead of `gethostbyname_ex`

## 0.5.0
- Added `contains` action
- Added `fping` action
- Added `resolve` action
- Added `traceroute_mtr` action

## 0.4.6
- Version bump to fix tagging issues

## 0.4.5
- Added `ping_py` action (using Python and option to force success).
- Update Jon Middleton's email in `CONTRIBUTORS.md`.

## 0.4.4
- Added `ping` action.

## 0.4.3
- Update authors email address.

## 0.4.2
- Minor linting

## 0.4.0
- Added `is_valid_hostname` action.

## 0.3.1
- Added example configuration file

## 0.3
- Add support for the GeoIP Lite ASN DB.
- Require geoip2 >= 2.5.0 for GeoIP Lite ASN support.

## 0.2
- Added `geoip` action and action alias.

## 0.1
- First release.
