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

from st2common.runners.base_action import Action


class HostsAction(Action):
    def run(self, family, network):
        """
        List the host addresses in a given subnet

        Args:
          network: The network to enumerate.
          family: The type of network (ipv4, ipv6).

        Raises:
          ValueError: On invalid network has been given.

        Returns:
          list: The list of all the IP addresses in the network.
        """

        network_obj = ipaddress.ip_network(network)

        if family == "ipv6" and network_obj.version == 4:
            raise ValueError("Valid IPv4 network, but IPv6 is required.")
        elif family == "ipv4" and network_obj.version == 6:
            raise ValueError("Valid IPv6 network, but IPv4 is required.")

        return [str(address) for address in network_obj.hosts()]
