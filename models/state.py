#!/usr/bin/python3
""" Defines the State module"""
from os import environ
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ Represents a state for a MySQL database.
        inherits from SQLAlchemy Base and links to the MySQL table states.
        Attributes:
            __tablename__ (str): name of the MySQL table to store states.
            name (sqlalchemy String): state name
            state_id: (sqlalchemy String): state id
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    """ For DBStorage """
    if environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship(
                "City", backref="state", cascade="all, delete-orphan")

    # For FileStorage """
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns list of city instances
            with state_id equals to the current State_i
            """
            from models.city import City
            from models import storage

            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
