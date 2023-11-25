from django.test import TestCase
from django.db import models
from django_model_docs.serializers.column_serializers.data_type import (
    DataTypeColumnSerializer,
)


class TestDataTypeColumnSerializer(TestCase):
    def test_handles_CharField(self):
        """Serializes CharField data type column correctly"""

        field = models.CharField()
        serializer = DataTypeColumnSerializer

        self.assertEqual(serializer.markdown(field), "CharField")

    def test_handles_FloatField(self):
        """Serializes FloatField data type column correctly"""

        field = models.FloatField()
        serializer = DataTypeColumnSerializer

        self.assertEqual(serializer.markdown(field), "FloatField")

    def test_handles_CharFieldWithChoices(self):
        """Serializes CharField with choices correctly"""

        field = models.CharField(
            choices=[
                ("KV", "Kurt Vonnegut"),
                ("JP", "John Prine"),
                ("JQ", "Jacques Pepin"),
            ]
        )
        serializer = DataTypeColumnSerializer

        self.assertEqual(
            serializer.markdown(field),
            (
                "CharField<br><br>Choices (stored value : human readable)<br>"
                + "<br>- `KV` : `Kurt Vonnegut`"
                + "<br>- `JP` : `John Prine`"
                + "<br>- `JQ` : `Jacques Pepin`<br>"
            ),
        )
