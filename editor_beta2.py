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
filename = ""
file_changed = False

def setup_colors():
	global offset_window, hex_window, ascii_window
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_RED, -1)
	curses.init_pair(2, curses.COLOR_YELLOW, -1)
	curses.init_pair(3, curses.COLOR_GREEN, -1)
	offset_window.bkgd(' ', curses.color_pair(2))
	hex_window.bkgd(' ', curses.color_pair(0))
	ascii_window.bkgd(' ', curses.color_pair(0))
	focus_hex()

def focus_hex():
	global mode, ascii_window, hex_window, x
	ascii_window.bkgd(' ', 0)
	hex_window.bkgd(' ', curses.color_pair(3))
	mode = 'hexedit'
	x = x*3

def focus_ascii():
	global mode, ascii_window, hex_window, x
	hex_window.bkgd(' ', 0)
	ascii_window.bkgd(' ', curses.color_pair(3))
	mode = 'asciiedit'
	x = x/3

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
	global screen, hex_window, editor_top, editor_bottom, x, y, mode, disp_buffer
	buf = get_hex()
	key = screen.getch()
	if key == 27: # ESC
		mod = screen.getch()
		if mod == 27:
			sys.exit(0)
		elif mod == ord("s"):
			save_file()
		else:
			pass
	elif key == 9: # vertical tab
		if mode == 'hexedit':
			focus_ascii()
		else:
			focus_hex()
	elif key == 261: # right
		# if (mode == 'hexedit' and x < hex_width-2) or (mode == 'asciiedit' and x < ascii_width-1):
		cursor_right(1)
	elif key == 260: # left
		# if (mode == 'hexedit' and x > hex_window_originX) or (mode == 'asciiedit' and x > ascii_window_originX):
		cursor_left(1)
	elif key == 259 and y > 0: # DOWN
		cursor_down(1)
	elif key == 258 and y < len(buf)-1: # UP
		cursor_up(1)

	elif key < 255: # editing
		update_cursor()
		if mode == 'hexedit' and chr(key) in '0123456789abcdef':
			# focus_ascii()

			# 44 (hex)
			# 4*16 + 4*1
			# 4*16 case
			# 0x44 = 0b1000100
			# AND with 0b1111 = 0100 (got rid of first digit)
			# + "add" int(key)*16
			# 4*1 case
			# AND with 0b1111<<4
			#
			# GOAL: indentify whether the cursor is on 16s digit or 1s digit.

			hex_window.addstr(40, 5, 'hexedit x%d y%d or disp_buffer[%d]: %s' % (x, y, (y*len(buf[0]))+x/3, hex(ord(disp_buffer[(y*len(buf[0]))+x/3]))))
			digit16 = (x%3==0)
			byte = ord(disp_buffer[(y*len(buf[0]))+x/3])
			# hex_window.addstr(41, 5, "key: " + hex(key))
			# hex_window.addstr(42, 5, str(digit16) + "       ")
			# hex_window.addstr(43, 5, hex(byte)+" or "+str(byte)+"       ")
			if digit16:
				byte &= 0xf
				byte += int(chr(key), 16)*0x10
			else:
				byte &= 0xf0
				byte += int(chr(key), 16)*0x1
			# hex_window.addstr(44, 5, hex(byte)+" or "+str(byte)+"       ")
			set_byte(x, y, byte)

			# focus_hex()
			cursor_right(1)
		elif mode == 'asciiedit':
			if (chr(key).isalnum() or chr(key) in '!@#$%^&*()_+-=~`,./;<>?:"\'[]{}\\| '):
				# focus_hex()
				disp_buffer[(y*len(buf[0]))+x] = chr(key)
				# focus_ascii()
				hex_window.addstr(40, 5, 'wrote %s to asciiedit x%d y%d or disp_buffer[%d]' % (chr(key), x, y, (y*len(buf[0]))+x))
				cursor_right(1)
			elif (chr(key) in "\n \r".split(" ")):
				set_byte(x, y, key)
				cursor_right(1)

	update_cursor()
	screen.addstr(0, 0, 'y: %d, x: %d, lenbufY: %d, lenbufX: %d' % (y, x, len(buf), len(buf[0])))

def update_cursor():
	global screen, hex_window_originX, hex_window_originY, ascii_window_originX, ascii_window_originY, x, y, mode
	# screen.addstr(0, 0, 'y: %d, x: %d' % (y, x))
	if mode == 'hexedit':
		screen.move(hex_window_originY+y, hex_window_originX+x)
	elif mode == 'asciiedit':
		screen.move(ascii_window_originY+y, ascii_window_originX+x)

