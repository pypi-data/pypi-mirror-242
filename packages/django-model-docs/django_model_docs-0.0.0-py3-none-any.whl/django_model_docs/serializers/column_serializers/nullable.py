from django.db.models.fields import Field

from .column_serializer import (
    ColumnSerializer,
)


class NullableColumnSerializer(ColumnSerializer):
    name = "Nullable"

    def markdown(field: Field) -> str:
        """Return a string indicating whether the field is nullable"""

        return str(field.null)
