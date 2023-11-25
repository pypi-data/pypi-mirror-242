from textwrap import dedent
from django.test import TestCase
from django.db import models
from django_model_docs.serializers.model_serializer import ModelSerializer


class TestModelSerializer(TestCase):
    def test_works_as_expected(self):
        """Serializes a model correctly"""

        class ShoeCustomerModel(models.Model):
            """A customer in a shoe company app"""

            name = models.CharField(max_length=30, help_text="Full name")
            shoe_size = models.IntegerField()
            shoe_style = models.CharField([("LO", "Loafer"), ("BO", "Boot")])

        model = ShoeCustomerModel(name="Joe", shoe_size=9, shoe_style="BO")
        serializer = ModelSerializer()

        self.assertEqual(
            serializer.markdown(model),
            (
                "## `shoecustomermodel` model\n"
                + "\n"
                + "A customer in a shoe company app\n"
                + "\n"
                + "|    Field   |Description|  Data type |Nullable|Default|\n"
                + "|------------|-----------|------------|--------|-------|\n"
                + "|    `id`    |           |BigAutoField|  False |   -   |\n"
                + "|   `name`   | Full name |  CharField |  False |   -   |\n"
                + "| `shoe_size`|           |IntegerField|  False |   -   |\n"
                + "|`shoe_style`|           |  CharField |  False |   -   |\n"
                + "\n"
            ),
        )
