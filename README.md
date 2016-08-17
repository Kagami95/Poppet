# Poppet
A Curses-based Hex Editor for Linux

### Background
I was looking for a Linux terminal hex editor for quite some time, and tried a lot of them but never quite found the right one for me. That is why I decided to create Poppet.

The name "Poppet" comes from a tutorial I came across while looking for documentation on [hexcurse](https://github.com/LonnyGomes/hexcurse), which described, not how to use a hex editor, but rather how to lift a curse cast on someone (witchcraft and such). My friend and I had a good laugh, and the name stuck.

### Planned Features
Poppet was created in order to add support for all the things I couldn't do in the other terminal-based editors.
- Deleting bytes
- Easy copy/pasting
- Support for large files
- Color schemes

### Current Progress:
- Stores file descriptors in list
- Buffers only `offset <= byte < (offset+length)` (large files don't choke RAM)
- Sweet hex/ascii layout (similar to `$ hexdump -vC`)

### Pull Requests
Pull requests are welcome and encouraged, but are subject to review (as one might expect). I want this application to be useful to everyone, and to be the best available. For that, I need the community's  help.
