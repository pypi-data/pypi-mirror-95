"""
This file defines the necessary functions and definitions that students must
import in order to be able to write a new Karel program. Any new Karel file
must include the following line:

from stanfordkarel import *

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""
import os
import sys
import tkinter as tk

from .didyoumean import didyoumean_hook
from .karel import KarelProgram
from .karel_application import KarelApplication

sys.excepthook = didyoumean_hook
"""
The following function definitions are defined as stubs so that IDEs can recognize
the function definitions in student code. These names are re-bound upon program
execution to asscoiate their behavior to the one particular Karel object located
in a given world.
"""


def move():
    pass


def turn_left():
    pass


def put_beeper():
    pass


def pick_beeper():
    pass


def front_is_clear():
    pass


def front_is_blocked():
    pass


def left_is_clear():
    pass


def left_is_blocked():
    pass


def right_is_clear():
    pass


def right_is_blocked():
    pass


def beepers_present():
    pass


def no_beepers_present():
    pass


def beepers_in_bag():
    pass


def no_beepers_in_bag():
    pass


def facing_north():
    pass


def not_facing_north():
    pass


def facing_east():
    pass


def not_facing_east():
    pass


def facing_west():
    pass


def not_facing_west():
    pass


def facing_south():
    pass


def not_facing_south():
    pass


def paint_corner():
    pass


def corner_color_is():
    pass


# Defined constants for ease of use by students when coloring corners
RED = "red"
BLACK = "black"
CYAN = "cyan"
DARK_GRAY = "gray30"
GRAY = "gray55"
GREEN = "green"
LIGHT_GRAY = "gray80"
MAGENTA = "magenta3"
ORANGE = "orange"
PINK = "pink"
WHITE = "snow"
BLUE = "blue"
YELLOW = "yellow"
BLANK = ""


def run_karel_program(world_file=""):
    # Extract the name of the file the student is executing
    student_code_file = sys.argv[0]

    # Special case - if filename matches a specified world name,
    # Set the default world to the world with that name.
    # I personally recommend removing this functionality completely.
    if world_file == "":
        base_filename = os.path.basename(student_code_file)
        if base_filename in os.listdir(
            os.path.join(os.path.dirname(__file__), "worlds")
        ):
            world_file = os.path.splitext(base_filename)[0]

    # Create Karel and assign it to live in the newly created world
    karel = KarelProgram(world_file)

    # Initialize root Tk Window and spawn Karel application
    root = tk.Tk()
    app = KarelApplication(karel, student_code_file, master=root)
    app.mainloop()
