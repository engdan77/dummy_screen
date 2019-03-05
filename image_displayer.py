import Tkinter as tkinter
from PIL import Image
import sys


def convert_png_to_gif(input_png):
    im = Image.open(input_png)
    im.save(input_png.replace('.png', '.gif'))


def quit_ui(*args):
    print args
    sys.exit(0)


def callback():
    print("click!")


def run():
    IMAGE ='./image.png'
    convert_png_to_gif(IMAGE)
    root = tkinter.Tk()
    root.configure(background="black")

    canvas = tkinter.Canvas(root)
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    canvas.configure(background='black')

    img_file = tkinter.PhotoImage(file=IMAGE.replace('.png', '.gif'))
    img = canvas.create_image(0,0, anchor="nw", image=img_file)

    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", quit_ui)
    root.mainloop()

if __name__ == '__main__':
    run()