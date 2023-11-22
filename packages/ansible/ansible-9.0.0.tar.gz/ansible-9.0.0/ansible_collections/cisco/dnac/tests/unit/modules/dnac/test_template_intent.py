# Copyright (c) 2020-2022 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import patch
from ansible_collections.cisco.dnac.plugins.modules import template_intent
from .dnac_module import TestDnacModule, set_module_args, loadPlaybookData


class TestDnacTemplateIntent(TestDnacModule):

    module = template_intent

    test_data = loadPlaybookData("template_intent")

    playbook_config = test_data.get("playbook_config")
    playbook_config_missing_param = test_data.get("playbook_config_missing_param")

    def setUp(self):
        super(TestDnacTemplateIntent, self).setUp()
        self.mock_dnac_init = patch(
            "ansible_collections.cisco.dnac.plugins.module_utils.dnac.DNACSDK.__init__")
        self.run_dnac_init = self.mock_dnac_init.start()
        self.run_dnac_init.side_effect = [None]
        self.mock_dnac_exec = patch(
            "ansible_collections.cisco.dnac.plugins.module_utils.dnac.DNACSDK.exec"
        )
        self.run_dnac_exec = self.mock_dnac_exec.start()

    def tearDown(self):
        super(TestDnacTemplateIntent, self).tearDown()
        self.mock_dnac_exec.stop()
        self.mock_dnac_init.stop()

    def load_fixtures(self, response=None, device=""):
        if "create_template" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("create_template_list_response"),
                self.test_data.get("create_template_get_project_response"),
                self.test_data.get("create_template_response"),
                self.test_data.get("create_template_task_details_for_create"),
                self.test_data.get("create_template_version_template_response"),
                self.test_data.get("create_template_task_details_for_versioning")
            ]
        elif "update_not_needed" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("update_template_list"),
                self.test_data.get("update_template_existing_template"),
            ]
        elif "update_needed" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("update_template_list"),
                self.test_data.get("update_template_existing_template_needs_update"),
                self.test_data.get("update_template_response"),
                self.test_data.get("update_template_version_template_response"),
                self.test_data.get("update_template_task_details_for_versioning")
            ]
        elif "project_not_found" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                [],
            ]
        elif "delete_non_existing_template" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("create_template_list_response")
            ]
        elif "delete_template" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("update_template_list"),
                self.test_data.get("update_template_existing_template_needs_update"),
                self.test_data.get("delete_template_response"),
                self.test_data.get("delete_template_task_details"),
            ]

    def test_template_intent_create_template(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result.get('response').get('progress'),
            "Successfully committed template ANSIBLE-TEST to version 1"
        )

    def test_template_intent_update_not_needed(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=False, failed=False)
        self.assertEqual(
            result.get('msg'),
            "Template does not need update"
        )

    def test_template_intent_update_needed(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result.get('response').get('progress'),
            "Successfully committed template ANSIBLE-TEST to version 2"
        )

    def test_template_intent_project_not_found(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=False, failed=True)
        self.assertEqual(
            result.get('msg'),
            "Project Not Found"
        )

    def test_template_intent_delete_non_existing_template(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="deleted",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=False, failed=True)
        self.assertEqual(
            result.get('msg'),
            "Template not found"
        )

    def test_template_intent_delete_template(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="deleted",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result.get('response').get('progress'),
            "Successfully deleted template with name fd74ab6c-fdda-465e-9f59-fb7eac7d6b15"
        )

    def test_template_intent_missing_param(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config_missing_param
            )
        )
        result = self.execute_module(changed=False, failed=True)
        self.assertEqual(
            result.get('msg'),
            "missing required arguments: language or deviceTypes or softwareType"
        )

    def test_template_intent_invalid_state(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merge",
                config=self.playbook_config
            )
        )
        result = self.execute_module(changed=False, failed=True)
        self.assertEqual(
            result.get('msg'),
            "value of state must be one of: merged, deleted, got: merge"
        )

    def test_template_intent_invalid_param(self):
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.test_data.get("playbook_config_invalid_param")
            )
        )
        result = self.execute_module(changed=False, failed=True)
        self.assertEqual(
            result.get('msg'),
            "Invalid parameters in playbook: velocty : Invalid choice provided"
        )
