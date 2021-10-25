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

from subnets import SubnetsAction

__all__ = ["SubnetsTestCase"]


class SubnetsTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = SubnetsAction

    def test_16_into_18_ipv4_networks(self):
        expected = ["192.168.0.0/18", "192.168.64.0/18", "192.168.128.0/18", "192.168.192.0/18"]

        action = self.get_action_instance()

        result = action.run(network="192.168.0.0/16", family="ipv4", new_prefix=18)
        self.assertEqual(result, expected)

    def test_24_into_29_ipv4_networks(self):
        expected = [
            "192.168.0.0/29",
            "192.168.0.8/29",
            "192.168.0.16/29",
            "192.168.0.24/29",
            "192.168.0.32/29",
            "192.168.0.40/29",
            "192.168.0.48/29",
            "192.168.0.56/29",
            "192.168.0.64/29",
            "192.168.0.72/29",
            "192.168.0.80/29",
            "192.168.0.88/29",
            "192.168.0.96/29",
            "192.168.0.104/29",
            "192.168.0.112/29",
            "192.168.0.120/29",
            "192.168.0.128/29",
            "192.168.0.136/29",
            "192.168.0.144/29",
            "192.168.0.152/29",
            "192.168.0.160/29",
            "192.168.0.168/29",
            "192.168.0.176/29",
            "192.168.0.184/29",
            "192.168.0.192/29",
            "192.168.0.200/29",
            "192.168.0.208/29",
            "192.168.0.216/29",
            "192.168.0.224/29",
            "192.168.0.232/29",
            "192.168.0.240/29",
            "192.168.0.248/29",
        ]

        action = self.get_action_instance()

        result = action.run(network="192.168.0.0/24", family="ipv4", new_prefix=29)
        self.assertEqual(result, expected)

    def test_60_into_64_ipv6_networks(self):
        expected = [
            "2001:cafe::/64",
            "2001:cafe:0:1::/64",
            "2001:cafe:0:2::/64",
            "2001:cafe:0:3::/64",
            "2001:cafe:0:4::/64",
            "2001:cafe:0:5::/64",
            "2001:cafe:0:6::/64",
            "2001:cafe:0:7::/64",
            "2001:cafe:0:8::/64",
            "2001:cafe:0:9::/64",
            "2001:cafe:0:a::/64",
            "2001:cafe:0:b::/64",
            "2001:cafe:0:c::/64",
            "2001:cafe:0:d::/64",
            "2001:cafe:0:e::/64",
            "2001:cafe:0:f::/64",
        ]

        action = self.get_action_instance()

        result = action.run(network="2001:cafe::/60", family="ipv6", new_prefix=64)
        self.assertEqual(result, expected)
