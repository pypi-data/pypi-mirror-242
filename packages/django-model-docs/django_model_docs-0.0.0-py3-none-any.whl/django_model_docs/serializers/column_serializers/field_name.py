from django.db.models.fields import Field

from .column_serializer import (
    ColumnSerializer,
)


class FieldNameColumnSerializer(ColumnSerializer):
    name = "Field"

    def markdown(field: Field) -> str:
        """Return a string of a field's name"""

        return f"`{field.name}`"
