#!/usr/bin/python3
""" This script defines the BaseModel. """

import models
import uuid
from datetime import datetime


class BaseModel:
    """ Defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """ Initializes the BaseModel attributes """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        value = datetime.strptime(
                                value, '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """ String representation of objects """
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ Updates the updated_at attribute to current time """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all
        keys/values of __dict__ of the instance"""
        data = self.__dict__.copy()
        data['__class__'] = self.__class__.__name__
        data['updated_at'] = self.updated_at.isoformat()
        data['id'] = self.id
        data['created_at'] = self.created_at.isoformat()
        return data
