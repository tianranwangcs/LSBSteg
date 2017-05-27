from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from Encryption import Encryption
from Decryption import Decryption
import math
import os


class Application(Frame):
    def __init__(self, master=None):
        self.file_name = ''
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def open_file(self):
        self.file_name = askopenfilename(filetypes=[('BMP File', '*.bmp')])

        # change label text dynamically
        self.name_label['text'] = 'Name: ' + self.file_name

        # clear message in msg_box
        if self.msg_box.get('1.0', END) != '':
            self.msg_box.delete('1.0', END)

        # clear image file
        # img & photo must be global or image will not show
        global left_img
        left_img = None
        global left_photo
        left_photo = None
        global right_img
        right_img = None
        global right_photo
        right_photo = None

        left_img = Image.open(self.file_name)
        w, h = left_img.size
        self.dimensions_label['text'] = 'Dimensions: ' + str(w) + 'x' + str(h)

        self.size_label['text'] = 'Size: ' + str(os.path.getsize(self.file_name)) + 'Bytes'

        # mode https://pillow.readthedocs.io/en/4.1.x/handbook/concepts.html#concept-modes
        if left_img.mode == 'L':
            self.mode_label['text'] = 'Mode: 8-Bit Pixels, Black and White'
            self.available = int((w * h) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = 'Available Size For Stega: 0 Bytes'
            else:
                self.available_label['text'] = 'Available Size For Stega: ' + str(self.available) + 'Bytes'
        elif left_img.mode == 'RGB':
            self.mode_label['text'] = 'Mode: 3x8-Bit Pixels, True Color'
            self.available = int((w * h * 3) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = 'Available Size For Stega: 0 Bytes'
            else:
                self.available_label['text'] = 'Available Size For Stega: ' + str(self.available) + 'Bytes'
        else:
            self.mode_label['text'] = 'Mode: ' + left_img.mode

        # resize img
        scale_w = img_display_width / w
        scale_h = img_display_height / h
        scale = min(scale_w, scale_h)
        new_w = math.ceil(scale * w)
        new_h = math.ceil(scale * h)
        # Image.NEAREST http://pillow.readthedocs.io/en/4.1.x/releasenotes/2.7.0.html
        left_img = left_img.resize((new_w, new_h), Image.NEAREST)

        left_photo = ImageTk.PhotoImage(left_img)

        self.left_img_canvas.create_image(img_display_width / 2, img_display_height / 2, anchor=CENTER,
                                          image=left_photo)

    def decry(self):
        if self.file_name == '':
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Please open a bitmap file first.')
            return 0
        elif self.available < 1:
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'This image is too short to hide message.')
            return 0
        else:
            decryption = Decryption(self.file_name)
            decry_msg = decryption.run()
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Hidden message: "' + decry_msg + '".')

    def encry(self):
        hide_msg = self.msg_box.get('1.0', END).replace('\n', '')
        if self.file_name == '':
            if hide_msg == '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Please open a bitmap file first.')
            return 0
        elif hide_msg == '':
            self.msg_box.insert(END, 'Input hidden message here.')
            return 0
        elif len(hide_msg) > self.available:
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Input hidden message is larger than ' + str(self.available) + ' bytes.')
            return 0
        else:
            origin_file_name = self.file_name
            # add 'hidden' to new image file name
            new_file_name = self.file_name[:-4] + '_hidden' + self.file_name[-4:]
            encryption = Encryption(origin_file_name, new_file_name, hide_msg)
            encryption.run()

            global right_img
            right_img = Image.open(self.file_name)
            w, h = right_img.size
            # resize img
            scale_w = img_display_width / w
            scale_h = img_display_height / h
            scale = min(scale_w, scale_h)
            new_w = math.ceil(scale * w)
            new_h = math.ceil(scale * h)
            img = right_img.resize((new_w, new_h), Image.NEAREST)

            global right_photo
            right_photo = ImageTk.PhotoImage(img)
            self.right_img_canvas.create_image(img_display_width / 2, img_display_height / 2, anchor=CENTER,
                                               image=right_photo)

            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Saved new file into ' + new_file_name + '.')

    def create_widgets(self):
        # do not try to use grid and pack in the same window

        # left part -----------------------------------------------------------
        left_frame = Frame(self)
        left_frame.pack(side=LEFT)

        show_frame = Frame(left_frame)
        show_frame.pack(side=TOP)

        open_frame = Frame(show_frame)
        open_frame.pack(side=TOP)

        open_label = Label(open_frame, text='Open BMP File:')
        open_label.pack(side=LEFT)

        open_button = Button(open_frame, text='Open', command=self.open_file)
        open_button.pack(side=LEFT)

        self.name_label = Label(show_frame, text='Name: ')
        self.name_label.pack(side=TOP)

        self.dimensions_label = Label(show_frame, text='Dimensions: ')
        self.dimensions_label.pack(side=TOP)

        self.size_label = Label(show_frame, text='Size: ')
        self.size_label.pack(side=TOP)

        self.mode_label = Label(show_frame, text='Available Size For Stega: ')
        self.mode_label.pack(side=TOP)

        self.available_label = Label(show_frame, text='Mode: ')
        self.available_label.pack(side=TOP)

        self.left_img_canvas = Canvas(left_frame, bg='grey', width=img_display_width, height=img_display_height)
        self.left_img_canvas.pack(side=BOTTOM)

        # right part ------------------------------------------------------
        right_frame = Frame(self)
        right_frame.pack(side=RIGHT)

        en_de_cry_frame = Frame(right_frame)
        en_de_cry_frame.pack(side=TOP)

        decry_button = Button(en_de_cry_frame, text='Decryption', command=self.decry)
        decry_button.pack(side=LEFT)

        encry_button = Button(en_de_cry_frame, text='Encryption', command=self.encry)
        encry_button.pack(side=RIGHT)

        msg_frame = Frame(right_frame)
        msg_frame.pack(side=TOP)

        self.msg_box = Text(msg_frame, width=42, height=7)
        self.msg_box.pack(side=BOTTOM)

        # right button part ---------------------------------------------------
        self.right_img_canvas = Canvas(right_frame, bg='grey', width=img_display_width, height=img_display_height)
        self.right_img_canvas.pack(side=BOTTOM)


left_img = None
left_photo = None
right_img = None
right_photo = None
img_display_width = 300
img_display_height = 200
app = Application()
app.master.title('LSB Steganography')
app.mainloop()
