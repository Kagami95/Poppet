#!/usr/bin/env python2

import os, sys

# CONSTANTS
ERROR_OTHER = 1
ERROR_NOSUCHFILE = 2
ERROR_READ = 3
ERROR_WRITE = 4

# GLOBALS
open_files = []
disp_buffer = '' # What gets shown
width = 24-1 # 24 bytes per line

def open_file(path):
	if not os.path.exists(path):
		return ERROR_NOSUCHFILE
	open_files.append(open(path, 'rw'))

def read_bytes(file, start, end):
	try:
		file.seek(start)
		return file.read(end - start)
	except IOError:
		return ERROR_READ

def get_lines(): # returns lines of length `width`
	line = ''
	lines = []
	column = 0
	for byte in disp_buffer:
		line += byte
		column += 1
		if column == width:
			lines.append(line)
			line = ''
			column = 0
	if len(line) > 0:
		lines.append(line)
	return lines

def format_hex():
	value = ''
	offset = 0
	addr_prefix = '0x%s | '
	lines = get_lines()
	for line in lines:
		ascii_line = ''
		hex_line = ''
		for byte in line:
			if int(byte.encode('hex'), 16) > 0x19 and int(byte.encode('hex'), 16) < 0x7e:
				ascii_line += byte
			else:
				ascii_line += '.' # Not displayable
			hex_line += '%s ' % byte.encode('hex')
		if len(hex_line) < width*3:
			hex_line += ' '*(width*3-len(hex_line)) # Fix hex_line width
		if len(ascii_line) < width:
			ascii_line += ' '*(width-len(ascii_line)) # Fix ascii_line width
		value += addr_prefix % hex(offset)[2:].zfill(8) + hex_line + ' | ' + ascii_line + ' |\n'
		offset += len(ascii_line)
	return value

def exit():
	for file in open_files:
		file.close()

def run1():
	global disp_buffer
	open_file('./lorem_ipsum.txt')
	disp_buffer = read_bytes(open_files[0], 512, 2048) # start at offset 512, runs for 1536 bytes
	print format_hex()
	exit()

run1()
