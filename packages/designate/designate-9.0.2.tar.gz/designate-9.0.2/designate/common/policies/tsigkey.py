# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from oslo_policy import policy

from designate.common.policies import base

rules = [
    policy.DocumentedRuleDefault(
        name="create_tsigkey",
        check_str=base.RULE_ADMIN,
        description="Create Tsigkey",
        operations=[
            {
                'path': '/v2/tsigkeys',
                'method': 'POST'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name="find_tsigkeys",
        check_str=base.RULE_ADMIN,
        description="List Tsigkeys",
        operations=[
            {
                'path': '/v2/tsigkeys',
                'method': 'GET'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name="get_tsigkey",
        check_str=base.RULE_ADMIN,
        description="Show a Tsigkey",
        operations=[
            {
                'path': '/v2/tsigkeys/{tsigkey_id}',
                'method': 'PATCH'
            }, {
                'path': '/v2/tsigkeys/{tsigkey_id}',
                'method': 'GET'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name="update_tsigkey",
        check_str=base.RULE_ADMIN,
        description="Update Tsigkey",
        operations=[
            {
                'path': '/v2/tsigkeys/{tsigkey_id}',
                'method': 'PATCH'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name="delete_tsigkey",
        check_str=base.RULE_ADMIN,
        description="Delete a Tsigkey",
        operations=[
            {
                'path': '/v2/tsigkeys/{tsigkey_id}',
                'method': 'DELETE'
            }
        ]
    )
]


def list_rules():
    return rules
