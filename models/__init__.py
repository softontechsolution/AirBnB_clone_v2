#!/usr/bin/python3
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
"""This module instantiates an object of class FileStorage and DBstorage"""
"""Creates a unique storage instance for the application"""
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import environ

# use env to store environ var and devide storage method
env = environ["HBNB_TYPE_STORAGE"]
if env == 'db':
    storage = DBStorage()
    storage.reload()

else:
    storage = FileStorage()
    storage.reload()