def update_editor():
	global offset_window, hex_window, ascii_window
	offset = 0
	for number in range(len(get_hex())):
		line = get_hex()[number]
		hex_text = ''
		ascii_text = ''
		for byte in line:
			hex_text += byte + ' '
			if int(byte, 16) > 0x19 and int(byte, 16) <= 0x7e:
				ascii_text += byte.decode('hex')
			else:
				ascii_text += '.' # Not displayable
		offset_window.addstr(number+1, 2, '0x' + hex(offset)[2:].zfill(8))
		hex_window.addstr(number+1, 2, hex_text)
		ascii_window.addstr(number+1, 2, ascii_text)
		offset += len(line)


	windows = [offset_window, hex_window, ascii_window]
	for window in windows:
		window.box()
		window.refresh()

	panels.update_panels()
	curses.doupdate()

	update_cursor()


def main():
	global windows, offset_window, hex_window, ascii_window, disp_buffer, x ,y, filename
	try:
		try:
			filename = sys.argv[1]
		except:
			print "Usage: editor.py <file>"
			sys.exit(1)
		setup_screen() # create panes
		setup_colors() # configure Kolorz
		buf(filename, 0, 1000) # load 1kB from lorem_ipsum.txt
		update_editor() # display changes

		windows = [offset_window, hex_window, ascii_window]
		for window in windows:
			window.box() # Draw box
			window.refresh()

		panels.update_panels()
		curses.doupdate()

		screen.move(hex_window_originY, hex_window_originX) # set cursor to ORIGIN
		while True:
			update_editor() # refresh editor
			user_input() # input (arrows, typing, commands, etc)

		update_editor()
		close_screen()
	except SystemExit:
		close_screen()
		return
	except IOError:
		close_screen()
		print "No such file: " + sys.argv[1]
	except:
		close_screen()
		print traceback.format_exc()

#!/usr/bin/env python2

import os, sys

def cursor_right(i):
	global x, y, mode
	buf = get_hex()
	for j in range(i):
		if (mode == 'hexedit' and x < len(buf[y])*3-2) or (mode == 'asciiedit' and x < len(buf[y])-1):
			if mode == 'hexedit' and (x+2)%3 == 0:
				x += 2
			else:
				x += 1
		elif y < len(buf)-1:
			x = 0
			y += 1
	update_cursor()

def cursor_left(i):
	global x, y, mode
	buf = get_hex()
	for j in range(i):
		if x > 0:
			if mode == 'hexedit' and (x)%3 == 0:
				x -= 2
			else:
				x -= 1
		elif y > 0:
			if mode == 'hexedit':
				x = len(buf[y-1])*3-2
			else:
				x = len(buf[y-1])-1
			y -= 1
	update_cursor()

def cursor_down(i):
	global x, y
	for j in range(i):
		y -= 1
	update_cursor()

def cursor_up(i):
	global x, y, mode
	buf = get_hex()
	for j in range(i):
		if (mode == 'hexedit' and x < len(buf[y+1]*3)-1) or (mode == 'asciiedit' and x < len(buf[y+1])):# editor_bottom-3:
			y += 1


#!/usr/bin/env python2

import os, sys

# CONSTANTS
ERROR_OTHER = 1
ERROR_NOSUCHFILE = 2
ERROR_READ = 3
ERROR_WRITE = 4

# GLOBALS
disp_buffer = [] # What gets shown
hex_width = 0 # 24 bytes per line
ascii_width = 0 # 24 bytes per line

def read_bytes(file, start, end):
	try:
		file.seek(start)
		return file.read(end - start)
	except IOError:
		return ERROR_READ

def get_lines(): # returns lines of length `width`
	global disp_buffer, ascii_width
	line = ''
	lines = []
	column = 0
	for byte in disp_buffer:
		line += byte
		column += 1
		if column == ascii_width:
			lines.append(line)
			line = ''
			column = 0
	if len(line) > 0:
		lines.append(line)
	return lines

def get_hex():
	value = []
	for line in get_lines():
		hex_line = []
		for char in line:
			hex_line.append(char.encode('hex'))
		value.append(hex_line)
	return value

def buf(file, start, end):
	global disp_buffer
	if not os.path.exists(file):
		return ERROR_NOSUCHFILE
	with open(file, 'rw') as f:
		f.seek(start)
		for byte in f.read(end-start):
			disp_buffer.append(byte)

def set_byte(x, y, byte):
	global disp_buffer, mode, screen
	if mode == "hexedit":
		x /= 3
	try:
		max_height = screen.getmaxyx()[0]
		max_width = screen.getmaxyx()[1]
		offset_width = 14
		new_width = max_width - 8
		ascii_width = int(round((new_width - offset_width)/4))
		disp_buffer[(y*(ascii_width))+x] = chr(byte)
	except:
		close_screen()
		print "%s %d %s" % (hex(byte), byte, str(byte))

def save_file():
	global disp_buffer, filename
	with open(filename, "w") as f:
		f.write(bytearray(disp_buffer))

main()
