import Tkinter as tk
from PIL import Image
import sys
from io import BytesIO
import StringIO
from base64 import b64decode
from jsonsocket import Server
import logging
import Queue
import time
import threading
import os
import argparse

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M', level=logging.DEBUG)

method_mapper = {'text': 'display_text',
                 'image': 'display_image'}

def get_image_data(input_file=None, base64_data=None, input_format='png', workdir='./'):
    if input_file:
        io_in = BytesIO(open(input_file, 'rb').read())
    elif base64_data:
        io_in = StringIO(b64decode(base64_data))
    image = Image.open(io_in)
    filename = workdir + 'tmp.gif'
    image.save(filename)
    return filename


def startJsonServer(queue_object, port=9999, host='0.0.0.0'):
    server = Server(host, port)
    while True:
        data = server.accept().recv()
        if not data:
            server.send({'status': 'error', 'message': 'not valid json'})
        else:
            server.send({'status': 'ok'})
            queue_object.put(data)


def queue_watcher(queue_object, window_object, key_method_mapper, delay=2):
    while True:
        queue_items = list(queue_object.queue)
        if len(queue_items) > 0:
            logging.info('queue: %s' % (queue_items,))
            if 'exit' in [item.get('command', None) for item in queue_items if type(item) is dict]:
                logging.info('exiting')
                os._exit(0)
                break
            q = queue_object.get()
            logging.info('getting next in queue %s' % (q,))
            for k in q.keys():
                method_name = key_method_mapper.get(k, None)
                if method_name:
                    logging.info('executing method %s with args %s' % (method_name, q[k]))
                    found_method = getattr(locals()['window_object'], method_name)
                    found_method(**q[k])
        time.sleep(delay)


class MyWindow:
    def __init__(self, root, queue_object, workdir='./'):
        self.q = queue_object
        self.root = root
        self.root.configure(background="black")
        self.workdir = workdir

    def display_image(self, image_file=None, base64_data=None):
        if image_file:
            # convert to gif
            image_file = get_image_data(input_file=image_file, workdir=self.workdir)
        if base64_data:
            image_file = self.workdir + 'tmp.png'
            with open(image_file, 'w') as f:
                f.write(b64decode(base64_data))
            image_file = get_image_data(input_file=image_file, workdir=self.workdir)
        # display image
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
        # self.root.bind("<Escape>", self.quit_ui)
        self.root.bind("<Escape>", self.quit_ui)


    def display_text(self, input_text='', font_size=180, width=450, heigth=100):
        w = str(width)
        h = str(heigth)
        self.root.geometry('%sx%s' % (w,h))
        label = tk.Label(self.root, text=input_text, background='black', foreground='white')
        label.config(font=('courier', font_size, 'bold'))
        label.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def quit_ui(self, *args):
        self.q.put({"command": "exit"})
        # os._exit(0)
        # sys.exit(0)

    def clear(self):
        list = self.root.slaves()
        for l in list:
            l.destroy()


def start_threads(theads_list):
    threads = []
    for target, args, name in theads_list:
        t = threading.Thread(target=target, args=args, name=name)
        threads.append(t)
        t.start()
    return threads

def run():
    parser = argparse.ArgumentParser(description='A very simple application for expose a json-socket server easily used for control text and images being displayed through tool such as NetCat')
    parser.add_argument('--port', default=9999, help='Which port to open for incomming connections')
    parser.add_argument('--workdir', default='./', help='Specify which path to use for temporary files, for example if you like to use a tmpfs in-memory')
    args = parser.parse_args()

    q = Queue.Queue()
    logging.info('starting')

    root = tk.Tk()
    my_window = MyWindow(root, q, args.workdir)

    # IMAGE = '/Users/edo/tmp/bubble.png'
    # my_window.display_image(image_file=IMAGE)
    # my_window.display_text('Hello\nWorld')
    # root.after(3000, my_window.clear)

    my_window.make_fullscreen()

    threads_list = ([queue_watcher, (q, my_window, method_mapper), 'queue_watcher'],
                    [startJsonServer, (q, args.port), 'jsonServer'])
    start_threads(threads_list)

    root.mainloop()


if __name__ == '__main__':
    run()