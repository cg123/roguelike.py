#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base import Entity

class Room(Entity):
	'''
		Represents a space that can be walked on in the game world.
	'''
	def __init__(self, world, x, y, w, h):
		'''
			Construct a new room.

			x, y: Position of the top left corner of the room
			w: Room width
			h: Room height
		'''
		super(Room, self).__init__(world, '')
		self.pos = [x, y]
		self.size = [w, h]
		self.openings = set()
		self.entities = set()
	
	def add_opening(self, x, y):
		self.openings.add((x, y))

	def w():
		'''
			The width of the room.
		'''
		def fget(self):
			return self.size[0]
		def fset(self, value):
			self.size[0] = value
		return locals()
	w = property(**w())
	def h():
		'''
			The height of the room.
		'''
		def fget(self):
			return self.size[1]
		def fset(self, value):
			self.size[1] = value
		return locals()
	h = property(**h())

	def draw(self, pad):
		'''
			Draws the room into the world.
		'''
		# Draw walls
		for x in range(self.x-1, self.x + self.size[0]+1):
			pad.addch(self.y-1, x, '-')
			pad.addch(self.y + self.size[1], x, '-')
		for y in range(self.y, self.y + self.size[1]):
			pad.addch(y, self.x-1, '|')
			pad.addch(y, self.x+self.size[0], '|')
		# Draw floor
		for x in range(self.x, self.x + self.size[0]):
			for y in range(self.y, self.y + self.size[1]):
				pad.addch(y, x, '.', 0)
		for (x, y) in self.openings:
			pad.addch(y, x, '.', 0)
	
	def contains(self, x, y):
		'''
			Determine if a given location is within the room.

			Returns True or False.
		'''
		return ((x >= self.x and x < self.x + self.size[0] and
				 y >= self.y and y < self.y + self.size[1]) or 
			    (x, y) in self.openings)
	def entity_at(self, x, y):
		'''
			Find the entity at the given location.

			Return None if there is no such entity.
		'''
		for ent in self.entities:
			if ent.pos == (x, y):
				return ent
		return None

