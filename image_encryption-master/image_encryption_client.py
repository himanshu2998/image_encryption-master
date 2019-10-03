import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import numpy as np
import random
import socket
import pickle
from PIL import Image,ImageTk
import cv2

class form(Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.pack(padx=10,pady=10)
        self.createWidget()

    def createWidget(self):
        self.title=Label(self,text="Hi, Client here!!")
        self.title.grid(row=0,column=1,padx=10,pady=10,sticky=W)
        self.encryptImg=Button(self,text="Encrypted",command=self.btnEncrypted)
        self.encryptImg.grid(row=1,column=0)
        self.decode=Button(self,text="Decode",command=self.btnDecode)
        self.decode.grid(row=1,column=2)

        self.s = socket.socket()

        self.port = 123
        self.host = socket.gethostname()
        self.s.connect((self.host, self.port))  # here client connects with server through port number and host name

        # receiving data from server

        self.str1 = self.s.recv(409600)
        self.str2 = self.s.recv(409600)

        # unpickling bytes to form numpy array

        self.r = pickle.loads(self.str1)  # encrypted matrix

        self.key = pickle.loads(self.str2)  # key matrix

        self.inv = np.linalg.inv(self.key)  # inverse of key matrix

        self.r_alt = np.array(self.r)  # because self.r=self.r_alt in python would change r if r_alt is changed(by reference)
        self.r_alt.resize(len(self.key), len(self.key[0]))
        self.r_alt%=255

    def btnEncrypted(self):
        self.encrypted = Image.fromarray(self.r_alt)
        self.encrypted.show()  # encrypted image

    def btnDecode(self):
        self.org = []
        for x in range(len(self.r)):  # matrix multiplication of (pix*key) and key_inverse
            for y in range(len(self.inv)):
                p = 0
                for z in range(len(self.inv)):
                    p += self.r[x][z] * self.inv[z][y]
                self.org.append(p)
        self.org = np.array(self.org)
        self.org.resize(len(self.inv), len(self.inv[0]))

        self.decoded = Image.fromarray(self.org)
        self.decoded.show()  # retrieved image ******

        self.s.close()
        exit(0)


root=Tk()
root.title("Client")
form_obj=form(root)
root.mainloop()