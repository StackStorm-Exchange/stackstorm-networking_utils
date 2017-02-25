# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ipaddress
import geoip2.database

from st2actions.runners.pythonrunner import Action


class GeoIpAction(Action):
    def _get_databases(self):
        """
        Try to open all the GeoIP2 databases we need.
        """

        try:
            reader_isp = geoip2.database.Reader(self.config['isp_db'])
        except IOError:
            reader_isp = None

        try:
            reader_city = geoip2.database.Reader(self.config['city_db'])
        except IOError:
            reader_city = None

        return (reader_isp, reader_city)

    def run(self, ip_addresses):
        """
        Return GeoIP information about an IP address

        Args:
        - ip_address: The IP address to validate.

        Raises:
        - ValueError: On invalid database.

        Returns:
        dict: with keys of IP address containing a dict of the
        GeoIP information.
        """

        results = {"ok": False, "geoip": {}}

        (reader_isp, reader_city) = self._get_databases()

        if reader_city is None and reader_isp is None:
            results['error'] = "No GeoIP2 databases"
            return results
        else:
            results["ok"] = True

        for ip_address in ip_addresses:
            details = {}

            # As ipaddress is a backport from Python 3.3+ it errors if the
            # ip address is a string and not unicode.
            try:
                ip_obj = ipaddress.ip_address(unicode(ip_address))
            except ValueError:
                results['geoip'][ip_address] = {'error': "Invalid IP"}
                continue

            if ip_obj.is_private:
                results['geoip'][ip_address] = {'error': "Private IP"}
                continue

            if reader_isp:
                response = reader_isp.isp(ip_address)

                details['AS Number'] = response.autonomous_system_number
                details['AS Org'] = response.autonomous_system_organization
                details['ISP'] = response.isp
                details['Org'] = response.organization

            if reader_city:
                response = reader_city.city(ip_address)

                details['City'] = response.city.name
                details['Country'] = response.country.name
                details['Lat'] = response.location.latitude  # NOQA pylint: disable=no-member
                details['Lon'] = response.location.longitude  # NOQA pylint: disable=no-member

                url = "maps.google.com/maps/place/"
                details['Google Maps'] = "https://{url}/maps/place/{name}/@{lat},{lon},{z}z".format(  # NOQA
                    url=url,
                    name=ip_address,
                    z=10,
                    lat=details['Lat'],
                    lon=details['Lon'])

            results['geoip'][ip_address] = details

        if reader_city:
            reader_city.close()

        if reader_isp:
            reader_isp.close()

        return results
