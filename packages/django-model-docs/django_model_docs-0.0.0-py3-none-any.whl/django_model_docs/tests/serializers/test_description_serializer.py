from django.test import TestCase
from django.db import models
from django_model_docs.serializers.column_serializers.description import (
    DescriptionColumnSerializer,
)


class TestDescriptionColumnSerializer(TestCase):
    def test_description_users_help_attribute(self):
        """Serializes str description correctly"""

        expected_description = "expected description"
        field = models.CharField(help_text=expected_description)
        serializer = DescriptionColumnSerializer

        self.assertEqual(serializer.markdown(field), expected_description)

    def test_description_users_handles_None(self):
        """Serializes None description correctly"""

        field = models.CharField()
        serializer = DescriptionColumnSerializer

        self.assertEqual(serializer.markdown(field), "")
