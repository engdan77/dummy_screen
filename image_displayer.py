import Tkinter as tkinter
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


def quit_ui(*args):
    print args
    sys.exit(0)


def callback():
    print("click!")


def run():
    IMAGE ='./image.gif'
    image_data = get_image_data(input_file=IMAGE)
    root = tkinter.Tk()
    root.configure(background="black")

    canvas = tkinter.Canvas(root)
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    canvas.configure(background='black')

    img_file = tkinter.PhotoImage(file=image_data)
    image_canvas = canvas.create_image(0, 0, anchor="nw", image=img_file)


    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", quit_ui)
    root.mainloop()

if __name__ == '__main__':
    run()