# Documentation

## Block Part Numbers
- 0: not/nor
- 1: and
- 2: or
- 3: xor
- 4: input
- 5: toggle
- 6: LED
- 7: Sound
- 8: conductor

## Functions

### `finish()`
call after making all your blocks, finalizes and formats it into a string and pastes it.

### `text_to_hexadecimal(text)`
Converts ASCII text to hexadecimal for the sign.

### `xyztoindex(x, y, z)`
Takes an XYZ coordinate. If there's a block there, it gets the index of it. Mainly used in wires.

### `createBlock(x, y, z, part, specialparams=None)`
- Part: Block part ID.
- Special Params (optional): Used in special blocks like LED, sound blocks, etc. RGB values are defined by arrays, e.g., r:255, g:0, b:0 → [255, 0, 0].

### `createWire(start_x, start_y, start_z, end_x, end_y, end_z)`
Adds wires using two XYZ inputs.

### `createWireIndex(index1, index2)`
Adds wires using two index inputs.

### `number_to_binary(num, numofbits)`
Turns a number into binary.

### `import_build(input_string, offset_x=0, offset_y=0, offset_z=0)`
Puts a registry string into the build. Offsets are not mandatory.

### `createBlockCustom(string)`
Allows you to input a string like `7,0,0,0,0,1234.00` directly into the parts.

### `cube(x1, y1, z1, x2, y2, z2, part, specialparams)`
Creates an array of blocks based on two 3D points.

### `createCustomBuilding(Type, x, y, z, rotX, rotY, rotZ, value)`
Creates a custom building. Valid types: Sign, Door, Graph, MassiveMemory, MassMemory, KeyInput, QwertyKeyInput.

### `getString()`
Returns the formatted string of blocks. (wont work unless used after finish())

### `getBlocks()`
Returns the unformatted list of blocks.

### `getConnections()`
Returns the unformatted index list of connections.

### `getBuilds()`
Returns the unformatted list of builds.

### `getBuildvalues()`
Returns the unformatted list of builds values.

## Note
The current block index is within the `index_counter`.