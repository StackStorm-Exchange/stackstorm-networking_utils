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
from mock import patch
from traceroute_mtr import TracerouteMTR

__all__ = ["TracerouteMTRTestCase"]


class TracerouteMTRTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = TracerouteMTR

    @patch("subprocess.check_output")
    def test_traceroute_mtr_localhost(self, mock):
        action = self.get_action_instance()

        mock.return_value = b"""
    {
    "report": {
      "mtr": {
        "src": "test",
        "dst": "127.0.0.1",
        "tos": "0x0",
        "psize": "64",
        "bitpattern": "0x00",
        "tests": "10"
      },
      "hubs": [
        {
          "count": "1",
          "host": "localhost",
          "Loss%": 0,
          "Snt": 10,
          "Last": 0.07,
          "Avg": 0.07,
          "Best": 0.07,
          "Wrst": 0.1,
          "StDev": 0.01
        }
      ]
    }
  }
    """

        result = action.run("127.0.0.1")

        self.assertGreater(len(result["report"]["hubs"]), 0)
