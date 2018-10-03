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

class Ping(Action):
    def run(self, host, force_success=False, count=5):
        """
        Carry out a ping and return an JSON object containing

        :param host: string
        :param force_success: Boolean
        :param count: int
        :return: (boolean, dict)
        """

        results = dict()

        try:
            ping = subprocess.check_output(
                ["ping", "-c", str(count), host]
            )
        except subprocess.CalledProcessError, e:
            results['up'] = False
            results['output'] = e.output
        else:
            results['up'] = True
            results['output'] = ping

        if force_success:
            success = True
        else:
            success = results['up']

        return (success, results)
