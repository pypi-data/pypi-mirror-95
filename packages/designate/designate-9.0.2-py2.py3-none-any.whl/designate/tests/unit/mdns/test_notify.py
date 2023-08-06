# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Author: Federico Ceratto <federico.ceratto@hpe.com>
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
import socket

import dns
import dns.rdataclass
import dns.rdatatype
import mock

import designate.mdns.notify as notify
import designate.tests
from designate.tests.unit import RoObject


class MdnsNotifyTest(designate.tests.TestCase):
    def setUp(self):
        super(MdnsNotifyTest, self).setUp()

        self.notify = notify.NotifyEndpoint(mock.Mock())

    @mock.patch('time.sleep')
    def test_notify_zone_changed(self, mock_sleep):
        self.notify._make_and_send_dns_message = mock.Mock()

        self.notify.notify_zone_changed(*range(8))

        self.notify._make_and_send_dns_message.assert_called_with(
            1, 2, 3, 4, 5, 6, notify=True
        )

    @mock.patch('time.sleep')
    def test_get_serial_number_nxdomain(self, mock_sleep):
        # The zone is not found but it was supposed to be there
        response = RoObject(
            answer=[RoObject(
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.SOA
            )],
            rcode=mock.Mock(return_value=dns.rcode.NXDOMAIN)
        )
        zone = RoObject(name='zn', serial=314)
        self.notify._make_and_send_dns_message = mock.Mock(
            return_value=(response, 1)
        )

        out = self.notify.get_serial_number(
            'c', zone, 'h', 1234, 1, 2, 3, 4
        )

        self.assertEqual(('NO_ZONE', None, 0), out)

    @mock.patch('time.sleep')
    def test_get_serial_number_nxdomain_deleted_zone(self, mock_sleep):
        # The zone is not found and it's not was supposed be there
        response = RoObject(
            answer=[RoObject(
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.SOA
            )],
            rcode=mock.Mock(return_value=dns.rcode.NXDOMAIN)
        )
        zone = RoObject(name='zn', serial=0, action='DELETE')
        self.notify._make_and_send_dns_message = mock.Mock(
            return_value=(response, 1)
        )

        out = self.notify.get_serial_number(
            'c', zone, 'h', 1234, 1, 2, 3, 4
        )

        self.assertEqual(('NO_ZONE', 0, 3), out)

    @mock.patch('time.sleep')
    def test_get_serial_number_ok(self, mock_sleep):
        zone = RoObject(name='zn', serial=314)
        ds = RoObject(items=[zone])
        response = RoObject(
            answer=[RoObject(
                name='zn',
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.SOA,
                to_rdataset=mock.Mock(return_value=ds)
            )],
            rcode=mock.Mock(return_value=dns.rcode.NOERROR)
        )
        self.notify._make_and_send_dns_message = mock.Mock(
            return_value=(response, 1)
        )

        out = self.notify.get_serial_number(
            'c', zone, 'h', 1234, 1, 2, 3, 4
        )

        self.assertEqual(('SUCCESS', 314, 3), out)

    @mock.patch('time.sleep')
    def test_get_serial_number_too_many_retries(self, mock_sleep):
        zone = RoObject(name='zn', serial=314)
        ds = RoObject(items=[RoObject(serial=310)])
        response = RoObject(
            answer=[RoObject(
                name='zn',
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.SOA,
                to_rdataset=mock.Mock(return_value=ds)
            )],
            rcode=mock.Mock(return_value=dns.rcode.NOERROR)
        )
        self.notify._make_and_send_dns_message = mock.Mock(
            return_value=(response, 1)
        )

        out = self.notify.get_serial_number(
            'c', zone, 'h', 1234, 1, 2, 3, 4
        )

        self.assertEqual(('ERROR', 310, 0), out)

    @mock.patch('time.sleep')
    def test_make_and_send_dns_message_timeout(self, mock_sleep):
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        self.notify._send_dns_message = mock.Mock(
            side_effect=dns.exception.Timeout
        )

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((None, 3), out)

    def test_make_and_send_dns_message_bad_response(self):
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        self.notify._send_dns_message = mock.Mock(
            side_effect=notify.dns_query.BadResponse
        )

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((None, 1), out)

    @mock.patch('time.sleep')
    def test_make_and_send_dns_message_eagain(self, mock_sleep):
        # bug #1558096
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        socket_error = socket.error()
        socket_error.errno = socket.errno.EAGAIN
        self.notify._send_dns_message = mock.Mock(
            side_effect=socket_error
        )

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((None, 3), out)

    def test_make_and_send_dns_message_econnrefused(self):
        # bug #1558096
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        socket_error = socket.error()
        socket_error.errno = socket.errno.ECONNREFUSED
        # socket errors other than EAGAIN should raise
        self.notify._send_dns_message = mock.Mock(
            side_effect=socket_error)

        self.assertRaises(
            socket.error,
            self.notify._make_and_send_dns_message,
            zone, 'host', 123, 1, 2, 3
        )

    def test_make_and_send_dns_message_nxdomain(self):
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        response = RoObject(rcode=mock.Mock(return_value=dns.rcode.NXDOMAIN))
        self.notify._send_dns_message = mock.Mock(return_value=response)

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((response, 1), out)

    def test_make_and_send_dns_message_missing_AA_flags(self):
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')

        response = RoObject(
            rcode=mock.Mock(return_value=dns.rcode.NOERROR),
            # rcode is NOERROR but (flags & dns.flags.AA) gives 0
            flags=0,
            answer=['answer'],
        )
        self.notify._send_dns_message = mock.Mock(return_value=response)

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((None, 1), out)

    def test_make_and_send_dns_message_error_flags(self):
        zone = RoObject(name='zn')
        self.notify._make_dns_message = mock.Mock(return_value='')
        response = RoObject(
            rcode=mock.Mock(return_value=dns.rcode.NOERROR),
            # rcode is NOERROR but flags are not NOERROR
            flags=123,
            ednsflags=321,
            answer=['answer'],
        )
        self.notify._send_dns_message = mock.Mock(return_value=response)

        out = self.notify._make_and_send_dns_message(
            zone, 'host', 123, 1, 2, 3
        )

        self.assertEqual((None, 1), out)

    def test_make_dns_message(self):
        msg = self.notify._make_dns_message('zone_name')
        txt = msg.to_text().split('\n')[1:]

        self.assertEqual([
            'opcode QUERY',
            'rcode NOERROR',
            'flags RD',
            ';QUESTION',
            'zone_name. IN SOA',
            ';ANSWER',
            ';AUTHORITY',
            ';ADDITIONAL'
        ], txt)

    def test_make_dns_message_notify(self):
        msg = self.notify._make_dns_message('zone_name', notify=True)
        txt = msg.to_text().split('\n')[1:]

        self.assertEqual([
            'opcode NOTIFY',
            'rcode NOERROR',
            'flags AA',
            ';QUESTION',
            'zone_name. IN SOA',
            ';ANSWER',
            ';AUTHORITY',
            ';ADDITIONAL',
        ], txt)

    @mock.patch.object(notify.dns_query, 'udp')
    def test_send_udp_dns_message(self, mock_udp):
        self.CONF.set_override('all_tcp', False, 'service:mdns')

        self.notify._send_dns_message('msg', '192.0.2.1', 1234, 1)

        mock_udp.assert_called_with(
            'msg', '192.0.2.1', port=1234, timeout=1
        )

    @mock.patch.object(notify.dns_query, 'tcp')
    def test_send_tcp_dns_message(self, mock_tcp):
        self.CONF.set_override('all_tcp', True, 'service:mdns')

        self.notify._send_dns_message('msg', '192.0.2.1', 1234, 1)

        mock_tcp.assert_called_with(
            'msg', '192.0.2.1', port=1234, timeout=1
        )
