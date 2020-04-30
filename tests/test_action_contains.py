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

from contains import Contains

__all__ = ["ContainsTestCase"]


class ContainsTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = Contains

    def test_contains_ip_in_network(self):
        action = self.get_action_instance()

        self.assertTrue(action.run("10.0.0.1", "10.0.0.0/24", item_type="address"))
        self.assertFalse(action.run("10.0.0.1", "10.0.1.0/24", item_type="address"))

    def test_contains_network_in_network(self):
        action = self.get_action_instance()

        self.assertTrue(action.run("10.0.0.0/24", "10.0.0.0/16", item_type="network"))
        self.assertFalse(action.run("10.0.0.0/24", "10.0.2.0/24", item_type="network"))
