#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Charles O. Goddard
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

