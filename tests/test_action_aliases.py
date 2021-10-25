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

from st2tests.base import BaseActionAliasTestCase


class GeoIP(BaseActionAliasTestCase):
    action_alias_name = "geoip"

    def test_geoip(self):
        format_string = self.action_alias_db.formats[0]["representation"][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "geoip 192.168.1.1,192.168.1.2"
        expected_parameters = {"ip_addresses": "192.168.1.1,192.168.1.2"}

        self.assertExtractedParametersMatch(
            format_string=format_string, command=command, parameters=expected_parameters
        )
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings, command=command
        )
