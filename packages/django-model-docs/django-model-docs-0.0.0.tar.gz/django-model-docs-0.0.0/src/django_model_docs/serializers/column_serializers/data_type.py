from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from .column_serializer import (
    ColumnSerializer,
)

from django_model_docs.serializers.utils import format_model_name

MAX_CHOICES = 75


class DataTypeColumnSerializer(ColumnSerializer):
    name = "Data type"

    def markdown(field: Field) -> str:
        """Get a string representing the data type of the field"""

        type_message = field.get_internal_type()

        choices = field.choices

        if choices is None:
            if isinstance(field, RelatedField):
                cleaned_relation_type_name = format_model_name(type(field))
                cleaned_target_model_name = format_model_name(field.related_model)
                type_message = (
                    f"{cleaned_relation_type_name} " + f"-> {cleaned_target_model_name}"
                )

            return type_message

        # Use special formatting for Choice and Choice-like fields
        type_message += "<br><br>Choices (stored value : human readable)<br><br>"

        for idx, choice_item in enumerate(choices):
            if idx > MAX_CHOICES:
                type_message += " - This list has been truncated..."
                break
            type_message += f"- `{choice_item[0]}` : `{choice_item[1]}`<br>"

        return type_message
