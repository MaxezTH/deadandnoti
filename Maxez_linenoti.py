import customtkinter
import time
import cv2
import numpy
import win32gui
import win32ui
from ctypes import windll
from tkinter import *
global System_Maxez
System_Maxez = False
def login():
    #root.iconify()
    #root.state(newstate='iconic')
    global System_Maxez
    System_Maxez = True
    scan()
    check()

def stop():
    global System_Maxez
    System_Maxez = False

def scan():
    from PIL import Image
    title_import = listbox.get()
    hwnd = win32gui.FindWindow(None, title_import)
    label_status.configure(text="Scaning ...", text_color="white")
    root.update()
    time.sleep(1)
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print("result + ", result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    print(bmpinfo)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    print(im)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    root.update()
    if result == 1:
        # PrintWindow Succeeded
        im.save("test.png")
        #im.show("test.png")
        print(System_Maxez)
        label_status.configure(text="Checking....", text_color="white")
        root.update()
        time.sleep(1)
    
def check():
    apiget = entry1.get()
    from parinya import LINE
    item = cv2.imread('Dead.png')
    screen = cv2.imread('test.png')
    result = cv2.matchTemplate(item, screen, cv2.TM_SQDIFF_NORMED)
    loc_cut = numpy.where(result <=0.03)
    loc_xy = list(zip(*loc_cut[::-1]))
    print(System_Maxez)
    root.update()
    if System_Maxez:
        if loc_xy == []:
            print("ไม่เจอ")
            label_status.configure(text="ยังไม่ตาย ...",text_color="white")
            del result
            del screen
            del loc_cut
            del loc_xy
            time.sleep(1)
            if System_Maxez:
                scan()
                check()
        else :
            print("เจอ")
            line = LINE(apiget)
            textdead = entry2.get()
            time.sleep(0.5)
            line.sendtext(textdead)
            root.state(newstate='normal')
            label_status.configure(text="ตายแล้ว ...",text_color="red")

        #cv2.imshow('Dead.png',screen)
    else :
        label_status.configure(text="หยุดการทำงาน....",text_color="yellow")
        cv2.waitKey(0)

def testbotton():
    from parinya import LINE
    textdead = entry2.get()
    apiget = entry1.get()
    line = LINE(apiget)
    time.sleep(0.5)
    line.sendtext(textdead)
    label_status.configure(text="ส่งข้อความไปแล้วน้า . .. ")
    global System_Maxez
    System_Maxez = 0
import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []


def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
        titles.remove('')

    return True


EnumWindows(EnumWindowsProc(foreach_window), 0)

print(titles)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("400x420")
root.title("Maxez | Check Death V.0.0.3")
root.resizable(width=False, height=False)
root.iconbitmap("alligator.ico")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Line แจ้งเตือนตาย Flyff ", font=("Kanit", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="ใส่ API ของ LINE")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="เมื่อตายให้แจ้งในไลน์ว่า")
entry2.pack(pady=12, padx=10)


clicked = StringVar()
clicked.set("asdsadsa")

label2 = customtkinter.CTkLabel(master=frame, text="เลือกหน้าต่างระบบ", font=("Kanit", 14))
label2.pack(pady=5, padx=10)

listbox = customtkinter.CTkOptionMenu(master=frame, values=titles, font=("Kanit", 14))
listbox.pack(pady=5, padx=10)

#entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="1-99",width= 100)
#entry3.pack(pady=12, padx=10)

frame2 = customtkinter.CTkFrame(master=frame, width=100, height=60)
frame2.pack()

label_titlestatus = customtkinter.CTkLabel(master=frame2, text="Status", text_color="yellow", font=("Kanit", 18))
label_titlestatus.pack()

label_status = customtkinter.CTkLabel(master=frame2, text="Waiting", font=("Kanit", 14))
label_status.pack()

button2 = customtkinter.CTkButton(master=frame, text="ทดสอบส่ง", command=testbotton, width=60, border_color='white', font=("Kanit", 14))
#button2.pack(pady=5, padx=10)
button2.place(x=110,y=350)

button = customtkinter.CTkButton(master=frame, text="เริ่มทำงาน", command=login, height=40, width=100, border_color='black',
                                 border_width=1, fg_color="DarkOliveGreen3", text_color="black", font=("Kanit", 14))
#button.pack(pady=5, padx=10)
button.place(x=40,y=300)

button_Stop = customtkinter.CTkButton(master=frame, text="หยุดทำงาน", command=stop, height=40,
                                      width=100, border_color='black', border_width=1, fg_color="Red3", font=("Kanit", 14))
button_Stop.place(x=150,y=300)
root.mainloop()