# Copyright 2014 Rackspace Inc.
#
# Author: Tim Simmons <tim.simmons@rackspace.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_config import cfg

BIND9_GROUP = cfg.OptGroup(
    name='backend:agent:bind9',
    title="Configuration for bind9 backend"
)

BINS9_OPTS = [
    cfg.StrOpt('rndc_host', default='127.0.0.1', help='RNDC Host'),
    cfg.IntOpt('rndc_port', default=953, help='RNDC Port'),
    cfg.StrOpt('rndc_config_file',
               help='RNDC Config File'),
    cfg.StrOpt('rndc_key_file', help='RNDC Key File'),
    cfg.StrOpt('zone_file_path', default='$state_path/zones',
               help='Path where zone files are stored'),
    cfg.StrOpt('query_destination', default='127.0.0.1',
               help='Host to query when finding zones'),
]


def register_opts(conf):
    conf.register_group(BIND9_GROUP)
    conf.register_opts(BINS9_OPTS, group=BIND9_GROUP)


def list_opts():
    return {
        BIND9_GROUP: BINS9_OPTS,
    }
