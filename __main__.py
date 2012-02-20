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

from world import World
from entities import Room

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
