"""
This file defines the GUI for running Karel programs.

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""
from __future__ import annotations

import importlib.util
import inspect
import os
import sys
import tkinter as tk
import traceback as tb
from time import sleep
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
from types import FrameType
from typing import Any, Callable

from .karel_canvas import DEFAULT_ICON, LIGHT_GREY, PAD_X, PAD_Y, KarelCanvas
from .karel_program import KarelException, KarelProgram


class StudentCode:
    """
    This process extracts a module from an arbitary file that contains student code.
    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    """

    def __init__(self, code_file: str) -> None:
        if not os.path.isfile(code_file):
            raise FileNotFoundError(f"{code_file} could not be found.")

        self.module_name = os.path.basename(code_file)
        if self.module_name.endswith(".py"):
            self.module_name = os.path.splitext(self.module_name)[0]

        spec = importlib.util.spec_from_file_location(
            self.module_name, os.path.abspath(code_file)
        )
        try:
            self.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.mod)  # type: ignore
        except Exception as e:
            # Handle syntax errors and only print location of error
            print(f"Syntax Error: {e}")
            print("\n".join(tb.format_exc(limit=0).split("\n")[1:]))
            sys.exit()

        # Do not proceed if the student has not defined a main function.
        if not hasattr(self.mod, "main"):
            print("Couldn't find the main() function. Are you sure you have one?")
            sys.exit()

    def __repr__(self) -> str:
        return inspect.getsource(self.mod)

    def inject_namespace(self, karel: KarelProgram) -> None:
        """
        This function is responsible for doing some Python hackery
        that associates the generic commands the student wrote in their
        file with specific commands relating to the Karel object that exists
        in the world.
        """
        functions_to_override = [
            "move",
            "turn_left",
            "pick_beeper",
            "put_beeper",
            "facing_north",
            "facing_south",
            "facing_east",
            "facing_west",
            "not_facing_north",
            "not_facing_south",
            "not_facing_east",
            "not_facing_west",
            "front_is_clear",
            "beepers_present",
            "no_beepers_present",
            "beepers_in_bag",
            "no_beepers_in_bag",
            "front_is_blocked",
            "left_is_blocked",
            "left_is_clear",
            "right_is_blocked",
            "right_is_clear",
            "paint_corner",
            "corner_color_is",
        ]
        for func in functions_to_override:
            setattr(self.mod, func, getattr(karel, func))


class KarelApplication(tk.Frame):
    def __init__(
        self,
        karel: KarelProgram,
        code_file: str,
        master: tk.Tk,
        window_width: int = 800,
        window_height: int = 600,
        canvas_width: int = 600,
        canvas_height: int = 400,
    ) -> None:
        # set window background to contrast white Karel canvas
        master.configure(background=LIGHT_GREY)

        # configure location of canvas to expand to fit window resizing
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        # set master geometry
        master.geometry(f"{window_width}x{window_height}")

        super().__init__(master, background=LIGHT_GREY)

        self.karel = karel
        self.world = karel.world
        self.student_code = StudentCode(code_file)
        self.student_code.inject_namespace(karel)
        master.title(self.student_code.module_name)
        if not self.student_code.mod:
            master.destroy()
            return
        self.icon = DEFAULT_ICON
        self.window_width = window_width
        self.window_height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.master = master
        self.set_dock_icon()
        self.inject_decorator_namespace()
        self.grid(row=0, column=0)
        self.create_menubar()
        self.create_canvas()
        self.create_buttons()
        self.create_slider()
        self.create_status_label()

    def set_dock_icon(self) -> None:
        # make Karel dock icon image
        path = os.path.join(os.path.dirname(__file__), "icon.png")
        try:
            img = tk.Image("photo", file=path)
            self.master.tk.call("wm", "iconphoto", self.master._w, img)  # type: ignore
        except Exception:
            print(f"Warning: invalid icon.png: {path}")

    def create_menubar(self) -> None:
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Exit", underline=1, command=self.master.quit, accelerator="Cmd+W"
        )
        iconmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Select Icon", menu=iconmenu)
        iconmenu.add_command(label="Karel", command=lambda: self.set_icon("karel"))
        iconmenu.add_command(label="Simple", command=lambda: self.set_icon("simple"))

        self.bind_all("<Command-w>", self.quit)
        self.master.config(menu=menubar)  # type: ignore

    def quit(self, event: tk.Event[Any]) -> None:  # type: ignore
        del event
        sys.exit(0)

    def set_icon(self, icon: str) -> None:
        self.canvas.icon = icon
        self.canvas.redraw_karel()

    def create_slider(self) -> None:
        """
        This method creates a frame containing three widgets:
        two labels on either side of a scale slider to control
        Karel execution speed.
        """
        self.slider_frame = tk.Frame(self, bg=LIGHT_GREY)
        self.slider_frame.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

        self.fast_label = tk.Label(self.slider_frame, text="Fast", bg=LIGHT_GREY)
        self.fast_label.pack(side="right")

        self.slow_label = tk.Label(self.slider_frame, text="Slow", bg=LIGHT_GREY)
        self.slow_label.pack(side="left")

        self.speed = tk.DoubleVar()

        self.scale = tk.Scale(
            self.slider_frame,
            orient=tk.HORIZONTAL,
            variable=self.speed,
            showvalue=False,
        )
        self.scale.set(self.world.init_speed)
        self.scale.pack()

    def create_canvas(self) -> None:
        """ This method creates the canvas on which Karel and the world are drawn. """
        self.canvas = KarelCanvas(
            self.canvas_width,
            self.canvas_height,
            self.master,
            world=self.world,
            karel=self.karel,
        )
        self.canvas.grid(column=1, row=0, sticky="NESW")
        self.canvas.bind("<Configure>", lambda t: self.canvas.redraw_all())

    def create_buttons(self) -> None:
        """
        This method creates the three buttons that appear on the left
        side of the screen. These buttons control the start of Karel
        execution, resetting Karel's state, and loading new worlds.
        """
        self.program_control_button = tk.Button(
            self, highlightthickness=0, highlightbackground="white"
        )
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
        self.program_control_button.grid(
            column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

        self.load_world_button = tk.Button(
            self, highlightthickness=0, text="Load World", command=self.load_world
        )
        self.load_world_button.grid(
            column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

    def create_status_label(self) -> None:
        """ This function creates the status label at the bottom of the window. """
        self.status_label = tk.Label(
            self.master, text="Welcome to Karel!", bg=LIGHT_GREY
        )
        self.status_label.grid(row=1, column=0, columnspan=2)

    def karel_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper() -> None:
            # execute Karel function
            karel_fn()
            # redraw canvas with updated state of the world
            self.canvas.redraw_karel()
            # delay by specified amount
            sleep(1 - self.speed.get() / 100)

        return wrapper

    def beeper_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper() -> None:
            # execute Karel function
            karel_fn()
            # redraw canvas with updated state of the world
            self.canvas.redraw_beepers()
            self.canvas.redraw_karel()
            # delay by specified amount
            sleep(1 - self.speed.get() / 100)

        return wrapper

    def corner_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper(color: str) -> None:
            # execute Karel function
            karel_fn(color)
            # redraw canvas with updated state of the world
            self.canvas.redraw_corners()
            self.canvas.redraw_beepers()
            self.canvas.redraw_karel()
            # delay by specified amount
            sleep(1 - self.speed.get() / 100)

        return wrapper

    def inject_decorator_namespace(self) -> None:
        """
        This function is responsible for doing some Python hackery
        that associates the generic commands the student wrote in their
        file with specific commands relating to the Karel object that exists
        in the world.
        """
        self.student_code.mod.turn_left = self.karel_action_decorator(  # type: ignore
            self.karel.turn_left
        )
        self.student_code.mod.move = self.karel_action_decorator(  # type: ignore
            self.karel.move
        )
        self.student_code.mod.pick_beeper = (  # type: ignore
            self.beeper_action_decorator(self.karel.pick_beeper)
        )
        self.student_code.mod.put_beeper = self.beeper_action_decorator(  # type: ignore
            self.karel.put_beeper
        )
        self.student_code.mod.paint_corner = (  # type: ignore
            self.corner_action_decorator(self.karel.paint_corner)
        )

    def disable_buttons(self) -> None:
        self.program_control_button.configure(state="disabled")
        self.load_world_button.configure(state="disabled")

    def enable_buttons(self) -> None:
        self.program_control_button.configure(state="normal")
        self.load_world_button.configure(state="normal")

    def display_error_traceback(self, e: KarelException | NameError) -> None:
        print("Traceback (most recent call last):")
        display_frames: list[tuple[FrameType, int]] = []
        # walk through all the frames in stack trace at time of failure
        for frame, lineno in tb.walk_tb(e.__traceback__):
            frame_info = inspect.getframeinfo(frame)
            # get the name of the file corresponding to the current frame
            filename = frame_info.filename
            # Only display frames generated within the student's code
            if self.student_code.module_name + ".py" in filename:
                display_frames.append((frame, lineno))

        trace = tb.format_list(tb.StackSummary.extract(display_frames))  # type: ignore
        print("".join(trace).strip())
        print(f"{type(e).__name__}: {e}")

    def run_program(self) -> None:
        # Error checking for existence of main function completed in prior file
        try:
            self.status_label.configure(text="Running...", fg="brown")
            self.disable_buttons()
            self.student_code.mod.main()  # type: ignore
            self.status_label.configure(text="Finished running.", fg="green")

        except (KarelException, NameError) as e:
            # Generate popup window to let the user know their program crashed
            self.status_label.configure(
                text="Program crashed, check console for details.", fg="red"
            )
            self.display_error_traceback(e)
            self.update()
            showwarning(
                "Karel Error", "Karel Crashed!\nCheck the terminal for more details."
            )

        finally:
            # Update program control button to force user
            # to reset world before running program again
            self.program_control_button["text"] = "Reset World"
            self.program_control_button["command"] = self.reset_world
            self.enable_buttons()

    def reset_world(self) -> None:
        self.karel.reset_state()
        self.world.reset_world()
        self.canvas.redraw_all()
        self.status_label.configure(text="Reset to initial state.", fg="black")
        # Once world has been reset, program control button resets to "run" mode
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
        self.update()

    def load_world(self) -> None:
        default_worlds_path = os.path.join(os.path.dirname(__file__), "worlds")
        filename = askopenfilename(
            initialdir=default_worlds_path,
            title="Select Karel World",
            filetypes=[("Karel Worlds", "*.w")],
            parent=self.master,
        )
        # User hit cancel and did not select file, so leave world as-is
        if filename == "":
            return
        self.world.reload_world(filename=filename)
        self.karel.reset_state()
        self.canvas.redraw_all()
        # Reset speed slider
        self.scale.set(self.world.init_speed)
        self.status_label.configure(
            text=f"Loaded world from {os.path.basename(filename)}.", fg="black"
        )

        # Make sure program control button is set to 'run' mode
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
