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

from fping import FPing
from mock import patch

__all__ = ["FPingTestCase"]


class FPingTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = FPing

    @patch("subprocess.check_output")
    def test_fping_localhost(self, mock):
        action = self.get_action_instance()

        mock.return_value = b"8.8.8.8 : xmt/rcv/%loss = 10/10/0%, min/avg/max = 4.78/4.85/4.91\n"
        result = action.run("127.0.0.1", interval=1, count=3)

        self.assertEquals(result["packets"]["transmitted"], result["packets"]["received"])
