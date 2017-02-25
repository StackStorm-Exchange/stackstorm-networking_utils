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

from mock import MagicMock

from networking_utils_base_test_case import NetworkingUtilsBaseActionTestCase

from geoip import GeoIpAction

__all__ = [
    'GeoIpActionTestCase'
]


class FakeISP(object):

    @property
    def autonomous_system_number(self):
        return 12345

    @property
    def autonomous_system_organization(self):
        return "Google"

    @property
    def isp(self):
        return "Google"

    @property
    def organization(self):
        return "Google"


class FakeISPReader(object):
    def isp(self, ip_address):
        return FakeISP()

    def close(self):
        return True


class FakeCityName(object):
    @property
    def name(self):
        return "London"


class FakeCountry(object):
    @property
    def name(self):
        return "UK"


class FakeLocation(object):
    @property
    def latitude(self):
        return 1.0

    @property
    def longitude(self):
        return 1.0


class FakeCity(object):
    def __init__(self):
        self.city = FakeCityName()
        self.country = FakeCountry()
        self.location = FakeLocation()


class FakeCityReader(object):
    def city(self, ip_address):
        return FakeCity()

    def close(self):
        return True


class GeoIpActionTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = GeoIpAction

    def test_run_no_databases(self):
        expected = {"ok": False,
                    "geoip": {},
                    "error": "No GeoIP2 databases"}
        action = self.get_action_instance(self.full_config)

        result = action.run(ip_addresses=["192.168.1.1"])
        self.assertEqual(result, expected)

    def test_run_invalid_ip(self):
        expected = {
            "ok": True,
            "geoip": {"Not_an_IP": {"error": "Invalid IP"}}
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeCityReader()])

        result = action.run(ip_addresses=["Not_an_IP"])
        self.assertEqual(result, expected)

    def test_run_invalid_private_ip(self):
        expected = {
            "ok": True,
            "geoip": {"192.168.1.1": {"error": "Private IP"}}
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeCityReader()])

        result = action.run(ip_addresses=["192.168.1.1"])
        self.assertEqual(result, expected)

    def test_run_google_lookup(self):
        self.maxDiff = None
        expected = {
            "ok": True,
            "geoip": {
                "8.8.8.8": {
                    'AS Number': 12345,
                    'AS Org': "Google",
                    'ISP': "Google",
                    'Org': "Google",
                    'City': "London",
                    'Country': "UK",
                    'Lat': 1.0,
                    'Lon': 1.0,
                    'Google Maps': 'https://maps.google.com/maps/place//maps/place/8.8.4.4/@1.0,1.0,10z'  # NOQA
                },
                "8.8.4.4": {
                    'AS Number': 12345,
                    'AS Org': "Google",
                    'ISP': "Google",
                    'Org': "Google",
                    'City': "London",
                    'Country': "UK",
                    'Lat': 1.0,
                    'Lon': 1.0,
                    'Google Maps': 'https://maps.google.com/maps/place//maps/place/8.8.4.4/@1.0,1.0,10z'  # NOQA
                }
            }
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeCityReader()])

        result = action.run(ip_addresses=["8.8.8.8", "8.8.4.4"])
        self.assertEqual(result, expected)
