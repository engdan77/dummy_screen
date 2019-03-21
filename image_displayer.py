import Tkinter as tk
from PIL import Image
import sys
from io import BytesIO
import StringIO
from base64 import b64decode


def get_image_data(input_file=None, base64_data=None, input_format='png'):
    if input_file:
        io_in = BytesIO(open(input_file, 'rb').read())
    elif base64_data:
        io_in = StringIO(b64decode(base64_data))
    image = Image.open(io_in)
    filename = 'tmp.gif'
    image.save(filename)
    return filename

class MyWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(background="black")

    def display_image(self, image_file):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.configure(background='black')
        self.converted_image = tk.PhotoImage(file=image_file)
        self.image_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.converted_image)
        return self.image_canvas

    def make_fullscreen(self):
        self.root.overrideredirect(True)
        self.root.overrideredirect(False)
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.quit_ui)

    def display_label(self, input_text):
        w = tk.Label(self.root, text=input_text)
        w.pack()

    def display_text(self, input_text, font_size=180, width=450, heigth=100):
        w = str(width)
        h = str(heigth)
        self.root.geometry('%sx%s' % (w,h))
        label = tk.Label(self.root, text=input_text, background='black', foreground='white')
        label.config(font=('courier', font_size, 'bold'))
        label.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def quit_ui(*args):
        print args
        sys.exit(0)

    def clear(self):
        list = self.root.slaves()
        for l in list:
            l.destroy()

def run():
    IMAGE ='./image.gif'
    image_file = get_image_data(input_file=IMAGE)
    root = tk.Tk()

    my_window = MyWindow(root)
    # my_window.display_image(image_file)
    my_window.display_text('foooo\nbaaar')
    # root.after(3000, my_window.clear)
    my_window.make_fullscreen()
    root.mainloop()


if __name__ == '__main__':
    run()