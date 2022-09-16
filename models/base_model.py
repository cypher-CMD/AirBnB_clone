#!/usr/bin/python3
"""
The Base Module for AirBnB Console
"""
from unittest import result
import uuid
from datetime import datetime


class BaseModel:
    """The Base class"""

    def __init__(self, *args, **kwargs):
        """
        instatiates an object with it's
        attributes

        Args:
            *args (tuple): Ignored.
            kwargs: A dictionary of attribute keys-value pairs.
        """
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            from models import storage
            storage.new(self)

    def __str__(self):
        """string representation

        Returns: A string representation
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__
        of the instance

        Returns: Dict of attributes
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        result['__class__'] = self.__class__.__name__
        return result
