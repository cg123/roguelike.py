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
	world.draw()
	while True:
		world.do_turn()
		if world.exiting:
			break
		time.sleep(1/60.0)

def main():
	curses.wrapper(game)
if __name__=='__main__':
	main()
