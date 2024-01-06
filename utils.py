import bpy
import mathutils

from enum import Enum, auto
import keyword
import re
from typing import Tuple

IMAGE_DIR_NAME = "imgs"

#node input sockets that are messy to set default values for
dont_set_defaults = {'NodeSocketGeometry',
                     'NodeSocketShader',
                     'NodeSocketVirtual'}

class ST(Enum):
    """
    Settings Types
    """
    # Primitives
    ENUM = auto()
    ENUM_SET = auto()
    STRING = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    VEC1 = auto()
    VEC2 = auto()
    VEC3 = auto()
    VEC4 = auto()
    COLOR = auto()

    # Special settings
    COLOR_RAMP = auto()
    CURVE_MAPPING = auto()

    # Asset Library
    MATERIAL = auto() # Handle with asset library
    OBJECT = auto() # Handle with asset library

    # Image
    IMAGE = auto() #needs refactor
    IMAGE_USER = auto() #needs refactor
    MOVIE_CLIP = auto() #unimplmented

    TEXTURE = auto() #unimplemented
    TEXT = auto() #unimplemented
    SCENE = auto() #unimplemented
    PARTICLE_SYSTEM = auto() #unimplemented
    FONT = auto() #unimplemented
    MASK = auto() #unimplemented
    CRYPTOMATTE_ENTRIES = auto() #unimplemented
    IMAGE_FORMAT_SETTINGS = auto()
    FILE_SLOTS = auto()
    LAYER_SLOTS = auto() #unimplemented

def clean_string(string: str, lower: bool = True) -> str:
    """
    Cleans up a string for use as a variable or file name

    Parameters:
    string (str): The input string
    
    Returns:
    string (str): The input string ready to be used as a variable/file
    """

    if lower:
        string = string.lower()
    string = re.sub(r"[^a-zA-Z0-9_]", '_', string)

    if keyword.iskeyword(string):
        string = "_" + string
    elif not (string[0].isalpha() or string[0] == '_'):
        string = "_" + string

    return string

def enum_to_py_str(enum: str) -> str:
    """
    Converts an enum into a string usuable in the add-on

    Parameters:
    enum (str): enum to be converted

    Returns:
    (str): converted string
    """
    return f"\'{enum}\'"
    
def str_to_py_str(string: str) -> str:
    """
    Converts a regular string into one usuable in the add-on

    Parameters:
    string (str): string to be converted

    Returns:
    (str): converted string
    """
    return f"\"{string}\""

def vec1_to_py_str(vec1) -> str:
    """
    Converts a 1D vector to a string usable by the add-on

    Parameters:
    vec1: a 1d vector

    Returns:
    (str): string representation of the vector
    """
    return f"[{vec1[0]}]"

def vec2_to_py_str(vec2) -> str:
    """
    Converts a 2D vector to a string usable by the add-on

    Parameters:
    vec2: a 2D vector

    Returns:
    (str): string representation of the vector
    """
    return f"({vec2[0]}, {vec2[1]})"

def vec3_to_py_str(vec3) -> str:
    """
    Converts a 3D vector to a string usable by the add-on

    Parameters:
    vec3: a 3d vector

    Returns:
    (str): string representation of the vector
    """
    return f"({vec3[0]}, {vec3[1]}, {vec3[2]})"

def vec4_to_py_str(vec4) -> str:
    """
    Converts a 4D vector to a string usable by the add-on

    Parameters:
    vec4: a 4d vector

    Returns:
    (str): string version
    """
    return f"({vec4[0]}, {vec4[1]}, {vec4[2]}, {vec4[3]})"

def color_to_py_str(color: mathutils.Color) -> str:
    """
    Converts a mathutils.Color into a string

    Parameters:
    color (mathutils.Color): a Blender color

    Returns:
    (str): string version
    """
    return f"mathutils.Color(({color.r}, {color.g}, {color.b}))"

def img_to_py_str(img : bpy.types.Image) -> str:
    """
    Converts a Blender image into its string

    Paramters:
    img (bpy.types.Image): a Blender image
    
    Returns:
    (str): string version
    """
    name = img.name.split('.', 1)[0]
    format = img.file_format.lower()
    return f"{name}.{format}"

#TODO: reconsider node tree definitions within node tree definitions
def make_indents(level: int) -> Tuple[str, str]:
    """
    Returns strings with the correct number of indentations 
    given the level in the function.

    Node groups need processed recursively, 
    so there can sometimes be functions in functions.

    Parameters:
    level (int): base number of indentations need

    Returns:
    outer (str): a basic level of indentation for a node group.
    inner (str): a level of indentation beyond outer
    """
    outer = "\t"*level
    inner = "\t"*(level + 1)
    return outer, inner