#!/usr/bin/env python2

import curses, os, sys, traceback
from curses import panel as panels
from curses import textpad

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
hex_window_originX = 0
hex_window_originY = 0
ascii_window_originX = 0
ascii_window_originY = 0
editor_top = 0
editor_bottom = 0

mode = 'hexedit' # or 'asciiedit'

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
	global screen, editor_top, editor_bottom, offset_window, offset_panel
	global hex_width, hex_panel, hex_window, hex_window_originX, hex_window_originY
	global ascii_width, ascii_panel, ascii_window, ascii_window_originX, ascii_window_originY

	screen = curses.initscr()
	curses.cbreak()
	curses.noecho()
	screen.keypad(1)

	max_height = screen.getmaxyx()[0]
	max_width = screen.getmaxyx()[1]

	offset_width = 14
	new_width = max_width - 8
	ascii_width = int(round((new_width - offset_width)/4))
	# hex_width = int(round(3*((max_width - offset_width)/4.), 0))
	hex_width = ascii_width * 3

	editor_top = 1
	editor_bottom = max_height-5
	hex_window_originX = offset_width+2
	hex_window_originY = editor_top + 1
	ascii_window_originX = hex_width+offset_width+4+2
	ascii_window_originY = editor_top + 1

	offset_window = curses.newwin(editor_bottom, offset_width, editor_top, 0) # from y3 down to max-3, 12 columns from x0
	hex_window = curses.newwin(editor_bottom, hex_width+4, editor_top, offset_width) # from y3 down to max-3, 4/5 X starting at x12
	ascii_window = curses.newwin(editor_bottom, ascii_width+4, editor_top, hex_width+offset_width+4) # from y3 down to max-3, 1/5 X starting at 4/5 X

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
	global screen, hex_window, editor_top, editor_bottom, x, y, mode
	buf = get_hex()
	key = screen.getch()
	hex_window.addstr(30, 5, 'y: %d, x: %d, lenbufY: %d, lenbufX: %d' % (y, x, len(buf), len(buf[0])))
	if key == 27:
		sys.exit(0)
	elif key == 9:
		if mode == 'hexedit':
			mode = 'asciiedit'
			x = x/3
		else:
			mode = 'hexedit'
			x = x*3
	elif key == 261:
		# if (mode == 'hexedit' and x < hex_width-2) or (mode == 'asciiedit' and x < ascii_width-1):
		if (mode == 'hexedit' and x < len(buf[y])*3-2) or (mode == 'asciiedit' and x < len(buf[y])-1):
			if mode == 'hexedit' and (x+2)%3 == 0:
				x += 2
			else:
				x += 1
	elif key == 260:
		# if (mode == 'hexedit' and x > hex_window_originX) or (mode == 'asciiedit' and x > ascii_window_originX):
		if x > 0:
			if mode == 'hexedit' and (x)%3 == 0:
				x -= 2
			else:
				x -= 1
	elif key == 259 and y > 0:#editor_top:
		y -= 1
	elif key == 258 and y < len(buf)-1:
		if (mode == 'hexedit' and x < len(buf[y+1]*3)-1) or (mode == 'asciiedit' and x < len(buf[y+1])):# editor_bottom-3:
			y += 1
	update_cursor()

def update_editor():
	global offset_window, hex_window, ascii_window
	offset = 0
	for number in range(len(get_hex())):
		line = get_hex()[number]
		hex_text = ''
		ascii_text = ''
		for byte in line:
			hex_text += byte + ' '
			if int(byte, 16) > 0x19 and int(byte, 16) < 0x7e:
				ascii_text += byte.decode('hex')
			else:
				ascii_text += '.' # Not displayable
		offset_window.addstr(number+1, 2, '0x' + hex(offset)[2:].zfill(8))
		hex_window.addstr(number+1, 2, hex_text)
		ascii_window.addstr(number+1, 2, ascii_text)
		offset += len(line)

def update_cursor():
	global screen, hex_window_originX, hex_window_originY, ascii_window_originX, ascii_window_originY, x, y, mode
	screen.addstr(0, 0, 'y: %d, x: %d' % (y, x))
	if mode == 'hexedit':
		screen.move(hex_window_originY+y, hex_window_originX+x)
	elif mode == 'asciiedit':
		screen.move(ascii_window_originY+y, ascii_window_originX+x)

def main():
	global windows, offset_window, hex_window, ascii_window, disp_buffer, x ,y
	try:
		setup_screen()
		setup_colors()

		buf('lorem_ipsum.txt', 0, 1000)
		update_editor()

		windows = [offset_window, hex_window, ascii_window]
		for window in windows:
			window.box()
			window.refresh()

		panels.update_panels()
		curses.doupdate()

		screen.addstr(0, 0, 'y: %d, x: %d, buf height: %d, buf width: %d' % (y, x, len(get_lines()), len(get_lines()[0])))
		screen.move(hex_window_originY, hex_window_originX)
		while True:
			user_input()

		update_editor()
	except:
		close_screen()
		print traceback.format_exc()

with open('functions.py', 'r') as f:
	exec(f.read())
main()
close_screen()
