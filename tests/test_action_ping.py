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
from ping import Ping

__all__ = ["PingActionTestCase"]


class PingActionTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = Ping

    @patch("subprocess.check_output")
    def test_run_ping_google_dns(self, mock):
        action = self.get_action_instance()

        mock.return_values = b"""
        ping 8.8.8.8 -c 5
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=63 time=36.6 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=63 time=22.4 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=63 time=23.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=63 time=22.0 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=63 time=21.4 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 21.404/25.136/36.668/5.794 ms"""

        (success, result) = action.run("8.8.8.8", force_success=True)

        self.assertTrue(success)
