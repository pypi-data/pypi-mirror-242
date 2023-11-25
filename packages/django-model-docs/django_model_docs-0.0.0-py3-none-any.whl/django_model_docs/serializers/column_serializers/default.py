from django.db.models.fields import Field, NOT_PROVIDED

from .column_serializer import (
    ColumnSerializer,
)


class DefaultColumnSerializer(ColumnSerializer):
    name = "Default"

    def markdown(field: Field) -> str:
        """
        Return a string representation for the default value of a field.
        Use '-' when there is no default.
        Add single quotes around strings.
        For all other types return the type name coerced to a string.
        """
        if field.default == NOT_PROVIDED:
            return "-"
        if type(field.default) == str:
            return f"'{field.default}'"

        # Certain Fields require a callable default (I'm looking
        # at you ArrayField), so we want to make it [] instead of
        # `<class 'list'>` by calling any callable defaults.
        if callable(field.default):
            return field.default()
        return str(field.default)
