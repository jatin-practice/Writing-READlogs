from django.test import TestCase

from __future__ import unicode_literals
import logging
from django.contrib.admin import AdminSite
from django.test import TestCase
from .admin import StatusLogAdmin
from .serializers import LogsSerializer
from .views import file_view
from .models import StatusLog


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient

class AccountTests(APITestCase):
    client = APIClient()
    def test_create_log(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('log-list')
        data = {"level":"INFO", "file_storage":"filesystem", "msg":"I am here"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_get_log_db(self):
        response = self.client.get(
            reverse("logs-all", kwargs={"version": "v1", "storage_type":"database"})
        )
        # fetch the data from db
        expected = StatusLog.objects.all()
        serialized = LogsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_log_filesystem(self):
        response = self.client.get(
            reverse("logs-all", kwargs={"version": "v1", "storage_type":"file_system"})
        )
        # fetch the data from db
        expected = file_view()
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_log_db_daterange(self):
        response = self.client.get(
            reverse("logs-all", kwargs={"version": "v1", "storage_type": "database", "start":"20-01-2020", "end":"21-01-20120"})
        )
        # fetch the data from db
        expected = StatusLog.objects.all()
        serialized = LogsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_log_db_level(self):
        response = self.client.get(
            reverse("logs-all", kwargs={"version": "v1", "storage_type": "database", "level":"INFO"})
        )
        # fetch the data from db
        expected = StatusLog.objects.all()
        serialized = LogsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
