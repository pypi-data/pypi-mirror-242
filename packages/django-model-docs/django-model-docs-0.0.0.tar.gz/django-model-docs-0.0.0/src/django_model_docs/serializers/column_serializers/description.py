from django.db.models.fields import Field

from .column_serializer import (
    ColumnSerializer,
)


class DescriptionColumnSerializer(ColumnSerializer):
    name = "Description"

    def markdown(field: Field) -> str:
        """Return a string describing the field."""

        return str(field.help_text)
