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


class FakeASN(object):

    @property
    def autonomous_system_number(self):
        return 12345

    @property
    def autonomous_system_organization(self):
        return "Google"


class FakeISPReader(object):
    def isp(self, ip_address):
        return FakeISP()

    def close(self):
        return True


class FakeASNReader(object):
    def asn(self, ip_address):
        return FakeASN()

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
        expected = {"geoip": {},
                    "error": "No GeoIP2 databases"}
        action = self.get_action_instance(self.full_config)

        (status, result) = action.run(ip_addresses=["192.168.1.1"])
        self.assertFalse(status)
        self.assertEqual(result, expected)

    def test_run_invalid_ip(self):
        self.maxDiff = None

        expected = {
            "geoip": {
                "Not_an_IP": {
                    "error": {
                        "name": "Error",
                        "value": "Invalid IP: u'Not_an_IP' does not appear to be an IPv4 or IPv6 address"  # NOQA
                    }
                }
            }
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeASNReader(),
                                                        FakeCityReader()])

        (status, result) = action.run(ip_addresses=["Not_an_IP"])
        self.assertTrue(status)
        self.assertEqual(result, expected)

    def test_run_invalid_private_ip(self):
        self.maxDiff = None

        expected = {
            "geoip": {
                "192.168.1.1": {
                    "error": {
                        'name': "Error",
                        'value': "Private IP"
                    }
                }
            }
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeASNReader(),
                                                        FakeCityReader()])

        (status, result) = action.run(ip_addresses=["192.168.1.1"])
        self.assertTrue(status)
        self.assertEqual(result, expected)

    def test_run_google_lookup(self):
        self.maxDiff = None

        expected = {
            "geoip": {
                "8.8.8.8": {
                    'as_num': {'name': "AS Number",
                               'value': 12345
                    },
                    'as_org': {'name': "AS Org",
                               'value': "Google"
                    },
                    'isp': {'name': "ISP",
                            'value': "Google"
                    },
                    'org': {'name': "Org",
                            'value': "Google"
                    },
                    'city': {'name': "City",
                             'value': "London"
                    },
                    'country': {'name': "Country",
                                'value': "UK"
                    },
                    'lat': {'name': "Lat",
                            'value': 1.0
                    },
                    'lon': {'name': "Lon",
                            'value': 1.0
                    },
                    'link': {'name': "Google Map",
                             'value': 'https://maps.google.com/maps/place//@1.0,1.0,10z'  # NOQA
                    }
                },
                "8.8.4.4": {
                    'as_num': {'name': "AS Number",
                               'value': 12345
                    },
                    'as_org': {'name': "AS Org",
                               'value': "Google"
                    },
                    'isp': {'name': "ISP",
                            'value': "Google"
                    },
                    'org': {'name': "Org",
                            'value': "Google"
                    },
                    'city': {'name': "City",
                             'value': "London"
                    },
                    'country': {'name': "Country",
                                'value': "UK"
                    },
                    'lat': {'name': "Lat",
                            'value': 1.0
                    },
                    'lon': {'name': "Lon",
                            'value': 1.0
                    },
                    'link': {'name': "Google Map",
                             'value': 'https://maps.google.com/maps/place//@1.0,1.0,10z'  # NOQA
                    }
                }
            }
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[FakeISPReader(),
                                                        FakeASNReader(),
                                                        FakeCityReader()])

        (status, result) = action.run(ip_addresses=["8.8.8.8", "8.8.4.4"])
        self.assertTrue(status)
        self.assertEqual(result, expected)

    def test_run_asn_google_lookup(self):
        self.maxDiff = None

        expected = {
            "geoip": {
                "8.8.8.8": {
                    'as_num': {'name': "AS Number",
                               'value': 12345
                    },
                    'as_org': {'name': "AS Org",
                               'value': "Google"
                    },
                    'city': {'name': "City",
                             'value': "London"
                    },
                    'country': {'name': "Country",
                                'value': "UK"
                    },
                    'lat': {'name': "Lat",
                            'value': 1.0
                    },
                    'lon': {'name': "Lon",
                            'value': 1.0
                    },
                    'link': {'name': "Google Map",
                             'value': 'https://maps.google.com/maps/place//@1.0,1.0,10z'  # NOQA
                    }
                },
                "8.8.4.4": {
                    'as_num': {'name': "AS Number",
                               'value': 12345
                    },
                    'as_org': {'name': "AS Org",
                               'value': "Google"
                    },
                    'city': {'name': "City",
                             'value': "London"
                    },
                    'country': {'name': "Country",
                                'value': "UK"
                    },
                    'lat': {'name': "Lat",
                            'value': 1.0
                    },
                    'lon': {'name': "Lon",
                            'value': 1.0
                    },
                    'link': {'name': "Google Map",
                             'value': 'https://maps.google.com/maps/place//@1.0,1.0,10z'  # NOQA
                    }
                }
            }
        }
        action = self.get_action_instance(self.full_config)
        action._get_databases = MagicMock(return_value=[None,
                                                        FakeASNReader(),
                                                        FakeCityReader()])

        (status, result) = action.run(ip_addresses=["8.8.8.8", "8.8.4.4"])
        self.assertTrue(status)
        self.assertEqual(result, expected)
