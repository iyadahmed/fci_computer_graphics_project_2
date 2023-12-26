from tkinter import Tk, Canvas, Event

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_BACKGROUND_COLOR = "white"

top = Tk()
canvas = Canvas(
    top, bg=WINDOW_BACKGROUND_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT
)
canvas.pack()


lines: list[int] = []


def mouse_left_down(event: Event):
    line = canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)
    lines.append(line)


def mouse_left_move(event: Event):
    if len(lines) == 0:
        return
    line = lines[-1]
    canvas.coords(
        line, canvas.coords(line)[0], canvas.coords(line)[1], event.x, event.y
    )


canvas.bind("<Button-1>", mouse_left_down)
canvas.bind("<B1-Motion>", mouse_left_move)

top.mainloop()
