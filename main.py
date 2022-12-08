from flask import Flask, render_template, request ,redirect, flash,make_response

app = Flask(__name__)
app.secret_key = 'my_secret_key'


import cv2
import numpy as np
from tkinter import *
from tkinter.ttk import *                                                                                 
from PIL import Image, ImageTk
from tkinter import filedialog,messagebox
from tkinter.filedialog import askopenfile
import sys
import pytesseract
import webbrowser
from pyzbar import pyzbar
from filestack import Client
import speech_recognition as sr

c = Client("Ax0cFWFwUQVqI8FjPgE3zz")

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_barcodes(image,str1):
    frame = cv2.imread(image)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        for i in barcode_info:
            str1+= i 
    return str1

def speak():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)
        query=""
    try:
        query = r.recognize_google(audio, language='en-in')
        query=query.lower()
        webbrowser.open_new('https://www.google.com/search?q='+query)
    except:
        pass 

image=""

@app.route('/voicesearch')
def voicesearch():
    speak()
    return  render_template('index.html')

@app.route('/imgimgsrch')
def imgimgsrch():
    heh=Tk()
    heh.geometry("1x1")
    img=filedialog.askopenfilename()
    heh.destroy()
    heh.mainloop()
    filelnk = c.upload(filepath = img)
    webbrowser.open_new('https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIIRP&sbisrc=UrlPaste&q=imgurl:'+filelnk.url)
    return  render_template('index.html')

@app.route('/camimgsrch')
def camimgsrch():
    video = cv2.VideoCapture(0) 
    while True:
        check, frame = video.read()
        cv2.imshow("Press Spacebar to Capture !!",frame)
        key = cv2.waitKey(1)
        if key == ord(" "):
            break
    cv2.waitKey(300)
    filename = "tempim"
    showPic = cv2.imwrite(filename+".jpg",frame)
    video.release()
    cv2.destroyAllWindows()
    image="tempim.jpg"
    filelnk = c.upload(filepath = image)
    webbrowser.open_new('https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIIRP&sbisrc=UrlPaste&q=imgurl:'+filelnk.url)
    return  render_template('index.html')

@app.route('/camtext')
def camtext():
    video = cv2.VideoCapture(0) 
    while True:
        check, frame = video.read()
        cv2.imshow("Press Spacebar to Capture !!",frame)
        key = cv2.waitKey(1)
        if key == ord(" "):
            break
    cv2.waitKey(300)
    filename = "tempim"
    showPic = cv2.imwrite(filename+".jpg",frame)
    video.release()
    cv2.destroyAllWindows()
    image="tempim.jpg"
    img = cv2.imread(image)
    text = pytesseract.image_to_string(img)
    if text=="":
        goo=Tk()
        goo.geometry("1x1")
        messagebox.showerror('No Text Found','The Image does not have any text, Please retry with another Image')
        goo.destroy()
        goo.mainloop()
    else:
        text=text.replace(' ','+')
        webbrowser.open_new('https://www.google.com/search?q='+text)
    return  render_template('index.html')

@app.route('/imgtext')
def imgtext():
    try:
        heh=Tk()
        heh.geometry("1x1")
        img=filedialog.askopenfilename()
        img = cv2.imread(img, 0)
        text = pytesseract.image_to_string(img)
        text=text.replace(' ','+')
        if text=="":
            messagebox.showerror('No Text Found','The Image does not have any text, Please retry with another Image')
            heh.destroy()
        else:
            heh.destroy()
            webbrowser.open_new('https://www.google.com/search?q='+text)
        heh.mainloop()
    except:
        heh.destroy()
        goo=Tk()
        goo.geometry("1x1")
        messagebox.showerror('No Text Found','The Image does not have any text, Please retry with another Image')
        goo.destroy()
        goo.mainloop()
    return  render_template('index.html')

@app.route('/camqr')
def camqr():
    try:
        str1=""
        video = cv2.VideoCapture(0) 
        while True:
            check, frame = video.read()
            cv2.imshow("Press Spacebar to Capture !!",frame)
            key = cv2.waitKey(1)
            if key == ord(" "):
                break
        cv2.waitKey(300)
        filename = "tempim"
        showPic = cv2.imwrite(filename+".jpg",frame)
        video.release()
        cv2.destroyAllWindows()
        image="tempim.jpg"
        str1 = read_barcodes(image,str1)
        if str1!="":
            webbrowser.open(str1)
            cv2.destroyAllWindows()
            str1=""
        else:
            heh=Tk()
            heh.geometry("1x1")
            messagebox.showerror('No QR Found','The Image does not have a valid QR, Please retry with another Image')
            heh.destroy()
            heh.mainloop()
    except:
        goo=Tk()
        goo.geometry("1x1")
        messagebox.showerror('No QR Found','The Image does not have a valid QR, Please retry with another Image')
        goo.destroy()
        goo.mainloop()
    return  render_template('index.html')

@app.route('/imgqr')
def imgqr():
    try:
        str1=""
        heh=Tk()
        heh.geometry("1x1")
        img=filedialog.askopenfilename()
        str1 = read_barcodes(img,str1)
        print(str1)
        if str1:
            heh.destroy()
            webbrowser.open(str1)
            cv2.destroyAllWindows()
            str1=""
        else:
            messagebox.showerror('No QR Found','The Image does not have a valid QR, Please retry with another Image')
            heh.destroy()
        heh.mainloop()
    except:
        heh.destroy()
        goo=Tk()
        goo.geometry("1x1")
        messagebox.showerror('No QR Found','The Image does not have a valid QR, Please retry with another Image')
        goo.destroy()
        goo.mainloop()
    return  render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route1')
def route1():
  return render_template('textscan.html')

@app.route('/route2')
def route2():
  return render_template('qrscan.html')

@app.route('/route3')
def route3():
  return render_template('imagesearch.html')

@app.route('/route4')
def route4():
  return render_template('voicesearch.html')

if __name__ == '__main__':
    app.debug=True
    app.run()