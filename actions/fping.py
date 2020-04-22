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

from st2common.runners.base_action import Action


class FPing(Action):
    def run(self, host, family="any", count=1, interval=1000):
        """
        Carry out a fping, and return formatted data
        :param host: str
        :param family: str
        :param count: int
        :param interval: int
        :return: Mapping[str, Any]
        """

        command = [
            "fping",
            str(host),
            "--netdata",
            "--quiet",
            "--count",
            str(count),
            "--interval",
            str(interval),
        ]

        if family == "ipv4":
            command.append("-4")
        elif family == "ipv6":
            command.append("-6")

        self.logger.debug("Running FPING: %s", " ".join(command))

        fping = (
            subprocess.check_output(command, stderr=subprocess.STDOUT).decode().strip()
        )

        self.logger.debug("Returned: %s", fping)

        return parse_fping_output(fping)


def parse_fping_output(output):
    target, result = output.split(" : ")
    packets_raw, latency_raw = result.split(", ")
    packets = {}
    latency = {}

    packets_data = packets_raw.split(" = ")[1].split("/")
    packets["transmitted"] = int(packets_data[0])
    packets["received"] = int(packets_data[1])
    packets["loss_percent"] = int(packets_data[2][:-1])

    latency_data = latency_raw.split(" = ")[1].split("/")
    latency["minimum"] = float(latency_data[0])
    latency["average"] = float(latency_data[1])
    latency["maximum"] = float(latency_data[2])

    return {"packets": packets, "latency": latency}
