from Tkinter import *
from Tkinter import Tk
import tkMessageBox
import time
import I2C_LCD_driver
import RPi.GPIO as GPIO
import MFRC522
import signal
import pymysql
import re

gui = Tk()
gui.geometry("2000x1000")

conn= pymysql.connect(host='192.168.1.125',user='mumbai',password='metro',db='event')
z=conn.cursor()

def clicked():
    a=txt.get()
    if a=="":
        a=0
    try:
        b=int(a)
    except:
        #tkMessageBox.showinfo('Paymaster',"Only numbers accepted")
        print("Alphabets included")
        b=0
        
    if b<=0:
        tkMessageBox.showinfo('Paymaster',"Enter an amount and try again")
    else:
        MIFAREReader = MFRC522.MFRC522()

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected")
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print(uid)
    
        if uid==[]:
            print("Card not detected")
            tkMessageBox.showinfo('Paymaster',"Card not placed on Reader")
        else:
            print("Card updated")
            sql='UPDATE user SET amount=%s WHERE carduid0=%s AND carduid1=%s AND carduid2=%s AND carduid3=%s AND carduid4=%s;'%(b,uid[0],uid[1],uid[2],uid[3],uid[4])
            z.execute(sql)
            conn.commit()
            tkMessageBox.showinfo('Paymaster',"Rs. "+txt.get()+" was added to your card")
        
gui.title("Paymaster")
      
a = Label(gui ,text="Welcome To   Paymaster",font=("Arial Bold",25))
a.grid(column=0,row=0)

b = Label(gui ,text="Enter the Amount",font=("Arial Bold",25))
b.grid(column=6,row=6)

txt=Entry(gui,width=20)
txt.grid(column=6, row=8)
txt.focus()


btn= Button(gui, text="OK",font=("Arial Bold",25),bg="blue",fg="white",command=clicked,padx=40,pady=3)
btn.grid(column=6,row=10)

gui.mainloop()