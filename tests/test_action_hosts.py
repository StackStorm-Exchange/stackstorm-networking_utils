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

from networking_utils_base_test_case import NetworkingUtilsBaseActionTestCase

from hosts import HostsAction

__all__ = ["HostsTestCase"]


class HostsTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = HostsAction

    def test_31_ipv4_network(self):
        expected = ["192.168.0.0", "192.168.0.1"]
        action = self.get_action_instance()

        result = action.run(network="192.168.0.0/31", family="ipv4")
        self.assertEqual(result, expected)

    def test_28_ipv4_network(self):
        expected = [
            "192.168.0.1",
            "192.168.0.2",
            "192.168.0.3",
            "192.168.0.4",
            "192.168.0.5",
            "192.168.0.6",
            "192.168.0.7",
            "192.168.0.8",
            "192.168.0.9",
            "192.168.0.10",
            "192.168.0.11",
            "192.168.0.12",
            "192.168.0.13",
            "192.168.0.14",
        ]

        action = self.get_action_instance()

        result = action.run(network="192.168.0.0/28", family="ipv4")
        self.assertEqual(result, expected)

    def test_127_ipv6_network(self):
        expected = ["2001:cafe::", "2001:cafe::1"]
        action = self.get_action_instance()

        result = action.run(network="2001:cafe::/127", family="ipv6")
        self.assertEqual(result, expected)

    def test_128_ipv6_network(self):
        expected = ["2001:cafe::1", "2001:cafe::2", "2001:cafe::3"]

        action = self.get_action_instance()

        result = action.run(network="2001:cafe::/126", family="ipv6")
        self.assertEqual(result, expected)
