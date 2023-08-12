#!/usr/bin/python3
"""This defines BaseModel for all common attributes/methods"""
import uuid
import models
from datetime import datetime


class BaseModel:
    """Beginning of basemodel class"""

    def __init__(self, *args, **kwargs):
        """Initializes new class

        Args:
            - *args: Arguments list (unused)
            - **kwargs: a dict for key/value arguments
            """

        dtform = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, dtform)
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Saves the current datetime to updated_at"""

        self.updated_at = datetime.now()
        models.storage.save()

    def __repr__(self):
        """Returns string function"""
        return self.__str__()

    def __str__(self):
        """Returns string representation of BaseModel"""

        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def to_dict(self):
        """Returns the dictionary of BaseModel"""

        cdict = dict(self.__dict__)
        cdict['created_at'] = self.created_at.isoformat()
        cdict['updated_at'] = self.updated_at.isoformat()
        cdict['__class__'] = str(self.__class__.__name__)
        return cdict

