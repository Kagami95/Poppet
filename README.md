# Poppet
A Curses-based Hex Editor for Linux

### Background
I was looking for a Linux terminal hex editor for quite some time, and tried a lot of them but never quite found the right one for me. That is why I decided to create Poppet.

The name "Poppet" comes from a tutorial I came across while looking for documentation on [hexcurse](https://github.com/LonnyGomes/hexcurse), which described, not how to use a hex editor, but rather how to lift a curse cast on someone by using a poppet, purple candles, and willow branches (witchcraft and such). My friend and I had a good laugh, and the name stuck.

### Ambitions
Poppet was created to do for all the things I couldn't do in the other terminal-based editors.
- Deleting bytes
- Easy copy/pasting
- Support for large files
- Color schemes

### Current Progress:
- ~~Sweet hex/ascii layout (similar to `$ hexdump -vC`)~~
- Auto-resizing editor panes (curses)
- Contained cursor (stays within bounds)
- Tab key switches from HEX editor to ASCII editor (just like hexedit, hexcurse, and dhex)
- ~~Bad color choices, bad variable names~~
- ~~MESSY CODE~~
- Creating editor_beta2.py:
	- [x] Draw editor windows
	- [x] Cleaner code
	- [x] Cursor moves

### TODO
- **[COMPLETED]** Rewrite Editor (make beta2)
- Buffer only `offset <= byte < (offset+length)` (large files don't choke RAM)
- Byte-wise cursor
- Write buffer
- Interface:
	- [ ] Window resize catching (redraw display)
	- [ ] Close file dialogue (save/discard/cancel)
	- [ ] Goto offset dialogue
	- [ ] Search for byte sequence dialogue
- Hotkeys:
	- [x] Arrow keys: move cursor *(needs rewrite)*
	- [ ] Ctrl+G: goto
	- [ ] Ctrl+F: find (search)
	- [ ] Shift+Up and Shift+Down: inc/decrement highlighted byte

### Latest Screenshots:
![screenshot](https://raw.githubusercontent.com/Kagami95/Poppet/master/latest_screenshot.png)

### Pull Requests
Pull requests are welcome and encouraged, but are subject to review (as one might expect). I want this application to be useful to everyone, and to be the best available. For that, I need the community's  help.
