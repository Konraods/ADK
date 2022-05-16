from tkinter import *
import tkinter as tk
import easygui as eg
import cv2
import os
import shutil

global I_save, counter

# Image sequence section
def read_img_seq():
    global path

    path = eg.diropenbox()
    path = path + str("\%01d.jpg")

    return path


def show_sequence():
    I_seq = cv2.VideoCapture(path)
    assert I_seq.isOpened()
    cv2.namedWindow("Animation", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = I_seq.read()
        if not ret:
            break

        cv2.imshow("Animation", frame)

        if cv2.waitKey(200) != -1:
            cv2.destroyWindow("Animation")
            break
    cv2.destroyWindow("Animation")
    I_seq.release()


def show_frame():
    global frame, counter, ret

    I_seq = cv2.VideoCapture(path)
    assert I_seq.isOpened()
    cv2.namedWindow("Animation", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = I_seq.read()
        if not ret:
            break

        cv2.imshow("Animation", frame)

        if cv2.waitKey() == 27:
            break

    I_seq.release()
    cv2.destroyWindow("Animation")

    return frame, ret


def save_frame():
    path = eg.diropenbox()
    #full_path = path + "\\" + str(e1.get()) + ".jpg"
    # cv2.imwrite(full_path, frame)

    I1 = temp_path + "\\frame_" + str(counter) + ".jpg"
    cv2.imwrite(I1, frame)

def read_img():
    global I_in, I_grey, I_blur, counter

    file = eg.fileopenbox()
    I_in = cv2.imread(file)
    cv2.imshow(winname="I_in", mat=I_in)
    I_grey = cv2.cvtColor(src=I_in, code=cv2.COLOR_BGR2GRAY)
    # cv2.imshow(winname="I_grey", mat=I_grey)
    I_blur = cv2.GaussianBlur(I_grey, (3, 3), 0)
    # cv2.imshow(winname="I_blur", mat=I_blur)

    I1 = temp_path + "\\I_in" + str(counter) + ".jpg"
    I2 = temp_path + "\\I_grey" + str(counter) + ".jpg"
    I3 = temp_path + "\\I_blur" + str(counter) + ".jpg"

    cv2.imwrite(I1, I_in)
    cv2.imwrite(I2, I_grey)
    cv2.imwrite(I3, I_blur)
    counter += 1
    return I_in, I_grey, I_blur


def edge_X():
    global counter

    I_x = I_blur
    I_x = cv2.Sobel(src=I_x, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
    cv2.imshow(winname="I_x", mat=I_x)

    I1 = temp_path + "\\I_x" + str(counter) + ".jpg"
    cv2.imwrite(I1, I_x)
    counter += 1
    return I_x


def edge_Y():
    global counter

    I_y = I_blur
    I_y = cv2.Sobel(src=I_y, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
    cv2.imshow(winname="I_y", mat=I_y)

    I1 = temp_path + "\\I_y" + str(counter) + ".jpg"
    cv2.imwrite(I1, I_y)
    counter += 1
    return I_y


def edge_XY():
    global counter

    I_xy = I_blur
    I_xy = cv2.Sobel(src=I_xy, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
    cv2.imshow(winname="I_xy", mat=I_xy)

    I1 = temp_path + "\\I_xy" + str(counter) + ".jpg"
    cv2.imwrite(I1, I_xy)
    counter += 1
    return I_xy


def canny():
    global counter

    I_canny = I_blur
    I_canny = cv2.Canny(image=I_canny, threshold1=float(e2.get()), threshold2=float(e3.get()))
    cv2.imshow(winname="I_canny", mat=I_canny)

    I1 = temp_path + "\\I_canny" + str(counter) + ".jpg"
    cv2.imwrite(I1, I_canny)
    counter += 1
    return I_canny


def upsampling():
    global counter
    I_up, I_down = I_in, I_in

    if int(e4.get()) >= 0:
        for i in range(int(e4.get())):
            I_up = cv2.pyrUp(src=I_up)

        cv2.imshow(winname="I_up", mat=I_up)
        I1 = temp_path + "\\I_up" + str(counter) + ".jpg"
        cv2.imwrite(I1, I_up)
    else:
        a = abs(int(e4.get()))
        for i in range(a):
            I_down = cv2.pyrDown(src=I_down)

        cv2.imshow(winname="I_up", mat=I_up)
        I2 = temp_path + "\\I_down" + str(counter) + ".jpg"
        cv2.imwrite(I2, I_down)
    counter += 1
    return I_up



def save_img():

    path = eg.diropenbox()

    print(list1.curselection())
    dir = os.listdir(temp_path)

    for i in list1.curselection():
        src_path = temp_path + "\\" + str(dir[i])
        shutil.copy2(src_path, path)

def exit():
    shutil.rmtree(temp_path)
    root.destroy()


def update():
    dic = os.listdir(temp_path)
    list1.delete(0, END)

    for name in dic:
        list1.insert('end', name)


# Main window
root = tk.Tk()
root.title("Image processing app")
root.geometry("650x850+0+0")

# Creating temp folder for images
temp_path = 'C:\\Images_temp'
isExist = os.path.exists(temp_path)

if not isExist:
    os.makedirs(temp_path)

# Part for multiple images
l1 = Label(master=root, text="Images sequence", font=13, width=66, height=5, bg="#d6d4d4")
b1 = Button(master=root, text="Read images for sequence", command=read_img_seq, font=13, height=2, bg="#c0c0c0")
b2 = Button(master=root, text="Show images sequence", command=show_sequence, font=13, height=2, bg="#c0c0c0")
b3 = Button(master=root, text="Frame by frame", command=show_frame, font=13, height=2, bg="#c0c0c0")
b4 = Button(master=root, text="Save frame", command=save_frame, font=13, height=2, bg="#c0c0c0")
e1 = Entry(master=root, justify="center", bg="#c0c0c0")

# Part for single image
l2 = Label(master=root, text="Single image", font=13, height=5, bg="#d6d4d4")
b5 = Button(master=root, text="Read image", command=read_img, font=13, height=2, bg="#c0c0c0")
l3 = Label(master=root, text="Edge detection", font=13, height=2, bg="#d6d4d4")
b7 = Button(master=root, text="X", command=edge_X, font=13, height=2, bg="#c0c0c0")
b8 = Button(master=root, text="Y", command=edge_Y, font=13, height=2, bg="#c0c0c0")
b9 = Button(master=root, text="X+Y", command=edge_XY, font=13, height=2, bg="#c0c0c0")
b10 = Button(master=root, text="Canny", command=canny, font=13, height=2, bg="#c0c0c0")
e2 = Entry(master=root, justify="center", bg="#c0c0c0")
e3 = Entry(master=root, justify="center", bg="#c0c0c0")
b11 = Button(master=root, text="Marked fragments WIP", font=13, height=2, bg="#c0c0c0")
b12 = Button(master=root, text="Search by pattern WIP", font=13, height=2, bg="#c0c0c0")
b13 = Button(master=root, text="Upsampling", command=upsampling, font=13, height=2, bg="#c0c0c0")
e4 = Entry(master=root, justify="center", bg="#c0c0c0")
b14 = Button(master=root, text="Save image WIP", command=save_img, font=13, height=2, bg="#c0c0c0")
e5 = Entry(master=root, justify="center", bg="#c0c0c0")
b15 = Button(master=root, text="Exit", command=exit, font=13, height=2, bg="#d6d4d4")

l1.grid(row=0, columnspan=3, sticky="nsew")
b1.grid(row=1, columnspan=3, sticky="nsew")
b2.grid(row=2, columnspan=3, sticky="nsew")
b3.grid(row=3, columnspan=3, sticky="nsew")
b4.grid(row=4, columnspan=2, sticky="nsew")

e1.grid(row=4, column=2, sticky="nsew")
e1.insert(0, "Fill file name")
e1.bind("<FocusIn>", lambda args: e1.delete("0", "end"))

l2.grid(row=5, columnspan=3, sticky="nsew")
b5.grid(row=6, columnspan=3, sticky="nsew")
l3.grid(row=7, columnspan=3, sticky="nsew")
b7.grid(row=8, column=0, sticky="w", ipadx=100)
b8.grid(row=8, column=1, sticky="w", ipadx=100)
b9.grid(row=8, column=2, sticky="e", ipadx=80)
b10.grid(row=9, column=0, sticky="nsew")

e2.grid(row=9, column=1, sticky="nsew")
e3.grid(row=9, column=2, sticky="nsew")
e2.insert(0, "Treshold 1")
e3.insert(0, "Treshold 2")
e2.bind("<FocusIn>", lambda args: e2.delete("0", "end"))
e3.bind("<FocusIn>", lambda args: e3.delete("0", "end"))

b11.grid(row=10, columnspan=3, sticky="nsew")
b12.grid(row=11, columnspan=3, sticky="nsew")
b13.grid(row=12, columnspan=2, sticky="nsew")

e4.insert(0, "-3 - 3")
e4.grid(row=12, column=2, sticky="nsew")
e4.bind("<FocusIn>", lambda args: e4.delete("0", "end"))

b14.grid(row=13, columnspan=2, sticky="nsew")

e5.grid(row=13, column=2, sticky="nsew")
e5.insert(0, "Fill file name")
e5.bind("<FocusIn>", lambda args: e5.delete("0", "end"))

b15.grid(row=14, columnspan=3, sticky="nsew", ipady=10)

counter = 0

workspace = tk.Toplevel(root)
workspace.title("Workspace")
workspace.geometry("200x350+650+0")
list1 = Listbox(master=workspace, selectmode="multiple")
b1 = Button(master=workspace, text="Update", command=update, font=13, height=2, bg="#d6d4d4")
list1.pack(fill=BOTH, expand=1)
b1.pack()

root.mainloop()

