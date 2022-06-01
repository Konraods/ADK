"""
Author: Konrad Jurkin WME19BC1S1

This is an app to edit and modify images
GUI is built using TKinter module
Functions to edit images are from opencv2 module (for now)

"""

from tkinter import *
from tkinter import messagebox
import tkinter as tk
import easygui as eg
import cv2
import os
import shutil

global path
path = None

# Image sequence section
def read_img_seq():
    global path, counter, subcounter

    path = eg.diropenbox()
    if path is None:
        e_l1.config(text="The path is empty")
    else:
        path = path + str("\%01d.jpg")
        counter += 1
        subcounter = 0
        e_l1.config(text="OK")
    return path


def show_sequence():
    if path is None:
        e_l1.config(text="The path is empty")
    else:
        try:
            I_seq = cv2.VideoCapture(path)
            assert I_seq.isOpened()
            cv2.namedWindow(winname="Animation", flags=cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = I_seq.read()
                if not ret:
                    break

                cv2.imshow(winname="Animation", mat=frame)

                if cv2.waitKey(200) != -1:
                    cv2.destroyWindow(winname="Animation")
                    break
            cv2.destroyWindow(winname="Animation")
            I_seq.release()
            e_l1.config(text="OK")
        except:
            e_l1.config(text="Images name should be numbers e.g. 1, 2 etc.")


def show_frame():
    global frame, counter, subcounter

    if path is None:
        e_l1.config(text="The path is empty")
    else:
        try:
            I_seq = cv2.VideoCapture(path)
            assert I_seq.isOpened()
            cv2.namedWindow(winname="Animation", flags=cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = I_seq.read()
                if not ret:
                    break

                cv2.imshow(winname="Animation", mat=frame)

                if cv2.waitKey() == 27:
                    break

            I_seq.release()
            cv2.destroyWindow(winname="Animation")

            I1 = temp_path + "\\" + str(counter) + "_frame_" + str(subcounter) + ".jpg"
            cv2.imwrite(filename=I1, img=frame)
            subcounter += 1
            e_l1.config(text="OK")
            return frame
        except:
            e_l1.config(text="Images name should be numbers e.g. 1, 2 etc.")


def read_img():
    global I_in, I_grey, I_blur, counter, subcounter, subcounter_up, subcounter_down, subcounter_mark
    counter += 1
    subcounter, subcounter_up, subcounter_down, subcounter_mark = 0, 0, 0, 0

    file = eg.fileopenbox()
    if file is None:
        e_l1.config(text="The selected image isn't loaded")
    else:
        try:
            I_in = cv2.imread(filename=file)
            if I_in is None:
                e_l1.config(text="File extension is wrong")
            else:
                cv2.imshow(winname="I_in", mat=I_in)
                I_grey = cv2.cvtColor(src=I_in, code=cv2.COLOR_BGR2GRAY)
                # cv2.imshow(winname="I_grey", mat=I_grey)
                I_blur = cv2.GaussianBlur(I_grey, (3, 3), 0)
                # cv2.imshow(winname="I_blur", mat=I_blur)

                I1 = temp_path + "\\" + str(counter) + "_I_in_" + str(subcounter) + ".jpg"
                I2 = temp_path + "\\" + str(counter) + "_I_grey_" + str(subcounter) + ".jpg"
                I3 = temp_path + "\\" + str(counter) + "_I_blur_" + str(subcounter) + ".jpg"

                cv2.imwrite(filename=I1, img=I_in)
                cv2.imwrite(filename=I2, img=I_grey)
                cv2.imwrite(filename=I3, img=I_blur)

                b7["state"] = "normal"
                b8["state"] = "normal"
                b9["state"] = "normal"
                b10["state"] = "normal"
                b11["state"] = "normal"
                b13["state"] = "normal"
                e_l1.config(text="OK")
                return I_in, I_grey, I_blur
        except:
            e_l1.config(text="File extension is wrong")


def edge_X():
    global counter, subcounter

    I_x = I_blur
    I_x = cv2.Sobel(src=I_x, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
    cv2.imshow(winname="I_x", mat=I_x)

    I1 = temp_path + "\\" + str(counter) + "_I_x_" + str(subcounter) + ".jpg"
    cv2.imwrite(filename=I1, img=I_x)
    return I_x


def edge_Y():
    global counter

    I_y = I_blur
    I_y = cv2.Sobel(src=I_y, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
    cv2.imshow(winname="I_y", mat=I_y)

    I1 = temp_path + "\\" + str(counter) + "_I_y_" + str(subcounter) + ".jpg"
    cv2.imwrite(filename=I1, img=I_y)
    return I_y


def edge_XY():
    global counter

    I_xy = I_blur
    I_xy = cv2.Sobel(src=I_xy, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
    cv2.imshow(winname="I_xy", mat=I_xy)

    I1 = temp_path + "\\" + str(counter) + "_I_xy_" + str(subcounter) + ".jpg"
    cv2.imwrite(filename=I1, img=I_xy)
    return I_xy


def canny():
    global counter, subcounter
    if (e2.get() or e3.get()) == "":
        e_l1.config(text="Threshold 1 or 2 - empty")
    elif e2.get() == "Treshold 1" or e3.get() == "Treshold 2":
        e_l1.config(text="Threshold 1 or 2 - empty")
    else:
        I_canny = I_blur
        I_canny = cv2.Canny(image=I_canny, threshold1=float(e2.get()), threshold2=float(e3.get()))
        cv2.imshow(winname="I_canny", mat=I_canny)

        I1 = temp_path + "\\" + str(counter) + "_I_canny_" + str(subcounter) + ".jpg"
        cv2.imwrite(filename=I1, img=I_canny)
        subcounter += 1
        e_l1.config(text="OK")
        return I_canny


def upsampling():
    global counter, subcounter, subcounter_up, subcounter_down
    I_up, I_down = I_in, I_in

    if 0 <= int(e4.get()) < 4:
        for i in range(int(e4.get())):
            I_up = cv2.pyrUp(src=I_up)

        cv2.imshow(winname="I_up", mat=I_up)
        I1 = temp_path + "\\" + str(counter) + "_I_up_" + str(subcounter) + ".jpg"
        cv2.imwrite(filename=I1, img=I_up)
        subcounter_up += 1
        e_l1.config(text="OK")
        return I_up

    elif -4 < int(e4.get()) <= 0:
        a = abs(int(e4.get()))
        for i in range(a):
            I_down = cv2.pyrDown(src=I_down)

        cv2.imshow(winname="I_down", mat=I_down)
        I2 = temp_path + "\\" + str(counter) + "_I_down_" + str(subcounter) + ".jpg"
        cv2.imwrite(filename=I2, img=I_down)
        subcounter_down += 1
        e_l1.config(text="OK")
        return I_down
    else:
        e_l1.config(text="Enter value between -3 and 3")

def mark_img():
    global subcounter_mark

    top_left = []
    bottom_right = []
    I_mark = I_in.copy()

    cv2.imshow(winname="I_mark", mat=I_mark)

    def drawRectangle(action, x, y, flags, *userdata):
        global top_left, bottom_right

        if action == cv2.EVENT_LBUTTONDOWN:
            top_left = [(x, y)]
        elif action == cv2.EVENT_LBUTTONUP:
            bottom_right = [(x, y)]
            cv2.rectangle(I_mark, top_left[0], bottom_right[0], (255, 0, 0), 1, 8)
            cv2.imshow(winname="I_mark", mat=I_mark)

    cv2.setMouseCallback("I_mark", drawRectangle)

    keyboard = 0
    while keyboard != 27:
        cv2.imshow(winname="I_mark", mat=I_mark)
        keyboard = cv2.waitKey(0)

    e_l1.config(text="OK")
    I1 = temp_path + "\\" + str(counter) + "_I_mark_" + str(subcounter) + ".jpg"
    cv2.imwrite(filename=I1, img=I_mark)
    subcounter_mark += 1
    cv2.destroyWindow(winname="I_mark")


def exit():  # Function to delete temp folder for images and close main window
    shutil.rmtree(path=temp_path)
    root.destroy()


def update():  # Function to update list's shown elements
    dic = os.listdir(path=temp_path)
    list1.delete(0, END)

    for name in dic:
        list1.insert('end', name)


def save_img():  # Function to save selected images from list to chosen dic
    path = eg.diropenbox()
    dir = os.listdir(path=temp_path)

    for i in list1.curselection():
        src_path = temp_path + "\\" + str(dir[i])
        shutil.copy2(src=src_path, dst=path)


# Main window
root = tk.Tk()
root.title("Image processing app")
root.geometry("650x700+0+0")

# Creating temp folder for images
temp_path = 'C:\\Images_temp'
isExist = os.path.exists(path=temp_path)
if not isExist:
    os.makedirs(name=temp_path)

# Part for multiple images
l1 = Label(master=root, text="Images sequence", font=13, width=66, height=5, bg="#d6d4d4")
b1 = Button(master=root, text="Read images for sequence", command=read_img_seq, font=13, height=2, bg="#c0c0c0")
b2 = Button(master=root, text="Show images sequence", command=show_sequence, font=13, height=2, bg="#c0c0c0")
b3 = Button(master=root, text="Frame by frame", command=show_frame, font=13, height=2, bg="#c0c0c0")

# Part for single image
l2 = Label(master=root, text="Single image", font=13, width=66, height=5, bg="#d6d4d4")
b5 = Button(master=root, text="Read image", command=read_img, font=13, height=2, bg="#c0c0c0")
l3 = Label(master=root, text="Edge detection", font=13, height=2, bg="#d6d4d4")
b7 = Button(master=root, text="X", command=edge_X, font=13, height=2, bg="#c0c0c0", state=DISABLED)
b8 = Button(master=root, text="Y", command=edge_Y, font=13, height=2, bg="#c0c0c0", state=DISABLED)
b9 = Button(master=root, text="X+Y", command=edge_XY, font=13, height=2, bg="#c0c0c0", state=DISABLED)
b10 = Button(master=root, text="Canny", command=canny, font=13, height=2, bg="#c0c0c0", state=DISABLED)
e2 = Entry(master=root, justify="center", bg="#c0c0c0")
e3 = Entry(master=root, justify="center", bg="#c0c0c0")
b11 = Button(master=root, text="Marked fragments", command=mark_img, font=13, height=2, bg="#c0c0c0", state=DISABLED)
b13 = Button(master=root, text="Upsampling", command=upsampling, font=13, height=2, bg="#c0c0c0", state=DISABLED)
e4 = Entry(master=root, justify="center", bg="#c0c0c0")
b14 = Button(master=root, text="Exit", command=exit, font=13, height=2, bg="#d6d4d4")

# Grid settings for sequence
l1.grid(row=0, columnspan=3, sticky="nsew")
b1.grid(row=1, columnspan=3, sticky="nsew")
b2.grid(row=2, columnspan=3, sticky="nsew")
b3.grid(row=3, columnspan=3, sticky="nsew")

# Grid settings for single image
l2.grid(row=4, columnspan=3, sticky="nsew")
b5.grid(row=5, columnspan=3, sticky="nsew")
l3.grid(row=6, columnspan=3, sticky="nsew")
b7.grid(row=7, column=0, sticky="w", ipadx=100)
b8.grid(row=7, column=1, sticky="w", ipadx=100)
b9.grid(row=7, column=2, sticky="e", ipadx=80)
b10.grid(row=8, column=0, sticky="nsew")
b11.grid(row=11, columnspan=3, sticky="nsew")
b13.grid(row=13, columnspan=2, sticky="nsew")
b14.grid(row=15, columnspan=3, sticky="nsew", ipady=10)

# Entry threshold for canny
e2.grid(row=8, column=1, sticky="nsew")
e3.grid(row=8, column=2, sticky="nsew")
e2.insert(0, "Treshold 1")
e3.insert(0, "Treshold 2")
e2.bind("<FocusIn>", lambda args: e2.delete("0", "end"))
e3.bind("<FocusIn>", lambda args: e3.delete("0", "end"))

# Entry lvl of up/down sampling
e4.insert(0, "-3 - 3")
e4.grid(row=13, column=2, sticky="nsew")
e4.bind("<FocusIn>", lambda args: e4.delete("0", "end"))


# Workspace window to select and save images
workspace = tk.Toplevel(master=root)
workspace.title("Workspace")
workspace.geometry("200x350+650+0")

# List and 2 buttons to update list and save images
list1 = Listbox(master=workspace, selectmode="multiple")
b1 = Button(master=workspace, text="Update", command=update, font=13, height=2, bg="#d6d4d4")
b2 = Button(master=workspace, text="Save selected images", command=save_img, font=13, height=2, bg="#d6d4d4")

# Pack settings for window
list1.pack(fill=BOTH, expand=1)
b1.pack(fill=X)
b2.pack(fill=X)


# Errors window
error = tk.Toplevel(master=root)
error.title("Error")
error.geometry("200x320+650-340")

# Label and pack settings for window
e_l1 = Label(master=error, text="No errors", fg='#F00', font=30, wraplength=180)
e_l1.pack(fill=BOTH, expand=1)

# Define counters
counter, subcounter, subcounter_up, subcounter_down, subcounter_mark = 0, 0, 0, 0, 0


def on_closing():  # Function to close window and delete temp folder
    if messagebox.askokcancel(title="Quit", message="Do you want to quit?"):
        shutil.rmtree(path=temp_path)
        root.destroy()


def block_closing():  # Function to prevent closing workspace window
    pass


root.protocol(name="WM_DELETE_WINDOW", func=on_closing)
workspace.protocol(name="WM_DELETE_WINDOW", func=block_closing)
error.protocol(name="WM_DELETE_WINDOW", func=block_closing)
root.mainloop()


