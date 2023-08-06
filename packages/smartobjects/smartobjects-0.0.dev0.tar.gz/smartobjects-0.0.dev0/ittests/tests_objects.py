import unittest
import uuid

from ittests.it_test import TestHelper


class TestObjectsService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/documentation/api_ingestion.html#objects
    """

    @classmethod
    def setUpClass(cls):
        cls.client = TestHelper.getClient()

    def test_delete(self):
        currentUUID = uuid.uuid4()
        deviceIdToDelete = "deviceIdToDelete-{}".format(currentUUID)

        with self.assertRaises(ValueError):
            self.client.objects.delete(deviceIdToDelete)

        self.client.objects.create({
            "x_device_id": deviceIdToDelete,
            "x_object_type": "object_type1",
        })

        self.client.objects.delete(deviceIdToDelete)

    def test_basic_objects(self):
        currentUUID = uuid.uuid4()
        deviceId = "deviceId-{}".format(currentUUID)
        value = "value-{}".format(currentUUID)

        self.assertEqual(self.client.objects.object_exists(deviceId), False)
        self.assertEqual(self.client.objects.objects_exist([deviceId]), {
            deviceId: False
        })

        self.client.objects.create({
            "x_device_id": deviceId,
            "x_object_type": "object_type1",
            "object_text_attribute": value,
        })

        with self.assertRaises(ValueError):
            self.client.objects.create({
                "x_device_id": deviceId,
            })

        self.assertEqual(self.client.objects.object_exists(deviceId), True)
        self.assertEqual(self.client.objects.objects_exist([deviceId]), {
            deviceId: True
        })

        self.client.objects.update(deviceId, {
            "object_text_attribute": "newvalue"
        })
