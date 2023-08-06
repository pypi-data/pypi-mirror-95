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
from oslo_config import cfg

from designate.conf import base  # noqa
from designate.conf import akamai
from designate.conf import agent
from designate.conf import api
from designate.conf import bind9
from designate.conf import central
from designate.conf import coordination
from designate.conf import denominator
from designate.conf import djbdns
from designate.conf import dynect
from designate.conf import gdnsd
from designate.conf import heartbeat_emitter
from designate.conf import infoblox
from designate.conf import keystone
from designate.conf import knot2
from designate.conf import mdns
from designate.conf import metrics
from designate.conf import msdns
from designate.conf import network_api
from designate.conf import producer
from designate.conf import proxy
from designate.conf import sink
from designate.conf import storage
from designate.conf import worker

CONF = cfg.CONF

base.register_opts(CONF)
akamai.register_opts(CONF)
agent.register_opts(CONF)
api.register_opts(CONF)
bind9.register_opts(CONF)
central.register_opts(CONF)
coordination.register_opts(CONF)
denominator.register_opts(CONF)
djbdns.register_opts(CONF)
dynect.register_opts(CONF)
gdnsd.register_opts(CONF)
heartbeat_emitter.register_opts(CONF)
infoblox.register_opts(CONF)
keystone.register_opts(CONF)
knot2.register_opts(CONF)
mdns.register_opts(CONF)
metrics.register_opts(CONF)
msdns.register_opts(CONF)
network_api.register_opts(CONF)
producer.register_opts(CONF)
proxy.register_opts(CONF)
sink.register_opts(CONF)
storage.register_opts(CONF)
worker.register_opts(CONF)
