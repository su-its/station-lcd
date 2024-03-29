import datetime
import math
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

def loop():
    global dt
    dt = datetime.datetime.now()
    update()
    root.after(100, loop)

def update():
    global image_tk, canvas
    image_tk = generateImageTk(box)
    canvas.create_image(0, 0, image = image_tk, anchor = "nw")

def drawAnalogClock(image_bgr):
    x1 = 147.5
    y1 = 152.5
    # 時針
    x2 = x1 + 50 * math.sin(dt.hour * math.pi / 6 + dt.minute * math.pi / 360)
    y2 = y1 - 50 * math.cos(dt.hour * math.pi / 6 + dt.minute * math.pi / 360)
    image_bgr = cv2.line(image_bgr, pt1 = (int(x1), int(y1)), pt2 = (int(x2), int(y2)), color = (255, 255, 255), thickness = 10, lineType = cv2.LINE_AA, shift = 0)
    # 分針
    x2 = x1 + 85 * math.sin(dt.minute * math.pi / 30 + dt.second * math.pi / 1800)
    y2 = y1 - 85 * math.cos(dt.minute * math.pi / 30 + dt.second * math.pi / 1800)
    image_bgr = cv2.line(image_bgr, pt1 = (int(x1), int(y1)), pt2 = (int(x2), int(y2)), color = (0, 0, 0), thickness = 8, lineType = cv2.LINE_AA, shift = 0)
    image_bgr = cv2.line(image_bgr, pt1 = (int(x1), int(y1)), pt2 = (int(x2), int(y2)), color = (255, 255, 255), thickness = 6, lineType = cv2.LINE_AA, shift = 0)
    # 秒針
    x2 = x1 + 90 * math.sin(dt.second * math.pi / 30)
    y2 = y1 - 90 * math.cos(dt.second * math.pi / 30)
    image_bgr = cv2.line(image_bgr, pt1 = (int(x1), int(y1)), pt2 = (int(x2), int(y2)), color = (158, 158, 158), thickness = 2, lineType = cv2.LINE_AA, shift = 0)
    return image_bgr

def setInformation():
    global information, information_length, information_id
    information_id += 1
    if information_id >= len(INFORMATION_LIST):
        information_id = 0
    if INFORMATION_LIST[information_id] == "_datetime":
        information = "今日は、" + str(dt.year) + "年" + str(dt.month) + "月" + str(dt.day) + "日 (" + WEEKDAY[dt.weekday()] + ")"
    elif INFORMATION_LIST[information_id] == "_garbage":
        if WEEKDAY[dt.weekday()] == "月" or WEEKDAY[dt.weekday()] == "木":
            information = "今日はゴミ収集日です! 室内のゴミ袋が満杯の場合、集積場に処分して下さい。収集時間は12:00～12:30です。"
        else:
            information = ""
    else:
        information = INFORMATION_LIST[information_id]
    information_length = len(information.encode())
    return

def drawInformation(image_bgr):
    global information_length, information_x
    information_x -= 12
    if information_x < information_length * 19 * -1 or information_id == -1 or information_length <= 0:
        setInformation()
        information_x = W_WIDTH
    image_bgr = drawText(image_bgr, information, information_x, 379, font, (255, 136, 0))
    return image_bgr

def getTextSize(img, text, font):
    font = ImageFont.truetype(font[0], font[1])
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font)
    return bbox[1], bbox[3]

def drawText(img, text, x, y, font, color):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    color_bgr = (color[2], color[1], color[0])
    draw.text((x, y), text, font = font, fill = color_bgr)
    img = np.array(img)
    return img

def generateImageTk(box):
    global image_bgr
    image_bgr = 255 * np.ones((W_HEIGHT, W_WIDTH, 3), np.uint8)
    for i in range(len(box)):
        if box[i].kind == "text":
            box[i].w, box[i].h = getTextSize(image_bgr, box[i].data, box[i].font)
            image_bgr = drawText(image_bgr, box[i].data, box[i].x, box[i].y, box[i].font, box[i].color)
        if box[i].kind == "image":
            put_image = box[i].data
            put_image = cv2.resize(put_image, (box[i].w, box[i].h))
            image_bgr[box[i].y:box[i].y + put_image.shape[0], box[i].x:box[i].x + put_image.shape[1]] = put_image
    image_bgr = drawAnalogClock(image_bgr)
    image_bgr = drawInformation(image_bgr)
    image_bgr = cv2.rectangle(image_bgr, (0, 0), (W_WIDTH, 27), COLOR_WHITE, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (0, 437), (W_WIDTH, W_HEIGHT), COLOR_WHITE, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (0, 0), (31, W_HEIGHT), COLOR_WHITE, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (768, 0), (W_WIDTH, W_HEIGHT), COLOR_WHITE, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (0, 0), (W_WIDTH, 22), COLOR_GRAY, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (0, 442), (W_WIDTH, W_HEIGHT), COLOR_GRAY, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (0, 0), (26, W_HEIGHT), COLOR_GRAY, thickness = -1)
    image_bgr = cv2.rectangle(image_bgr, (773, 0), (W_WIDTH, W_HEIGHT), COLOR_GRAY, thickness = -1)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    return image_tk

W_TITLE = "Station LCD"
W_WIDTH = 800
W_HEIGHT = 465
WEEKDAY = ["月", "火", "水", "木", "金", "土", "日"]
COLOR_GRAY = (31, 33, 32)
COLOR_WHITE = (255, 255, 255)

INFORMATION_LIST = [
    "_datetime",
    "_garbage",
    "本ソフトウェアのソースコードは、https://github.com/su-its/station-lcd で公開しています。"
]

dt = None
root = tkinter.Tk()
root.geometry(str(W_WIDTH) + "x" + str(W_HEIGHT))
root.title(W_TITLE)
root.resizable(0, 0)
root.attributes("-topmost", True)

box = []
canvas = tkinter.Canvas(root, highlightthickness = 0)
canvas.place(x = 0, y = 0, w = W_WIDTH, h = W_HEIGHT)
image_bgr = None
font = ImageFont.truetype("./assets/Kosugi-Regular.ttf", 42)

information = ""
information_length = 0
information_id = -1
information_x = W_WIDTH

box.append(Box("image", 0, 32, 28, 231, 255, cv2.imread("./assets/clock.png"), None, None))
box.append(Box("image", 0, 267, 28, 501, 255, cv2.imread("./assets/title.png"), None, None))
box.append(Box("image", 0, 32, 288, 736, 72, cv2.imread("./assets/message.png"), None, None))
box.append(Box("image", 0, 32, 365, 736, 72, cv2.imread("./assets/message.png"), None, None))
loop()
root.mainloop()
