"""
hcm2py Module

This module provides functionality for [describe what your module does].

Author: HawkKing

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

## Note
The current block index is within the `index_counter`.

"""
import pyperclip
import requests
import math

string = ""
connections = ""
builds = ""
buildvalues = ""
parts = []

index_counter = 1

def createBlockCustom(string):
    items = string.split(',')
    if(len(items[5])>2):
        if(len(items[5].split("+"))>2):
            parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "r": items[5].split("+")[0], "g": items[5].split("+")[1], "b": items[5].split("+")[2]})
            return
        else:
            parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "freq": items[5]})
            return
    parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "freq": items[5]})
def createWire(start_x, start_y, start_z, end_x, end_y, end_z):
    global connections
    connections += f"{xyztoindex(start_x, start_y, start_z)},{xyztoindex(end_x, end_y, end_z)};"
def createBlock(x, y, z, part, specialparams=None):
    global index_counter
    global parts
    freq = 0

    if specialparams is not None:
        if isinstance(specialparams, (int, float)):
            if isinstance(specialparams, int) or isinstance(specialparams, float):
                r = g = b = None
                freq = specialparams
            else:
                print("Error: specialparams should be an array of 3 numbers (RGB) or a single number (frequency).")
                return
        elif len(specialparams) == 3:
            r, g, b = specialparams
            freq = None
        else:
            print("Error: specialparams should be an array of 3 numbers (RGB) or a single number (frequency).")
            return
    if part == 6:
        if r is None or g is None or b is None:
            print("Warning: Part 6 (LED) must have RGB values provided.")
        else:
            parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part, "r": r, "g": g, "b": b})
            index_counter += 1
    elif part == 7 or part == 12 or part == 13:
        if freq is None:
            print("Warning: Part 7 (Sound Block) must have Frequency value provided.")
        else:
            parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part, "freq": freq})
            index_counter += 1
    else:
        parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part})
        index_counter += 1
def xyztoindex(x, y, z):
    for item in parts:
        if item["x"] == x and item["y"] == y and item["z"] == z:
            return str(item["index"]) 
def checkForBlock(x, y, z):
    for item in parts:
        if item["x"] == x and item["y"] == y and item["z"] == z:
            return True
    return False       
def createWireIndex(index1,index2):
    global connections
    connections += str(index1)+","+str(index2)+";"
def createCustomBuilding(Type, x, y, z, rotX, rotY, rotZ, value):
    global builds
    global buildvalues
    
    types = ['Sign', 'Door', 'Graph', 'MassiveMemory', 'MassMemory', 'KeyInput', 'QwertyKeyInput']
    
    if Type in types:
        rotX_rad = math.radians(rotX)
        rotY_rad = math.radians(rotY)
        rotZ_rad = math.radians(rotZ)

        # Create the rotation matrix manually
        R00 = math.cos(rotZ_rad) * math.cos(rotY_rad)
        R01 = -math.sin(rotZ_rad) * math.cos(rotX_rad) + math.cos(rotZ_rad) * math.sin(rotY_rad) * math.sin(rotX_rad)
        R02 = math.sin(rotZ_rad) * math.sin(rotX_rad) + math.cos(rotZ_rad) * math.sin(rotY_rad) * math.cos(rotX_rad)

        R10 = math.sin(rotZ_rad) * math.cos(rotY_rad)
        R11 = math.cos(rotZ_rad) * math.cos(rotX_rad) + math.sin(rotZ_rad) * math.sin(rotY_rad) * math.sin(rotX_rad)
        R12 = -math.cos(rotZ_rad) * math.sin(rotX_rad) + math.sin(rotZ_rad) * math.sin(rotY_rad) * math.cos(rotX_rad)

        R20 = -math.sin(rotY_rad)
        R21 = math.cos(rotY_rad) * math.sin(rotX_rad)
        R22 = math.cos(rotY_rad) * math.cos(rotX_rad)

        # Create the custom building entry
        builds += f"{Type},{x},{y},{z},{R00},{R01},{R02},{R10},{R11},{R12},{R20},{R21},{R22};\n"
        buildvalues += f"{value};"
    else:
        print('Invalid Type, valid types: Sign, Door, Graph, MassiveMemory, MassMemory, KeyInput, QwertyKeyInput')
def text_to_hexadecimal(text):
    bytes_text = text.encode('utf-8')
    hexadecimal_text = bytes_text.hex()
    return hexadecimal_text
def paste_to_dpaste(content):
    dpaste_api_url = "https://dpaste.org/api/"
    payload = {
        "lexer": "python",
        "content": content
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(dpaste_api_url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        dpaste_link = response.text.strip()
        print("dpaste.org link:", dpaste_link[1:-1] + "/raw")
        return dpaste_link[1:-1] + "/raw"
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
def number_to_binary(num, numofbits):
    binary_num = bin(num)[2:]
    binary_num = binary_num.zfill(numofbits)
    return binary_num
def import_build(input_string, offset_x=0, offset_y=0, offset_z=0):
    global index_counter
    import_connections = input_string.split("?")
    import_connections = import_connections[1]
    import_connections = import_connections.split(";")
    input_string = input_string.split("?")[0]
    import_parts = input_string.split(";")
    for i in range(len(import_parts)):
        items = import_parts[i].split(",")
        parts.append({"x": int(items[2])+offset_x, "y": int(items[3])+offset_y, "z": int(items[4])+offset_z, "index": index_counter, "part": items[0]})
        index_counter+=1
    if(len(import_connections)>1):
        for i in range(len(import_connections)):
            wires = import_connections[i].split(",")
            createWireIndex(int(wires[0])+index_counter-3,int(wires[1])+index_counter-3)
def cube(x1, y1, z1, x2, y2, z2, part, specialparams=None):
    for x in range(abs(x2 - x1)):
        for y in range(abs(y2 - y1)):
            for z in range(abs(z2 - z1)):
                if specialparams:
                    createBlock(x + x1, y + y1, z + z1, part, specialparams)
                else:
                    createBlock(x + x1, y + y1, z + z1, part)
should_paste = True
def set_should_paste(bool):
    global should_paste
    should_paste=bool


for item in parts:
    if item["part"] == 6 or item["part"] == "6" or item["part"] == 14 or item["part"] == "14":
        string += f";{item['part']},0,{item['x']},{item['y']},{item['z']},{item['r']}+{item['g']}+{item['b']}"
    elif item["part"] in [7, 12, 13, "7", "12", "13"]:
        string += f";{item['part']},0,{item['x']},{item['y']},{item['z']},{item['freq']}"
    else:
        string += f";{item['part']},0,{item['x']},{item['y']},{item['z']},"

string = string[1:]
connections = connections[:-1]
builds = builds[:-1]
buildvalues = buildvalues[:-1]
string += f"?{connections}?{builds}?{buildvalues}"
if should_paste:
    pyperclip.copy(paste_to_dpaste(string))
else:  
    print("String copied to clipboard:")
    print(string)
    pyperclip.copy(string)
