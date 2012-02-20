#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base import Entity

class Player(Entity):
	'''
		Represents the player in the game world.
	'''
	HEALTH_MAX = 10
	def __init__(self, world):
		super(Player, self).__init__(world, '@')
		self.health = Player.HEALTH_MAX
		# Just for kicks, start the player in the middle of the world.
		self.pos = [world.dims[0]/2, world.dims[1]/2]
			
	
	def can_walk(self, x, y):
		if self.room:
			if self.room.contains(x, y):
				return True
			elif (self.x, self.y) in self.room.openings:
				return self.world.can_walk(x, y)
		return False
