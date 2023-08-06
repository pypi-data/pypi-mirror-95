import unittest
import uuid

from smartobjects.api_manager import APIManager
from smartobjects.ingestion.events import EventsService

from tests.mocks.local_api_server import LocalApiServer


class TestEventsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False, backoff_config = None, token_override=None)
        cls.events = EventsService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.server.backend.clear()

    def test_send_ok(self):
        self.server.server.backend.objects['kitchen_door'] = {'x_device_id': 'kitchen_door'}

        resp = self.events.send([
            {'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'},
            {'x_object': {'x_device_id': 'cat_detector'}, 'x_event_type': 'cat_disappeared'},
        ])

        self.assertTrue(isinstance(resp[0].id, uuid.UUID))
        self.assertEqual(resp[0].result, "success")
        self.assertEqual(resp[0].object_exists, True)
        self.assertIn(resp[0].id, self.server.server.backend.events)
        self.assertEqual(self.server.server.backend.events[resp[0].id]['x_event_type'], 'door_open')

        self.assertTrue(isinstance(resp[1].id, uuid.UUID))
        self.assertEqual(resp[1].result, "success")
        self.assertEqual(resp[1].object_exists, False)
        self.assertIn(resp[1].id, self.server.server.backend.events)
        self.assertEqual(self.server.server.backend.events[resp[1].id]['x_object']['x_device_id'], 'cat_detector')

    def test_send_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([])
            self.assertEqual(ctx.exception.message, "Event list cannot be null or empty.")

    def test_send_device_id_missing(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([{'x_event_type': 'invalid event'}])
            self.assertEqual(ctx.exception.message, "x_object.x_device_id cannot be null or empty.")

    def test_send_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([{'x_object': {'x_device_id': None}, 'x_event_type': 'invalid event'}])
            self.assertEqual(ctx.exception.message, "x_object.x_device_id cannot be null or empty.")

    def test_send_event_type_missing(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([{'x_object': {'x_device_id': 'invalid'}}])
            self.assertEqual(ctx.exception.message, "x_event_type cannot be null or empty.")

    def test_send_object_must_exist_ok(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([{'x_object': {'x_device_id': 'invalid'}, 'x_event_type': ''}])
            self.assertEqual(ctx.exception.message, "x_event_type cannot be null or empty.")

    def test_send_event_type_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send([{'x_object': {'x_device_id': 'invalid'}, 'x_event_type': ''}])
            self.assertEqual(ctx.exception.message, "x_event_type cannot be null or empty.")

    def test_send_object_must_exist_fail(self):
        self.server.server.backend.objects['kitchen_door'] = {'x_device_id': 'kitchen_door'}
        resp = self.events.send([
            {'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'},
            {'x_object': {'x_device_id': 'cat_detector'}, 'x_event_type': 'cat_disappeared'},
        ], must_exist=True)

        self.assertTrue(isinstance(resp[0].id, uuid.UUID))
        self.assertEqual(resp[0].result, "success")

        self.assertTrue(isinstance(resp[1].id, uuid.UUID))
        self.assertEqual(resp[1].result, "error")
        self.assertEqual(resp[1].message, "Object 'cat_detector' not found")
        self.assertNotIn(resp[1].id, self.server.server.backend.events)

    def test_send_object_no_report(self):
        # with report_result=False, the request throws an error with the first error message but no details for
        # each event
        self.server.server.backend.objects['kitchen_door'] = {'x_device_id': 'kitchen_door'}
        with self.assertRaises(ValueError) as ctx:
            self.events.send([
                {'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'},
                {'x_object': {'x_device_id': 'cat_detector'}, 'x_event_type': 'cat_disappeared'},
            ], must_exist=True, report_results=False)
            self.assertEqual(ctx.exception.message, "Object 'cat_detector' not found")

    def test_send_duplicate(self):
        event_id = uuid.uuid4()

        with self.assertRaises(ValueError) as ctx:
            self.events.send([
                {'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'},
                {'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_closed'},
                {'event_id': event_id, 'x_object': {'x_device_id': 'cat_detector'}, 'x_event_type': 'cat_disappeared'},
            ])
            self.assertEqual(ctx.exception.message, "The event_id [{}] is duplicated in the list".format(event_id))

    def test_send_already_exist(self):
        event_id = uuid.uuid4()
        self.events.send([{'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'}])

        resp = self.events.send([{'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_closed'}])

        self.assertEqual(resp[0].id, event_id)
        self.assertEqual(resp[0].result, "error")
        self.assertEqual(resp[0].message, "Event ID '{}' already exists".format(event_id))

    def test_send_from_device_ok(self):
        self.server.server.backend.objects['device_1'] = {'x_device_id': 'device_1'}

        resp = self.events.send_from_device('device_1', [
            {'x_event_type': 'open'},
            {'x_event_type': 'closed'}
        ])

        self.assertTrue(isinstance(resp[0].id, uuid.UUID))
        self.assertEqual(resp[0].result, "success")
        self.assertTrue(isinstance(resp[1].id, uuid.UUID))
        self.assertEqual(resp[1].result, "success")

        self.assertDictContainsSubset({
            'x_object': {'x_device_id': 'device_1'},
            'x_event_type': 'open'
        }, self.server.server.backend.events[resp[0].id])

        self.assertDictContainsSubset({
            'x_object': {'x_device_id': 'device_1'},
            'x_event_type': 'closed'
        }, self.server.server.backend.events[resp[1].id])

    def test_send_from_device_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send_from_device(None, [{'x_event_type': 'open'}])
            self.assertEqual(ctx.exception.message, "device_id cannot be null or empty.")

    def test_send_from_device_empty_events(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send_from_device('device_1', [])
            self.assertEqual(ctx.exception.message, "Event list cannot be null or empty.")

    def test_send_from_device_event_type_missing(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send_from_device('device_1', [{'some_property': 'blue'}])
            self.assertEqual(ctx.exception.message, "x_event_type cannot be null or empty.")

    def test_send_from_device_event_type_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.events.send_from_device('device_1', [{'x_event_type': '', 'some_property': '42'}])
            self.assertEqual(ctx.exception.message, "x_event_type cannot be null or empty.")

    def test_send_from_device_event_already_exist(self):
        event_id = uuid.uuid4()
        self.events.send([{'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'}])

        resp = self.events.send_from_device('kitchen_door', [{'event_id': event_id, 'x_event_type': 'door_closed'}])
        self.assertEqual(resp[0].result, "error")
        self.assertEqual(resp[0].message, "Event ID '{}' already exists".format(event_id))

    def test_send_from_device_duplicate(self):
        event_id = uuid.uuid4()
        with self.assertRaises(ValueError) as ctx:
            self.events.send_from_device('device_1', [
                {'event_id': event_id, 'x_event_type': 'door_open'},
                {'event_id': event_id, 'x_event_type': 'door_closed'}
            ])
            self.assertEqual(ctx.exception.message, "The event_id [{}] is duplicated in the list".format(event_id))

    def test_event_exists(self):
        event_id = uuid.uuid4()
        self.events.send([{'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'}])

        self.assertEqual(self.events.event_exists(event_id), True)
        self.assertEqual(self.events.event_exists(uuid.uuid4()), False)

    def test_events_exist(self):
        ids_sent = [uuid.uuid4(), uuid.uuid4()]
        ids_not_sent = [uuid.uuid4(), uuid.uuid4()]

        events = [{'event_id': event_id, 'x_object': {'x_device_id': 'kitchen_door'}, 'x_event_type': 'door_open'} for event_id in ids_sent]
        self.events.send(events)

        resp = self.events.events_exist(ids_sent + ids_not_sent)

        self.assertDictContainsSubset({event_id: True for event_id in ids_sent}, resp)
        self.assertDictContainsSubset({event_id: False for event_id in ids_not_sent}, resp)



