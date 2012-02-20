#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
roguelike.py

2/19/2012
Charles O. Goddard

Crude implementation of a silly roguelike-like game.
'''

import curses
import time

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
				self.room = self.world.which_room(*value)
		return locals()
	pos = property(**pos())

	def draw(self, pad):
		'''
			Draws the entity.

			pad: The curses pad the world is drawn onto.
		'''
		pad.addch(self.pos[1], self.pos[0], self.char, self.attr)

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

class World(object):
	'''
		Represents the entirety of the game world. All of it.
	'''
	def __init__(self, stdscr, w, h):
		'''
			Create a new world.

			stdscr: The curses screen to draw to.
			w, h: The size of the game world.
		'''
		self.stdscr = stdscr

		self.dims = (w, h)
		self.rooms = []

		self.player = Player(self)
		self.entities = [self.player]

		self.world = curses.newpad(h+1, w+1)
		self.world.bkgd(' ')
	
	def do_walk(self, key):
		'''
			Given a key input, move the player in the appropriate
			direction.
		'''
		newPos = self.player.pos
		if key == ord('w'):
			newPos[1] -= 1
		elif key == ord('a'):
			newPos[0] -= 1
		elif key == ord('s'):
			newPos[1] += 1
		elif key == ord('d'):
			newPos[0] += 1
		if self.player.can_walk(*newPos):
			self.player.pos = newPos
			#self.player.room = self.which_room(*newPos)

	def do_keyboard(self):
		'''
			Read from the keyboard and act on inputs.
		'''
		c = self.stdscr.getch()
		if c < 0:
			return
		
		# Right now the only thing the keyboard does is make the player
		# walk around.
		if c in map(ord, 'wasd'):
			self.do_walk(c)

	def can_walk(self, x, y):
		'''
			Determine if a location is walkable by the player.
		'''
		return self.which_room(x, y) is not None
	
	def which_room(self, x, y):
		'''
			Return the room containing a given location.

			If there is no such room, return None.
		'''
		for room in self.rooms:
			if room.contains(x, y):
				return room
		return None

	def draw(self):
		'''
			Draw the game world to the screen.
		'''
		# Find how much real estate we have
		screen_h, screen_w = self.stdscr.getmaxyx()
		game_w, game_h = self.dims

		# Don't draw bigger than the screen or the game world
		win_w = min(game_w, screen_w)-1
		win_h = min(game_h, screen_h)-1

		# Center the view in the terminal
		x = (screen_w - win_w) / 2
		y = (screen_h - win_h) / 2

		ply = self.player
		# Try to center the view on the player, but not too hard.
		# X position
		game_x = ply.x - win_w / 2
		if game_x < 0:
			game_x = 0
		elif game_x + win_w >= game_w:
			game_x = game_w - win_w - 1
		# Y positon
		game_y = ply.y - win_h / 2
		if game_y < 0:
			game_y = 0
		elif game_y + win_h >= game_h:
			game_y = game_h - win_h - 1

		# Draw the world to the terminal
		self.world.refresh(game_y, game_x, y, x, y+win_h, x+win_w)

	def update(self):
		'''
			Update and draw the world.
		'''
		ply, world = self.player, self.world
		world.addch(ply.y, ply.x, ' ', 0)

		# Update things
		self.do_keyboard()

		# Draw the world to the pad
		# Rooms first, because they go behind stuff.
		for room in self.rooms:
			room.draw(self.world)
		for ent in self.entities:
			ent.draw(self.world)
		
		# Draw to the screen
		self.draw()

# Bootstrapping
def game(stdscr):
	curses.curs_set(0)
	stdscr.nodelay(1)

	world = World(stdscr, 160, 80)
	room1 = Room(world, world.dims[0]/2-4,world.dims[1]/2-4,8,10)
	room2 = Room(world, room1.x + room1.w + 1, room1.y + room1.h - 1, 10, 1)
	room1.add_opening(room1.x + room1.w, room1.y + room1.h - 1)
	room2.add_opening(room1.x + room1.w, room1.y + room1.h - 1)
	world.rooms = [room1, room2]
	world.player.room = room1
	while True:
		world.update()
		time.sleep(1/60.0)

def main():
	curses.wrapper(game)
if __name__=='__main__':
	main()
