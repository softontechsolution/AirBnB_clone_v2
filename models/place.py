#!/usr/bin/python3
from os import getenv
import models
from models.review import Review
from sqlalchemy import (Column, String, ForeignKey, Float, Integer)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

"""Defines the Place class"""


class Place(BaseModel, Base):
    """Place class is a subclass of BaseModel"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities_id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users_id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') != 'db':
	@property
	def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list
