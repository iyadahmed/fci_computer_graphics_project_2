from enum import Enum

from tkinter import Tk, Canvas, Event, Frame, Button


class Tool(Enum):
    LINE = 1
    CIRCLE = 2


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_BACKGROUND_COLOR = "white"
FILL_COLOR = "black"
LINE_WIDTH = 2

top = Tk()
canvas = Canvas(
    top, bg=WINDOW_BACKGROUND_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT
)
canvas.pack()


lines: list[int] = []
circles: list[int] = []

tool = Tool.LINE


def select_line_tool():
    global tool
    tool = Tool.LINE
    circle_button.config(relief="raised")
    line_button.config(relief="sunken")


def select_circle_tool():
    global tool
    tool = Tool.CIRCLE
    line_button.config(relief="raised")
    circle_button.config(relief="sunken")


toolbar = Frame(top)
toolbar.pack(side="top", fill="x")

line_button = Button(toolbar, text="Line", command=select_line_tool, relief="sunken")
line_button.pack(side="left")

circle_button = Button(toolbar, text="Circle", command=select_circle_tool)
circle_button.pack(side="left")


def mouse_left_down(event: Event):
    if tool == Tool.LINE:
        line = canvas.create_line(
            event.x, event.y, event.x, event.y, fill=FILL_COLOR, width=LINE_WIDTH
        )
        lines.append(line)
    elif tool == Tool.CIRCLE:
        r = 0
        circle = canvas.create_oval(
            event.x - r,
            event.y - r,
            event.x + r,
            event.y + r,
            fill="",
            outline=FILL_COLOR,
            width=LINE_WIDTH,
        )
        circles.append(circle)


def mouse_left_move(event: Event):
    if tool == Tool.LINE:
        if len(lines) == 0:
            return
        line = lines[-1]
        canvas.coords(
            line, canvas.coords(line)[0], canvas.coords(line)[1], event.x, event.y
        )
    elif tool == Tool.CIRCLE:
        if len(circles) == 0:
            return
        circle = circles[-1]
        x_min, y_min, x_max, y_max = canvas.coords(circle)
        center = ((x_min + x_max) / 2, (y_min + y_max) / 2)

        r = ((event.x - center[0]) ** 2 + (event.y - center[1]) ** 2) ** 0.5
        canvas.coords(
            circle,
            center[0] - r,
            center[1] - r,
            center[0] + r,
            center[1] + r,
        )


canvas.bind("<Button-1>", mouse_left_down)
canvas.bind("<B1-Motion>", mouse_left_move)

top.mainloop()
