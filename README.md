# Networking Utils Pack

This is a pack of useful networking utilities to use in workflows for
validation and flow control.

# Actions.

- *is_valid_asa_ifname*: Check for an valid Cisco ASA interface name.
- *is_valid_ip*: Check if an valid IP (IPv4 or IPv6) address (with options to exclude loopback).
- *is_valid_ipv4*: Check if an valid IPv4 address (with options to exclude loopback).
- *is_valid_ipv6*: Check if an valid IPv6 address (with options to exclude loopback).
- *is_valid_ip_port*: Check if an valid IP port (i.e. between 0 and 65535).
- *geoip*: Report geoip infomation from MaxMind database(s).
- *ping*: Pings an IP address / Hostname.
- *traceroute_mtr*: Runs a traceroute (requires the mtr command to be available)
- *fping*: Runs a fping and return data about packet loss and latency (requires the fping to be available)
- *contains*: Check if an address or a network is in another network
- *resolve*: Resolve a DNS or reverse DNS

## GeoIP

To use the `geoip` action you require at least one of the following
MaxMind databases:

- **Free**
  - The (GeoLite2 City)[http://dev.maxmind.com/geoip/geoip2/geolite2/] (licensed under CC BY-SA 4.0) database.
  - The (GeoLite2 ASN)[http://dev.maxmind.com/geoip/geoip2/geolite2/] (licensed under CC BY-SA 4.0) database.
- **Commerical**
  - The paid (City)[https://www.maxmind.com/en/geoip2-city] database.
  - The paid (ISP)[https://www.maxmind.com/en/geoip2-isp-database] database.

It's possible to use either the ISP or ASN databases (if the
commerical ISP database is found the ASN is not used), these can be
used whether with or without the City database.

Currently only the _City_, _ASN_ or_ISP_ database types are supported
by the action.

## Configuration

Configuration is only required is if you want to place the GeoIP2
databases in a different location from the default (`/opt/geoip2/`)
you'll need to create a config file
(`/opt/stackstorm/config/networking_utils.yaml`) as follows (and don't
forget to load it) as follows:

```yaml
---
isp_db: "/path/to/GeoIP2-ISP.mmdb"
city_db: "/path/to/GeoLite2-City.mmdb"
asn_db: "/path/to/GeoLite2-ASN.mmdb"
```
