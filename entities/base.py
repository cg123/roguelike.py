#!/usr/bin/python
# -*- coding: utf-8 -*-

class Entity(object):
	'''
		Base entity type for all in-world game elements.
	'''
	def __init__(self, world, char):
		'''
			Initialize the base entity.

			world: Must be the world object the entity exists in.
			char: Should be the character to draw the entity as.

			This behavior can be changed by overriding Entity.draw().
			For an example of this, see Room.
		'''
		self.world = world
		self._pos = [0, 0]
		self.char = char
		self.attr = 0
		self.room = None
	
	def x():
		'''
			Position along the X axis.
		'''
		def fget(self):
			return self.pos[0]
		def fset(self, value):
			self.pos[0]= value
		return locals()
	x = property(**x())
	
	def y():
		'''
			Position along the Y axis.
		'''
		def fget(self):
			return self.pos[1]
		def fset(self, value):
			self.pos[1]= value
		return locals()
	y = property(**y())

	def pos():
		'''
			Position of the entity, as an (X, Y) tuple.
		'''
		def fget(self):
			return list(self._pos)
		def fset(self, value):
			# Clamp to the bounds of the world.
			# A 1-cell buffer is kept around the whole world
			# as a safety and debugging measure.
			self._pos[0] = max(min(value[0], self.world.dims[0]-1), 1)
			self._pos[1] = max(min(value[1], self.world.dims[1]-1), 1)
			if (not self.room) or (not self.room.contains(*value)):
				if self.room and self in self.room.entities:
					self.room.entities.remove(self)
				self.room = self.world.which_room(*value)
				if self.room:
					self.room.entities.add(self)
		return locals()
	pos = property(**pos())

	def draw(self, pad):
		'''
			Draws the entity.

			pad: The curses pad the world is drawn onto.
		'''
		pad.addch(self.pos[1], self.pos[0], self.char, self.attr)