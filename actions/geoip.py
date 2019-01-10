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

from st2common.runners.base_action import Action


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
            reader_asn = geoip2.database.Reader(self.config['asn_db'])
        except IOError:
            reader_asn = None

        try:
            reader_city = geoip2.database.Reader(self.config['city_db'])
        except IOError:
            reader_city = None

        return (reader_isp, reader_asn, reader_city)

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

        results = {"geoip": {}}
        status = False

        (reader_isp, reader_asn, reader_city) = self._get_databases()

        if reader_city is None and reader_isp is None and reader_asn is None:
            results['error'] = "No GeoIP2 databases"
            return (status, results)
        else:
            status = True

        try:
            for ip_address in ip_addresses:
                details = {}

                # As ipaddress is a backport from Python 3.3+ it errors if the
                # ip address is a string and not unicode.
                try:
                    ip_obj = ipaddress.ip_address(unicode(ip_address))
                except ValueError as e:
                    results['geoip'][ip_address] = {
                        'error': {'name': "Error",
                                  'value': "Invalid IP: {}".format(e)}
                    }
                    continue

                if ip_obj.is_private:
                    details['error'] = {'name': "Error",
                                        'value': "Private IP"}
                    results['geoip'][ip_address] = details
                    continue

                if reader_isp:
                    response = reader_isp.isp(ip_address)

                    details['as_num'] = {
                        'name': "AS Number",
                        'value': response.autonomous_system_number}
                    details['as_org'] = {
                        'name': "AS Org",
                        'value': response.autonomous_system_organization}
                    details['isp'] = {'name': "ISP",
                                      'value': response.isp}
                    details['org'] = {'name': "Org",
                                      'value': response.organization}
                elif reader_asn:
                    response = reader_asn.asn(ip_address)

                    details['as_num'] = {
                        'name': "AS Number",
                        'value': response.autonomous_system_number}
                    details['as_org'] = {
                        'name': "AS Org",
                        'value': response.autonomous_system_organization}

                if reader_city:
                    response = reader_city.city(ip_address)

                    details['city'] = {'name': "City",
                                       'value': response.city.name}
                    details['country'] = {'name': "Country",
                                          'value': response.country.name}
                    details['lat'] = {'name': "Lat",
                                      'value': response.location.latitude}  # NOQA pylint: disable=no-member
                    details['lon'] = {'name': "Lon",
                                      'value': response.location.longitude}  # NOQA pylint: disable=no-member

                    url = "maps.google.com"
                    details['link'] = {
                        'name': "Google Map",
                        'value': "https://{url}/maps/place//@{lat},{lon},{z}z".format(
                            url=url,
                            z=10,
                            lat=details['lat']['value'],
                            lon=details['lon']['value'])}

                results['geoip'][ip_address] = details
        except Exception:
            self.logger.error("Something went really wrong!")
            raise
        finally:
            if reader_city:
                reader_city.close()

            if reader_isp:
                reader_isp.close()

            if reader_asn:
                reader_asn.close()

        return (status, results)
