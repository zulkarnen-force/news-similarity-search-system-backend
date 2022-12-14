from amqpstorm.management import ApiError
from amqpstorm.management import ManagementApi
from amqpstorm.tests import HTTP_URL
from amqpstorm.tests import PASSWORD
from amqpstorm.tests import USERNAME
from amqpstorm.tests.functional.utility import TestFunctionalFramework
from amqpstorm.tests.functional.utility import setup


class ApiQueueFunctionalTests(TestFunctionalFramework):
    @setup(queue=False)
    def test_api_queue_get(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.queue.declare(self.queue_name)

        queue = api.queue.get(self.queue_name)

        self.assertIsInstance(queue, dict)
        self.assertIn('name', queue)
        self.assertIn('auto_delete', queue)

    @setup(queue=False)
    def test_api_queue_list(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)

        api.queue.declare(self.queue_name)

        queues = api.queue.list()

        self.assertIsInstance(queues, list)
        self.assertGreater(len(queues), 0)

        for queue in queues:
            self.assertIsInstance(queue, dict)
            self.assertIn('name', queue)
            self.assertIn('vhost', queue)
            self.assertIn('node', queue)
            self.assertIn('durable', queue)
            self.assertIn('arguments', queue)
            self.assertIn('auto_delete', queue)

    @setup(queue=False)
    def test_api_queue_list_pagination(self):
        queues_to_create = 33

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(self.queue_name)

        try:
            for index in range(queues_to_create):
                api.queue.declare(
                    'pagination-%d' % (index + 1), virtual_host=self.queue_name
                )

            queues = api.queue.list(
                name='pagination-',
                page_size=3,
                virtual_host=self.queue_name
            )
        finally:
            for index in range(queues_to_create):
                api.queue.delete(
                    'pagination-%d' % (index + 1), virtual_host=self.queue_name
                )
            self.api.virtual_host.delete(self.queue_name)

        self.assertIsInstance(queues, list)
        self.assertEqual(len(queues), queues_to_create)

    @setup(queue=False)
    def test_api_queue_list_no_pagination(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(self.queue_name)

        try:
            api.queue.declare('abc', virtual_host=self.queue_name)
            api.queue.declare('def', virtual_host=self.queue_name)
            api.queue.declare('ghi', virtual_host=self.queue_name)

            queues = api.queue.list(
                page_size=None, virtual_host=self.queue_name
            )
        finally:
            api.queue.delete('abc', virtual_host=self.queue_name)
            api.queue.delete('def', virtual_host=self.queue_name)
            api.queue.delete('ghi', virtual_host=self.queue_name)
            self.api.virtual_host.delete(self.queue_name)

        self.assertIsInstance(queues, list)
        self.assertEqual(len(queues), 3)

    @setup(queue=False)
    def test_api_queue_list_filter_with_regex(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(self.queue_name)

        try:
            api.queue.declare('abc', virtual_host=self.queue_name)
            api.queue.declare('def', virtual_host=self.queue_name)
            api.queue.declare('ghi', virtual_host=self.queue_name)

            queues = api.queue.list(name='^ab', use_regex='true',
                                    virtual_host=self.queue_name)
        finally:
            api.queue.delete('abc', virtual_host=self.queue_name)
            api.queue.delete('def', virtual_host=self.queue_name)
            api.queue.delete('ghi', virtual_host=self.queue_name)
            self.api.virtual_host.delete(self.queue_name)

        self.assertIsInstance(queues, list)
        self.assertEqual(len(queues), 1)

    @setup(queue=False)
    def test_api_queue_list_filter_with_regex_boolean(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(self.queue_name)

        try:
            api.queue.declare('abc', virtual_host=self.queue_name)
            api.queue.declare('def', virtual_host=self.queue_name)
            api.queue.declare('ghi', virtual_host=self.queue_name)

            queues = api.queue.list(name='^ab', use_regex=True,
                                    virtual_host=self.queue_name)
        finally:
            api.queue.delete('abc', virtual_host=self.queue_name)
            api.queue.delete('def', virtual_host=self.queue_name)
            api.queue.delete('ghi', virtual_host=self.queue_name)
            self.api.virtual_host.delete(self.queue_name)

        self.assertIsInstance(queues, list)
        self.assertEqual(len(queues), 1)

    @setup(queue=False)
    def test_api_queue_list_filter_without_regex(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(self.queue_name)

        try:
            api.queue.declare('abc', virtual_host=self.queue_name)
            api.queue.declare('def', virtual_host=self.queue_name)
            api.queue.declare('ghi', virtual_host=self.queue_name)

            queues = api.queue.list(name='ab', use_regex=False,
                                    virtual_host=self.queue_name)
        finally:
            api.queue.delete('abc', virtual_host=self.queue_name)
            api.queue.delete('def', virtual_host=self.queue_name)
            api.queue.delete('ghi', virtual_host=self.queue_name)
            self.api.virtual_host.delete(self.queue_name)

        self.assertIsInstance(queues, list)
        self.assertEqual(len(queues), 1)

    @setup(queue=False)
    def test_api_queue_list_all(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)

        api.queue.declare(self.queue_name)

        queues = api.queue.list(show_all=True)

        self.assertIsInstance(queues, list)
        self.assertGreater(len(queues), 0)

        for queue in queues:
            self.assertIsInstance(queue, dict)
            self.assertIn('name', queue)
            self.assertIn('vhost', queue)
            self.assertIn('node', queue)
            self.assertIn('durable', queue)
            self.assertIn('arguments', queue)
            self.assertIn('auto_delete', queue)

    @setup(queue=False)
    def test_api_queue_declare(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        self.assertIsNone(api.queue.declare(self.queue_name, durable=True))

        result = api.queue.get(self.queue_name)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], self.queue_name)
        self.assertEqual(result['auto_delete'], False)
        self.assertEqual(result['durable'], True)

    @setup(new_connection=False)
    def test_api_queue_declare_passive(self):
        expected_error_message = (
            'NOT-FOUND - The client attempted to work '
            'with a server entity that does not exist.'
        )

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)

        try:
            api.queue.declare(self.queue_name, passive=True)
        except ApiError as why:
            self.assertEqual(str(why), expected_error_message)
            self.assertEqual(why.error_type, 'NOT-FOUND')
            self.assertEqual(why.error_code, 404)

    @setup(new_connection=False)
    def test_api_queue_declare_passive_exists(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.queue.declare(self.queue_name)

        self.assertIsNotNone(api.queue.declare(self.queue_name, passive=True))

    @setup(new_connection=False)
    def test_api_queue_delete(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        try:
            api.queue.declare(self.queue_name, durable=True)
            self.assertIsInstance(api.queue.get(self.queue_name), dict)
        finally:
            api.queue.delete(self.queue_name)

        try:
            api.queue.declare(self.queue_name, passive=True)
        except ApiError as why:
            self.assertEqual(why.error_code, 404)

    @setup(queue=True)
    def test_api_queue_purge(self):
        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)

        api.queue.declare(self.queue_name)
        self.assertIsNone(api.queue.purge(self.queue_name))

    @setup(queue=True)
    def test_api_queue_bind(self):
        exchange_name = 'amq.direct'

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.queue.declare(self.queue_name)

        bindings = len(api.queue.bindings(self.queue_name))

        self.assertIsNone(api.queue.bind(queue=self.queue_name,
                                         exchange=exchange_name,
                                         routing_key=self.queue_name,
                                         arguments=None))

        self.assertEqual(len(api.queue.bindings(self.queue_name)),
                         bindings + 1)

    @setup(queue=True)
    def test_api_queue_unbind(self):
        exchange_name = 'amq.direct'

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)

        api.queue.declare(self.queue_name)

        bindings = len(api.queue.bindings(self.queue_name))

        api.queue.bind(queue=self.queue_name, exchange=exchange_name,
                       routing_key=self.queue_name, arguments=None)

        self.assertEqual(len(api.queue.bindings(self.queue_name)),
                         bindings + 1)

        self.assertIsNone(api.queue.unbind(queue=self.queue_name,
                                           exchange=exchange_name,
                                           routing_key=self.queue_name))

        self.assertEqual(len(api.queue.bindings(self.queue_name)), bindings)
