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

from entities import *
import curses
import time

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
		self.exiting = False
	
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

	def do_keyboard(self):
		'''
			Read from the keyboard and act on inputs.
		'''
		c = self.stdscr.getch()
		if c < 0:
			return False
		
		# Right now the only thing the keyboard does is make the player
		# walk around.
		if c in map(ord, 'wasd'):
			self.do_walk(c)
			return True
		elif c == ord('q'):
			self.exiting = True
			return True
		return False
	
	def do_turn(self):
		#self.draw()
		while not self.do_keyboard():
			self._draw()
			time.sleep(1/60.0)
		
		ply, world = self.player, self.world
		world.addch(ply.y, ply.x, ' ', 0)

		self.draw()

	def can_walk(self, x, y):
		'''
			Determine if a location is walkable by the player.
		'''
		r = self.which_room(x, y)
		return r is not None and r.entity_at(x, y) is None
	
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
		# Draw the world to the pad
		# Rooms first, because they go behind stuff.
		for room in self.rooms:
			room.draw(self.world)
		for ent in self.entities:
			ent.draw(self.world)
		
		# Draw to the screen
		self._draw()

	def _draw(self):
		'''
			Draw the section of the pad centered around the player to the
			viewing area.
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
