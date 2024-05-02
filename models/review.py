#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
"""Defines the Review class"""


class Review(BaseModel, Base):
    """Review class inherits from BaseModel"""
    __tablename__ = 'reviews'
    place_id = Column(String(60), ForeignKey('places_id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users_id'), nullable=False)
    text = Column(String(1024), nullable=False)
