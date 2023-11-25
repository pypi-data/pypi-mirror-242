from abc import ABC, abstractmethod
from django.db.models.fields import Field


class ColumnSerializer(ABC):

    """
    Base class for column serializers
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The column name"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def markdown(field: Field) -> str:
        """Return a markdown string representation of a Field"""
        raise NotImplementedError
