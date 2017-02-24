# Networking Utils Pack

This is a pack of useful networking utilities to use in workflows for
validation and flow control.

## Configuration

Configuration is only required for using the `geoip` action.

```yaml
---
isp_enable: true
isp_db: "/path/to/GeoIP2-ISP.mmdb"
city_enable: true
city_db: "/path/to/GeoLite2-City.mmdb"
```

# Actions.

- *is_valid_asa_ifname*: Check for an valid Cisco ASA interface name.
- *is_valid_ip*: Check if an valid IP (IPv4 or IPv6) address (with options to exclude loopback).
- *is_valid_ipv4*: Check if an valid IPv4 address (with options to exclude loopback).
- *is_valid_ipv6*: Check if an valid IPv6 address (with options to exclude loopback).
- *is_valid_ip_port*: Check if an valid IP port (i.e. between 0 and 65535).
- *geoip*: Report geoip infomation from MaxMind database(s).

## GeoIP

To use the `geoip` action you need to download either the _city_
(geolite2)[http://dev.maxmind.com/geoip/geoip2/geolite2/] (licensed
under CC BY-SA 4.0) database or the commerical
(City)[https://www.maxmind.com/en/geoip2-city] /
(ISP)[https://www.maxmind.com/en/geoip2-isp-database] databases and
then configure the paths to the databases in the configuration.


