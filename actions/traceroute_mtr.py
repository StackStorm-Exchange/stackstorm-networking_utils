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

import subprocess
import json

from st2common.runners.base_action import Action


class TracerouteMTR(Action):
    def run(
        self,
        host,
        port=None,
        family="any",
        traceroute_type="icmp",
        dns=True,
        show_ips=False,
        asn=False,
        max_ttl=30,
        interval=1,
    ):
        """
        Carry out a traceroute using MTR and return an JSON object containing
        :param host: str
        :param port: int
        :param family: str
        :param traceroute_type: str
        :param dns: bool
        :param show_ips: bool
        :param asn: bool
        :param max_ttl: int
        :param interval: int
        :return: dict
        """

        command = [
            "mtr",
            str(host),
            "--json",
            "--max-ttl",
            str(max_ttl),
            "--interval",
            str(interval),
        ]

        if family == "ipv4":
            command.append("-4")
        elif family == "ipv6":
            command.append("-6")

        if traceroute_type == "tcp":
            command.append("--tcp")
            if port is not None:
                command.append("--port")
                command.append(str(port))
            else:
                raise TypeError("Missing Port for TCP traceroute")
        elif traceroute_type == "udp":
            command.append("--udp")
            if port is not None:
                command.append("--port")
                command.append(str(port))
            else:
                raise TypeError("Missing Port for UDP traceroute")

        if not dns:
            command.append("--no-dns")

        if show_ips:
            command.append("--show-ips")

        if asn:
            command.append("--aslookup")

        self.logger.debug("Running MTR: %s", " ".join(command))

        traceroute = subprocess.check_output(command).decode().strip()
        result = json.loads(traceroute)

        return result
