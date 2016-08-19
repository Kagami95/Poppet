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

def write_to_file(path):
	out = ''
	for byte in disp_buffer:
		out += byte
	with open(path, 'w') as f:
		f.write(out)
