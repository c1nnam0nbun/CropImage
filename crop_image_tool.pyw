from tkinter.filedialog import askopenfilename, asksaveasfilename, sys
from tkinter.messagebox import askyesno, showwarning, showinfo
from tkinter import Tk, Label, Entry, Spinbox, StringVar, OptionMenu, Button
from tkinter import W, E, END, DISABLED, NORMAL
from PIL import Image


class Config:
    def __init__(self, img=None, position=None):
        if position:
            self.position = position
        else:
            self.position = Position()
        self.img = img


class Position:
    def __init__(self, right=0, left=0, top=0, bottom=0, indent=0):
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
        self.indent = indent


root = Tk()
root.title("Create PDF from image")

config = Config()
first = True
global page_amount


# region utils
def enable_and_set_bounds():
    global config

    left_input.config(state=NORMAL, from_=0, to=config.img.size[0])
    right_input.config(state=NORMAL, from_=0, to=config.img.size[0])
    top_input.config(state=NORMAL, from_=0, to=config.img.size[1])
    bottom_input.config(state=NORMAL, from_=0, to=config.img.size[1])
    indent_input.config(state=NORMAL, from_=0, to=sys.maxsize)
    pages_input.config(state=NORMAL, from_=0, to=sys.maxsize)
    mode_menu.config(state=NORMAL)
    test_button.config(state=NORMAL)
    gen_button.config(state=NORMAL)


def warn_size(dim=None, value=None):
    if dim:
        showwarning("Wrong data", "This value should not be more than " + dim + ": " + str(value))
    else:
        showwarning("Wrong data", "This value should not be less than 0")


def update_inputs(right=None, left=None, top=None, bottom=None, indent=None):
    if right >= 0:
        right_input.delete(0, END)
        right_input.insert(END, right)
    if left >= 0:
        left_input.delete(0, END)
        left_input.insert(END, left)
    if top >= 0:
        top_input.delete(0, END)
        top_input.insert(END, top)
    if bottom >= 0:
        bottom_input.delete(0, END)
        bottom_input.insert(END, bottom)
    if indent >= 0:
        indent_input.delete(0, END)
        indent_input.insert(END, indent)


# endregion


# region set dimensions
def set_normal():
    global config

    left = 207
    right = config.img.size[0] - 191
    top = 5
    bottom = 703
    indent = 3

    config.position = Position(right, left, top, bottom, indent)

    update_inputs(right, left, top, bottom, indent)


def set_smaller():
    global config

    left = 323
    right = config.img.size[0] - 307
    top = 5
    bottom = 529
    indent = 2

    config.position = Position(right, left, top, bottom, indent)

    update_inputs(right, left, top, bottom, indent)


def set_left():
    global config

    left = 10
    right = config.img.size[0] - 387
    top = 5
    bottom = 703
    indent = 3

    config.position = Position(right, left, top, bottom, indent)

    update_inputs(right, left, top, bottom, indent)


def set_other():
    global config

    left = 257
    right = config.img.size[0] - 240
    top = 5
    bottom = 630
    indent = 2

    config.position = Position(right, left, top, bottom, indent)

    update_inputs(right, left, top, bottom, indent)


def set_custom(var):
    global config

    if str(var) == "PY_VAR1":
        config.position.left = int(var.get())
    if str(var) == "PY_VAR2":
        config.position.right = int(var.get())
    if str(var) == "PY_VAR3":
        config.position.top = int(var.get())
    if str(var) == "PY_VAR4":
        config.position.bottom = int(var.get())
    if str(var) == "PY_VAR5":
        config.position.indent = int(var.get())


def set_default():
    global config

    left = 0
    right = config.img.size[0]
    top = 0
    bottom = config.img.size[1]
    indent = 0

    config.position = Position(right, left, top, bottom, indent)

    update_inputs(right, left, top, bottom, indent)


# endregion


# region on change event handlers
def on_mode_change(*args):
    global config

    if mode.get() == "normal":
        set_normal()
    elif mode.get() == "left":
        set_left()
    elif mode.get() == "smaller":
        set_smaller()
    elif mode.get() == "other":
        set_other()
    else:
        set_default()


def on_input_change(var, *args):
    if not var.get().isdigit():
        entry_var_dict[str(var)].delete(0, END)
    elif int(var.get()) > config.img.size[0] and (str(var) == "PY_VAR1" or str(var) == "PY_VAR2"):
        warn_size("width", config.img.size[0])
        entry_var_dict[str(var)].delete(0, END)
    elif int(var.get()) > config.img.size[1] and (str(var) == "PY_VAR3" or str(var) == "PY_VAR4"):
        warn_size("height", config.img.size[1])
        entry_var_dict[str(var)].delete(0, END)
    elif int(var.get()) < 0:
        warn_size()
        entry_var_dict[str(var)].delete(0, END)
    else:
        if str(var) == "PY_VAR6":
            global page_amount
            page_amount = var.get()
        else:
            set_custom(var)


modes = {"normal", "left", "smaller", "other", "default"}
mode = StringVar(root)
mode.set("default")
mode.trace("w", on_mode_change)

lvar = StringVar(root)
lvar.trace("w", lambda *args: on_input_change(lvar, *args))

rvar = StringVar(root)
rvar.trace("w", lambda *args: on_input_change(rvar, *args))

