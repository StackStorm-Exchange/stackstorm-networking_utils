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
    def run(self, ip_address):
        """
        Return GeoIP information about an IP address

        Args:
        - ip_address: The IP address to validate.

        Raises:
        - ValueError: On invalid database.

        Returns:
        - dict: With GeoIP information about the IP address.
        """

        results = {"ok": False}

        # As ipaddress is a backport from Python 3.3+ it errors if the
        # ip address is a string and not unicode.
        try:
            ip_obj = ipaddress.ip_address(unicode(ip_address))
        except ValueError:
            results['error'] = "Invalid IP"
            return results

        if ip_obj.is_private:
            results['error'] = "Can't geoup a Private IP"
            return results

        results['ip_address'] = ip_address

        if self.config.isp_enable:
            reader_isp = geoip2.database.Reader(self.config.isp_db)
            response = reader_isp.isp(ip_address)

            results['as_num'] = response.autonomous_system_number
            results['as_org'] = response.autonomous_system_organization
            results['isp'] = response.isp
            results['org'] = response.organization

            reader_isp.close()

        if self.config.city_enable:
            reader_city = geoip2.database.Reader(self.config.city_db)
            response = reader_city.city(ip_address)

            results['city'] = response.city.name
            results['country'] = response.country.name
            results['latitude'] = response.location.latitude
            results['longitude'] = response.location.longitude

            results['google_maps'] = "http://maps.google.com/maps/place/{name}/@{lat},{lon},{z}z".format(  # NOQA
                name=ip_address,
                z=10,
                lat=results['latitude'],
                lon=results['longitude'])

            reader_city.close()

        return results
