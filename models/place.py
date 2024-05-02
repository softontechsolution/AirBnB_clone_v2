#!/usr/bin/python3
from os import getenv
import models
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import (Column, String, ForeignKey, Float, Integer, Table)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

"""Defines the Place class"""

association_table = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))


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
	amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
	amenity_ids = []

	if getenv('HBNB_TYPE_STORAGE') != 'db':
		@property
		def reviews(self):
			"""getter attribute returns the list of Review instances"""
			all_reviews = list(models.storage.all(Review).values())
			review_list = [review for review in all_reviews if review.place_id == self.id]
			return review_list

		@property
		def amenities(self):
			"""getter attribute returns the list of Amenity instances"""
			all_amenities = list(models.storage.all(Amenity).values())
			amenity_list = [amenity for amenity in all_amenities if amenity.id in self.amenity_ids]
			return amenity_list

		@amenities.setter
		def amenities(self, value):
			"""setter attribute"""
			if isinstance(value, Amenity):
				self.amenity_ids.append(value.id)
