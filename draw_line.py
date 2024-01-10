# https://stackoverflow.com/a/43046744/8094047
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


from enum import Enum

from tkinter import Tk, Canvas, Event, Frame, Button, Menu, filedialog


class Tool(Enum):
    LINE = 1
    CIRCLE = 2


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_BACKGROUND_COLOR = "white"
FILL_COLOR = "black"
LINE_WIDTH = 2

class App(Tk):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, bg=WINDOW_BACKGROUND_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        toolbar = Frame(self)
        toolbar.pack(side="top", fill="x")

        self.line_button = Button(toolbar, text="Line", command=self.select_line_tool, relief="sunken")
        self.line_button.pack(side="left")

        self.circle_button = Button(toolbar, text="Circle", command=self.select_circle_tool)
        self.circle_button.pack(side="left")

        self.lines: list[int] = []
        self.circles: list[int] = []

        self.tool = Tool.LINE

        self.canvas.bind("<Button-1>", self.mouse_left_down)
        self.canvas.bind("<B1-Motion>", self.mouse_left_move)

        self.menubar = Menu(self, tearoff=0)
        self.config(menu=self.menubar)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(
            label='Export Image',
            command=self.export_image,
        )
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )

    def export_image(self):
        file_types = [('PNG', '*.png'),  
         ('JPEG', '*.jpg'), 
         ('Custom Extension', '*.*')]
        output_file_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=file_types)
        if not output_file_path:
            return
        with open(output_file_path, mode="wb") as output_file:
            pass
        

    def select_line_tool(self):
        self.tool = Tool.LINE
        self.circle_button.config(relief="raised")
        self.line_button.config(relief="sunken")

    def select_circle_tool(self):
        self.tool = Tool.CIRCLE
        self.line_button.config(relief="raised")
        self.circle_button.config(relief="sunken")

    def mouse_left_down(self, event: Event):
        if self.tool == Tool.LINE:
            line = self.canvas.create_line(
                event.x, event.y, event.x, event.y, fill=FILL_COLOR, width=LINE_WIDTH
            )
            self.lines.append(line)
        elif self.tool == Tool.CIRCLE:
            r = 0
            circle = self.canvas.create_oval(
                event.x - r,
                event.y - r,
                event.x + r,
                event.y + r,
                fill="",
                outline=FILL_COLOR,
                width=LINE_WIDTH,
            )
            self.circles.append(circle)

    def mouse_left_move(self, event: Event):
        if self.tool == Tool.LINE:
            if len(self.lines) == 0:
                return
            line = self.lines[-1]
            self.canvas.coords(
                line, self.canvas.coords(line)[0], self.canvas.coords(line)[1], event.x, event.y
            )
        elif self.tool == Tool.CIRCLE:
            if len(self.circles) == 0:
                return
            circle = self.circles[-1]
            x_min, y_min, x_max, y_max = self.canvas.coords(circle)
            center = ((x_min + x_max) / 2, (y_min + y_max) / 2)

            r = ((event.x - center[0]) ** 2 + (event.y - center[1]) ** 2) ** 0.5
            self.canvas.coords(
                circle,
                center[0] - r,
                center[1] - r,
                center[0] + r,
                center[1] + r,
            )


app = App()
app.mainloop()
