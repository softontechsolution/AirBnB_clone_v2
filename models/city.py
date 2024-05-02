#!/usr/bin/python3
""" Defines the City class """
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ Represents the city class for a MySQL database
    Attributes:
        __tablename__ (str): represents the table name, cities
        name(sqlalchemy String): represents city name (128 characters)
        state_id(sqlalchemy String): represents City state_id (60 characters)
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete-orphan")
