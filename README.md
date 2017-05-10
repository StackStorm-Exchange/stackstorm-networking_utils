# Networking Utils Pack

This is a pack of useful networking utilities to use in workflows for
validation and flow control.

## Configuration

Configuration is only required is if you want to place the GeoIP2
databases in a different location from the default.

```yaml
---
isp_db: "/path/to/GeoIP2-ISP.mmdb"
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

To use the `geoip` action you need to download one at least one of the
following databases:

- The (GeoLite2 City)[http://dev.maxmind.com/geoip/geoip2/geolite2/] (licensed under CC BY-SA 4.0) database.
- The paid (City)[https://www.maxmind.com/en/geoip2-city] database.
- The paid (ISP)[https://www.maxmind.com/en/geoip2-isp-database] database.
- The (GeoLite2 ASN)[http://dev.maxmind.com/geoip/geoip2/geolite2/] (licensed under CC BY-SA 4.0) database.

And place into `/opt/geoip2/` or if you install elsewhere you'll need
to create a config file with the paths.

Currently only the _City_, _ASN_ or_ISP_ databases supported.
