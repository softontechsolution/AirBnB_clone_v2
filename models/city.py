#!/usr/bin/python3
""" Defines the City class """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
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
    places = relationship("Place", backref="cities", cascade="delete")
