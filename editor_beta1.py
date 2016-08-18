#!/usr/bin/env python2

import curses, os, sys, traceback
from curses import panel as panels

# GLOBALS
screen = None
offset_panel = None
hex_panel = None
ascii_panel = None
offset_window = None
hex_window = None
ascii_window = None

x = 0
y = 0

def setup_colors():
	global offset_window, hex_window, ascii_window
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_RED, -1)
	curses.init_pair(2, curses.COLOR_YELLOW, -1)
	curses.init_pair(3, curses.COLOR_GREEN, -1)
	offset_window.bkgd(' ', curses.color_pair(1))
	hex_window.bkgd(' ', curses.color_pair(2))
	ascii_window.bkgd(' ', curses.color_pair(3))


def setup_screen():
	global screen, offset_window, hex_window, ascii_window, offset_panel, hex_panel, ascii_panel
	screen = curses.initscr()
	curses.cbreak()
	curses.noecho()
	screen.keypad(1)

	max_height = screen.getmaxyx()[0]
	max_width = screen.getmaxyx()[1]

	offset_width = 20
	hex_width = 4*((max_width - offset_width)/5)
	ascii_width = ((max_width - offset_width)/5)

	offset_window = curses.newwin(max_height-5, offset_width, 3, 0) # from y3 down to max-3, 12 columns from x0
	hex_window = curses.newwin(max_height-5, hex_width, 3, offset_width) # from y3 down to max-3, 4/5 X starting at x12
	ascii_window = curses.newwin(max_height-5, ascii_width, 3, hex_width+offset_width) # from y3 down to max-3, 1/5 X starting at 4/5 X

	offset_panel = panels.new_panel(offset_window)
	hex_panel = panels.new_panel(hex_window)
	ascii_panel = panels.new_panel(ascii_window)

def close_screen():
	global screen
	curses.echo()
	curses.nocbreak()
	screen.keypad(0)
	curses.endwin()

def user_input():
	global screen
	key = screen.getch()
	if key == 261 and x < screen.getmaxyx()[1]-1:
		x += 1
		xcol = 1
	elif key == 260 and x > 0:
		x -= 1
		xcol = 2
	elif key == 259 and y > 2:
		y -= 1
		ycol = 2
	elif key == 258 and y < screen.getmaxyx()[0]-3:
		y += 1
		ycol = 1

def update_editor():
	global screen
	buf(open_files[0], 0, 1000)
	screen.addstr(str(format_hex()))
	user_input()

def main():
	global windows, offset_window, hex_window, ascii_window
	try:
		setup_screen()
		setup_colors()
		windows = [offset_window, hex_window, ascii_window]
		for window in windows:
			window.addstr(0, 0, 'xxxxxxxxxxxxxxxxxx')
			window.box()
			window.refresh()

		panels.update_panels()
		curses.doupdate()
		screen.getch()

		open_file('lorem_ipsum.txt')
		# update_editor()
	except:
		close_screen()
		print traceback.format_exc()

with open('functions.py', 'r') as f:
	exec(f.read())
main()
close_screen()
close_files()
