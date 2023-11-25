from django.test import TestCase
from django.db import models
from django_model_docs.serializers.column_serializers.nullable import (
    NullableColumnSerializer,
)


class TestNullableColumnSerializer(TestCase):
    def test_serializes_correctly_with_non_nullable_field(self):
        """Serializes non-nullable field to "False" """
        field = models.Field(null=False)
        serializer = NullableColumnSerializer

        self.assertEqual(serializer.markdown(field), "False")

    def test_serializes_correctly_with_nullable_field(self):
        """Serializes nullable field to "True" """

        field = models.Field(null=True)
        serializer = NullableColumnSerializer

        self.assertEqual(serializer.markdown(field), "True")
