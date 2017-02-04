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

# def format_hex():
# 	global width
# 	value = ''
# 	offset = 0
# 	addr_prefix = '0x%s | '
# 	lines = get_lines()
# 	for line in lines:
# 		ascii_line = ''
# 		hex_line = ''
# 		for byte in line:
# 			if int(byte.encode('hex'), 16) > 0x19 and int(byte.encode('hex'), 16) < 0x7e:
# 				ascii_line += byte
# 			else:
# 				ascii_line += '.' # Not displayable
# 			hex_line += '%s ' % byte.encode('hex')
# 		if len(hex_line) < width*3:
# 			hex_line += ' '*(width*3-len(hex_line)) # Fix hex_line width
# 		if len(ascii_line) < width:
# 			ascii_line += ' '*(width-len(ascii_line)) # Fix ascii_line width
# 		value += addr_prefix % hex(offset)[2:].zfill(8) + hex_line + ' | ' + ascii_line + ' |\n'
# 		offset += len(ascii_line)
# 	return value

def buf(file, start, end):
	global disp_buffer
	if not os.path.exists(file):
		return ERROR_NOSUCHFILE
	with open(file, 'rw') as f:
		f.seek(start)
		for byte in f.read(end-start):
			disp_buffer.append(byte)

def set_byte(x, y, byte):
	global disp_buffer, mode
	if mode == "hexedit":
		x /= 3
	try:
		disp_buffer[(y*len(disp_buffer[0]))+x] = chr(byte)
	except:
		close_screen()
		print "%s %d %s" % (hex(byte), byte, str(byte))
