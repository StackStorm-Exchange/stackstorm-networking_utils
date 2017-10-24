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

import re

from st2actions.runners.pythonrunner import Action


class IsValidHostnameAction(Action):
    def run(self, hostname):
        """
        Is this a valid hostname?

        Args:
          hostname: The hostname to validate.

        Raises:
          ValueError: On invalid hotname.

        Returns:
          dict: With extra information about the hostname.
        """

        results = {
            "hostname": hostname
        }
        invalid_chars = re.compile("[^a-z0-9-]", re.IGNORECASE)

        if hostname.endswith('.'):
            hostname.strip('.')
            results["final_dot"] = True
        else:
            results["final_dot"] = False

        if hostname.count('.') > 0:
            results["fqdn"] = True
        else:
            results["fqdn"] = False

        labels = hostname.split('.')

        if len(hostname) > 253:
            raise ValueError("Hostname is longer than 253 chars.")
        elif any(invalid_chars.search(label) for label in labels):
            raise ValueError("Hostname has invalid chars.")
        elif any(len(label) > 63 for label in labels):
            raise ValueError("Label over 63 chars.")
        elif any(label.startswith(-) for label in labels):
            raise ValueError("Label starts with a '-'")
        elif any(label.endswith(-) for label in labels):
            raise ValueError("Label ends with a '-'")
        elif labels[-1].match(r"[0-9]+$"):
            raise ValueError("All numberic TLD!")
        else:
            results['valid'] = True

        return results
