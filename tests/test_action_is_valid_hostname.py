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

from is_valid_hostname import IsValidHostnameAction

__all__ = [
    'IsValidHostnameActionTestCase'
]


class IsValidHostnameActionTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = IsValidHostnameAction

    def test_run_valid_hostname(self):
        expected = {"final_dot": False,
                    "fqdn": False,
                    'hostname': "foo",
                    'valid': True}

        action = self.get_action_instance()
        results = action.run("foo")

        self.assertEqual(results, expected)

    def test_run_valid_fqdn_final(self):
        expected = {"final_dot": False,
                    "fqdn": True,
                    'hostname': "foo.example.org",
                    'valid': True}

        action = self.get_action_instance()
        results = action.run("foo.example.org")

        self.assertEqual(results, expected)

    def test_run_valid_fqdn_final_dot(self):
        expected = {"final_dot": True,
                    "fqdn": True,
                    'hostname': "foo.example.org.",
                    'valid': True}

        action = self.get_action_instance()
        results = action.run("foo.example.org.")

        self.assertEqual(results, expected)

    def test_run_invalid_hostname_too_long_255(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "a" * 255 + ".")

    def test_run_invalid_hostname_too_long_300(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "a" * 300 + ".")

    def test_run_invalid_hostname_with_dollar(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foobar$")

    def test_run_invalid_hostname_with_long_label(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foo." + "a" * 64 + ".com.")

    def test_run_invalid_hostname_label_startswith_dash(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foo.-sub.example.com")

    def test_run_invalid_hostname_label_endswith_dash(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foo.sub-.example.com")

    def test_run_invalid_hostname_numeric_tld(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foo.sub-.example.123")
