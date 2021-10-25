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

from is_valid_ip_port import IsValidIpPortAction

__all__ = ["IsValidPortActionTestCase"]


class IsValidPortActionTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = IsValidIpPortAction

    def test_run_invalid_port_too_large(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError, action.run, 66000)

    def test_run_invalid_port_negitive(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError, action.run, -10)

    def test_run_valid_port(self):
        action = self.get_action_instance()
        result = action.run(80)
        self.assertTrue(result)
