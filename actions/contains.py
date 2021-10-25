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
import six
from st2common.runners.base_action import Action


class Contains(Action):
    def run(self, item, container, item_type="address"):
        """
        Check if item is in container
        :param item: string
        :param item_type: string
        :param container: string
        :return: bool
        """

        container_obj = ipaddress.ip_network(six.text_type(container))

        if item_type == "address":
            obj = ipaddress.ip_address(six.text_type(item))
            return obj in container_obj
        elif item_type == "network":
            obj = ipaddress.ip_network(six.text_type(item))
            return (
                container_obj.network_address <= obj.network_address
                and container_obj.broadcast_address >= obj.broadcast_address
            )
        else:
            raise TypeError("Unknown item type: {}".format(item_type))
