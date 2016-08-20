#!/usr/bin/env python2

import curses, os, sys, traceback
from curses import panel as panels

# GLOBALS
parent_window = None
center_popup = None
offset_panel = None
hex_panel = None
ascii_panel = None
offset_window = None
hex_window = None
ascii_window = None

cursor_x = 0
cursor_y = 0
editor_windows_top = 0
editor_windows_bottom = 0
offset_window_originX = 0
hex_window_originX = 0
ascii_window_originX = 0
offset_window_width = 0
hex_window_width = 0
ascii_window_width = 0

current_mode = 'file_open'
buf_changed = False

def main():
	init()
	draw_editor()
	user_input()
	close()

def init():
	global parent_window

	parent_window = curses.initscr()
	curses.cbreak()
	curses.noecho()
	parent_window.keypad(1)

	init_colors()
	init_editor()

def init_colors():
	global offset_window, hex_window, ascii_window
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_RED, -1)
	curses.init_pair(2, curses.COLOR_YELLOW, -1)
	curses.init_pair(3, curses.COLOR_GREEN, -1)

def init_editor():
	global editor_windows_top, editor_windows_bottom
	global offset_panel, offset_window, offset_window_width, offset_window_originX
	global hex_panel, hex_window, hex_window_width, hex_window_originX
	global ascii_panel, ascii_window, ascii_window_width, hex_window_originX

	max_height = parent_window.getmaxyx()[0]
	max_width = parent_window.getmaxyx()[1]

	offset_window_width = 14
	new_width = max_width - 8
	ascii_window_width = int(round((new_width - offset_window_width)/4))
	hex_window_width = ascii_window_width * 3

	editor_windows_top = 2
	editor_windows_bottom = max_height - 5

	offset_window_originX = 0
	hex_window_originX = offset_window_width + 2
	ascii_window_originX = hex_window_width + offset_window_width + 4 + 2 # 4 = hex_window padding L+R, 2 = ascii_window padding L

	offset_window = curses.newwin(editor_windows_bottom, offset_window_width, editor_windows_top, 0)
	hex_window = curses.newwin(editor_windows_bottom, hex_window_width + 4, editor_windows_top, offset_window_width) # 4 = hex_window padding L+R
	ascii_window = curses.newwin(editor_windows_bottom, ascii_window_width + 4, editor_windows_top, hex_window_width + offset_window_width + 4) # 4 = ascii_window padding L+R, hex_window padding L+R

	offset_window.bkgd(' ', curses.color_pair(2))
	hex_window.bkgd(' ', curses.color_pair(0))
	ascii_window.bkgd(' ', curses.color_pair(0))

	offset_panel = panels.new_panel(offset_window)
	hex_panel = panels.new_panel(hex_window)
	ascii_panel = panels.new_panel(ascii_window)

def draw_editor():
	[window.box() for window in [offset_window, hex_window, ascii_window]]
	# for window in [offset_window, hex_window, ascii_window]:
	# 	window.box()
	# 	window.refresh()
	panels.update_panels()
	curses.doupdate()

def user_input():
	global parent_window
	parent_window.getch()

def close():
	global parent_window
	parent_window.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()

main()
