import tkinter
import cv2
import numpy as np
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class Box:
    def __init__(self, kind, status, x, y, w, h, data, font, color):
        self.kind = kind
        self.status = status
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.data = data
        self.font = font
        self.color = color

def draw():
    global image_tk, canvas
    image_tk = generateImageTk(box)
    canvas.create_image(0, 0, image = image_tk, anchor = "nw")

def generateImageTk(box):
    global image_bgr
    image_bgr = 255 * np.ones((W_HEIGHT, W_WIDTH, 3), np.uint8)
    for i in range(len(box)):
        if box[i].kind == "text":
            box[i].w, box[i].h = getTextSize(image_bgr, box[i].data, box[i].font)
            image_bgr = drawText(image_bgr, box[i].data, box[i].x, box[i].y, box[i].font, box[i].color)
        if box[i].kind == "image":
            put_image = cv2.imread(box[i].data)
            put_image = cv2.resize(put_image, (box[i].w, box[i].h))
            image_bgr[box[i].y:box[i].y + put_image.shape[0], box[i].x:box[i].x + put_image.shape[1]] = put_image
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    return image_tk

W_TITLE = "Station LCD"
W_WIDTH = 800
W_HEIGHT = 465

root = tkinter.Tk()
root.geometry(str(W_WIDTH) + "x" + str(W_HEIGHT))
root.title(W_TITLE)
root.resizable(0, 0)

box = []
canvas = tkinter.Canvas(root, highlightthickness = 0)
canvas.place(x = 0, y = 0, w = W_WIDTH, h = W_HEIGHT)
image_bgr = None

box.append(Box("image", 0, 0, 0, W_WIDTH, W_HEIGHT, "./assets/bg.jpg", None, None))
draw()
root.mainloop()
