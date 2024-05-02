#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
"""Defines the Amenity class"""


class Amenity(BaseModel, Base):
    """Amenity class inherits from BaseModel"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity')
