import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import numpy
from PIL import Image, ImageDraw, ImageTk
import time 
import random as rand

class App:
    file_path = ""
    img_list = []

    def __init__(self,window):
        frame_a = tk.Frame(window)
        frame_b = tk.Frame(window)

        self.open_button = tk.Button(
            master=frame_a,
            text="Browse for PNG file",
            height=1,
            bg="white",
            fg="black",
            command=self.browse_file,
            pady = 5
        )

        self.shake_button = tk.Button(
            master=frame_a,
            text="Export Shake",
            width=10,
            height=1,
            bg="white",
            fg="black",
            command=lambda: self.make_gif(movement="shake", main = window),
            pady = 5
        )

        self.spin_button = tk.Button(
            master=frame_a,
            text="Export Spin",
            width=10,
            height=1,
            bg="white",
            fg="black",
            command=lambda: self.make_gif(movement="spin", main = window),
            pady = 5
        )

        self.label_png = tk.Label(master=frame_b)
        self.label_instructions = tk.Label(
            master=frame_a, 
            text = "Works best on PNG\'s with transparent backgrounds",
            fg= '#f00',
            pady = 5
        )
        
        self.label_instructions.pack()
        self.open_button.pack()
        self.shake_button.pack()
        self.spin_button.pack()
        self.label_png.pack()
        

        frame_a.pack()
        frame_b.pack()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        try:
            preview_pic = ImageTk.PhotoImage(self.read_resize(150))
            self.label_png["image"] = preview_pic
            self.label_png.image = preview_pic                  #Python needs reference or else it will not show up
        except:
            pass

    def read_resize(self, pixel_width):
        if(os.path.isfile(self.file_path)):
            icon = Image.open(self.file_path)
            basewidth = pixel_width
            wpercent = (basewidth/float(icon.size[0]))
            hsize = int((float(icon.size[1])*float(wpercent)))
            icon = icon.resize((basewidth, hsize), Image.NEAREST)
            return icon

    def make_gif(self, movement, main):
        img = self.read_resize(150)
        frames = 10
        angles = np.linspace(0, 360-360/frames, frames)
        xmax = 4
        ymax = 4
        
        try:
            if movement == "spin":
                for theta in angles:
                    self.img_list.append(img.rotate(angle=theta))
            elif movement == "shake":
                for i in range(frames):
                    translation = (rand.randint(-xmax, xmax), rand.randint(-ymax, ymax))
                    self.img_list.append(img.rotate(angle=0, translate= translation))
        except:
            pass  
        
        self.export(main)

    def export(self,main):
        try:
            save_filename = filedialog.asksaveasfilename(
                    defaultextension=".gif")
            self.img_list[0].save(save_filename, format='GIF', save_all=True,
                            append_images=self.img_list[1:], duration=100, transparency = 0, loop=0, disposal=2)
            main.destroy()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Make dumb slack emoji\'s from PNG\'s!')
    root.geometry("300x325")  
    App(root)
    root.mainloop()
