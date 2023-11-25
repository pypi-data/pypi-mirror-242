from textwrap import dedent
from django.db import models
from django.db.models.fields import Field
from markdownTable import markdownTable
from django_model_docs.serializers.column_serializers import (
    ColumnSerializer,
    DescriptionColumnSerializer,
    FieldNameColumnSerializer,
    DataTypeColumnSerializer,
    DefaultColumnSerializer,
    NullableColumnSerializer,
)

DEFAULT_COLUMNS = [
    FieldNameColumnSerializer,
    DescriptionColumnSerializer,
    DataTypeColumnSerializer,
    NullableColumnSerializer,
    DefaultColumnSerializer,
]
"""Default columns to include when serializing a model"""


class ModelSerializer:

    """
    Django Model serializer

    Generate a markdown document section representing a Django model.
    The document section consisits of an H2 heading, a description,
    and a table with a row for each of the model's fields.
    """

    def __init__(self, columns: list[ColumnSerializer] = DEFAULT_COLUMNS):
        """
        Initialize a DjangoModelSerializer

        Args:
            Columns: A list of ColumnSerializers to use in the field
                     table. The order of the items in this list will determine
                     the order of the columns.
        """
        self.columns = columns

    def heading(self, model: models.Model) -> str:
        """
        Text to use for the section heading
        """

        return f"{model._meta.model_name}"

    def description(self, model: models.Model) -> str:
        """
        Text to use for the section description
        """

        return f"{dedent(model.__doc__)}".strip()

    def get_row_object(self, field: Field) -> dict:
        """
        Serialize a given field into a JSON object representing
        a table row.

        Args:
            field: A Django model Field

        Returns:
            A dict with column names as keys and cell values
            as values
        """

        ret = {}

        for column in self.columns:
            ret[column.name] = column.markdown(field)

        return ret

    def markdown_table(self, model: models.Model) -> str:
        """
        Get markdown table representation of a model.

        Args:
            model: a Django model

        Returns:
            a mardown table representation of the model
        """

        # Generate a list of dictionaries, one for each field in the model.
        # Each dictionary will represent one row in the table
        field_dicts = []
        for field in model._meta.fields:
            field_dicts.append(self.get_row_object(field))

        # Generate the table markdown based on the list of dicts
        # generated above
        return (
            markdownTable(field_dicts)
            .setParams(row_sep="markdown", quote=False)
            .getMarkdown()
        ).strip()

    def markdown(self, model: models.Model):
        """
        Get markdown documentation section for a Django model
        """
        return (
            f"## `{self.heading(model)}` model"
            + "\n\n"
            + f"{self.description(model)}"
            + "\n\n"
            + f"{self.markdown_table(model)}"
            + "\n\n"
        )
