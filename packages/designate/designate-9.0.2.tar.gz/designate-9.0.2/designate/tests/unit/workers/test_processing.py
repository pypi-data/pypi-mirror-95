# Copyright 2016 Rackspace Inc.
#
# Author: Eric Larson <eric.larson@rackspace.com>
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
# under the License.mport threading
import mock

from designate import exceptions
from designate.tests import TestCase
from designate.tests import fixtures
from designate.worker import processing


class TestProcessingExecutor(TestCase):
    def setUp(self):
        super(TestProcessingExecutor, self).setUp()
        self.stdlog = fixtures.StandardLogging()
        self.useFixture(self.stdlog)

    def test_execute_multiple_tasks(self):
        def t1():
            return 1

        def t2():
            return 2

        tasks = [t1, t2, t1, t2, t1]
        exe = processing.Executor()

        results = exe.run(tasks)
        self.assertEqual([1, 2, 1, 2, 1], results)

    def test_execute_single_task(self):
        def t1():
            return 1

        exe = processing.Executor()

        results = exe.run(t1)
        self.assertEqual(1, results[0])

    def test_execute_bad_task(self):
        def failed_task():
            raise exceptions.BadAction('Not Great')

        exe = processing.Executor()

        results = exe.run(failed_task)
        self.assertIsNone(results[0])

        self.assertIn('Not Great', self.stdlog.logger.output)

    def test_executor_name_with_task(self):
        mock_task = mock.NonCallableMock(spec_set=[
            'task_name',
        ])
        mock_task.task_name = 'task_name'

        exe = processing.Executor()

        self.assertEqual('task_name', exe.task_name(mock_task))

    def test_executor_name_with_func(self):
        mock_task = mock.NonCallableMock(spec_set=[
            'func_name',
        ])
        mock_task.func_name = 'func_name'

        exe = processing.Executor()

        self.assertEqual('func_name', exe.task_name(mock_task))