tvar = StringVar(root)
tvar.trace_add("write", lambda *args: on_input_change(tvar, *args))

bvar = StringVar(root)
bvar.trace("w", lambda *args: on_input_change(bvar, *args))

ivar = StringVar(root)
ivar.trace("w", lambda *args: on_input_change(ivar, *args))

pvar = StringVar(root)
pvar.trace("w", lambda *args: on_input_change(pvar, *args))


# endregion


# region file processing
def get_file():
    global config, first

    input_filename = askopenfilename(title="Select", filetypes=[("image", "*.jpg *.jpeg *.png *.bmp")])

    img = Image.open(input_filename)
    config.img = img

    file_source_entry.config(state=NORMAL)
    file_source_entry.delete(0, END)
    file_source_entry.insert(END, input_filename)
    file_source_entry.config(state=DISABLED)

    enable_and_set_bounds()
    set_default()


def create_test_frames(position=None, incr=None):
    global config

    if position:
        left = position.left
        right = position.right
        top = position.top
        bottom = position.bottom
        indent = position.indent
    else:
        left = config.position.left
        right = config.position.right
        top = config.position.top
        bottom = config.position.bottom
        indent = config.position.indent

    if not incr:
        incr = bottom + indent

    slide = config.img.crop((left, top, right, bottom))
    slide.show()

    msg = askyesno("Image", "Do you like the result?")
    if not msg:
        msg = askyesno("Image", "Would you like to see next frame?")
        if msg:
            position = Position(right, left, top + incr, bottom + incr, indent)
            create_test_frames(position, incr)


def generate_pdf():
    global config, page_amount

    export_file_path = asksaveasfilename(defaultextension=".pdf")

    left = config.position.left
    right = config.position.right
    top = config.position.top
    bottom = config.position.bottom
    indent = config.position.indent

    incr = bottom + indent
    future_pdf = []
    first_page = None

    for i in range(int(page_amount)):
        slide = config.img.crop((left, top, right, bottom)).convert("RGB")
        if i == 0:
            first_page = slide
        else:
            future_pdf.append(slide)
        top += incr
        bottom += incr

    first_page.save(export_file_path, save_all=True, append_images=future_pdf)
    showinfo("File", "File successfully created!")


# endregion


# region graphical elements
mode_label = Label(root, text="Mode: ", font=("helvetica", 12))
mode_label.grid(row=1, column=0, pady=20, sticky=W)

mode_menu = OptionMenu(root, mode, *modes)
mode_menu.config(state=DISABLED)
mode_menu.grid(row=1, column=1, sticky=W + E)

file_source_label = Label(root, text="Source: ", font=("helvetica", 12))
file_source_label.grid(row=0, column=0, sticky=W)
file_source_entry = Entry(root, width=20, state=DISABLED)
file_source_entry.grid(row=0, column=1, columnspan=5, sticky=W + E)
file_source_button = Button(root, text="...", command=get_file)
file_source_button.grid(row=0, column=6, padx=10)

left_label = Label(root, text="Left: ", font=("helvetica", 12))
left_label.grid(row=2, column=0, sticky=W)
left_input = Spinbox(root, textvariable=lvar, state=DISABLED)
left_input.grid(row=2, column=1, sticky=W + E)
left_input.insert(END, config.position.left)

right_label = Label(root, text="Right: ", font=("helvetica", 12))
right_label.grid(row=2, column=3, sticky=W, padx=20)
right_input = Spinbox(root, textvariable=rvar, state=DISABLED)
right_input.grid(row=2, column=4, sticky=W + E)

top_label = Label(root, text="Top: ", font=("helvetica", 12))
top_label.grid(row=3, column=0, sticky=W)
top_input = Spinbox(root, textvariable=tvar, state=DISABLED)
top_input.grid(row=3, column=1, sticky=W + E)

bottom_label = Label(root, text="Bottom: ", font=("helvetica", 12))
bottom_label.grid(row=3, column=3, sticky=W, padx=20)
bottom_input = Spinbox(root, textvariable=bvar, state=DISABLED)
bottom_input.grid(row=3, column=4, sticky=W + E)

indent_label = Label(root, text="Indent: ", font=("helvetica", 12))
indent_label.grid(row=4, column=0, sticky=W, ipady=20)
indent_input = Spinbox(root, textvariable=ivar, state=DISABLED)
indent_input.grid(row=4, column=1, sticky=W + E)

pages_label = Label(root, text="Pages: ", font=("helvetica", 12))
pages_label.grid(row=5, column=0, sticky=W)
pages_input = Spinbox(root, textvariable=pvar, state=DISABLED)
pages_input.grid(row=5, column=1, sticky=W + E)

test_button = Button(root, text="Test", state=DISABLED, command=create_test_frames)
test_button.grid(row=6, column=4, padx=20, sticky=W + E, pady=10)
gen_button = Button(root, text="Generate PDF", state=DISABLED, command=generate_pdf)
gen_button.grid(row=6, column=5, padx=20, sticky=E)
# endregion


entry_var_dict = {
    "PY_VAR1": left_input,
    "PY_VAR2": right_input,
    "PY_VAR3": top_input,
    "PY_VAR4": bottom_input,
    "PY_VAR5": indent_input,
    "PY_VAR6": pages_input
}

root.mainloop()
