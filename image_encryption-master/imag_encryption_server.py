import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
import numpy as np
import random
import socket
import pickle
from PIL import Image, ImageTk

class form(Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.pack(padx=20,pady=20)
        self.createWidget()

    def createWidget(self):
        self.title=Label(self,text="Hi, Server here!!")
        self.title.grid(row=0,column=1,padx=10,pady=10,sticky=N)
        self.uploadBtn=Button(self,text="Upload",command=self.funcUploadBtn)
        self.uploadBtn.grid(row=1,column=0,stick=W)
        self.keyGen=Button(self,text="KeyGen",command=self.funcKeyGen)
        self.keyGen.grid(row=1,column=2,sticky=E)
        self.encrypt=Button(self,text="Encrypt",command=self.btnEncrypt)
        self.encrypt.grid(row=2,column=1)
        self.send=Button(self,text="Send",command=self.btnSend)
        self.send.grid(row=3,column=1,padx=15,pady=15)


    def funcUploadBtn(self):
        self.path=filedialog.askopenfile()
        self.pic = Image.open(self.path.name)  # opening image
        self.pic = self.pic.resize((250, 250), Image.ANTIALIAS)
        self.pix = np.array(self.pic)
        self.pix = self.pix[:, :, 0]  # converting to monochrome
        self.old = Image.fromarray(self.pix)  # forming image from array
        self.old.show()
        # print(self.path.name)

    def funcKeyGen(self):
        try:
            if(self.path==None):
                raise Exception
            self.key = np.array([[random.randint(0, 3) for i in range(len(self.pix[0]))] for j in range(len(self.pix))])  # generating random key matrix
            self.top=Toplevel()
            self.top.title("Key:")
            self.top.label=Label(self.top,text="Random key is:")
            self.top.msg=Message(self.top,text=self.key)
            self.top.msg.pack()
        except Exception as ex:
            tkinter.messagebox.showinfo("Error","Upload Image First!")

    def btnEncrypt(self):
        try:
            if(self.path.name=='\0'):
                raise ValueError
            elif(self.key is None):
                raise Exception
            self.r = []
            for x in range(len(self.pix)):  # matrix multiplication of original matrix and key matrix
                for y in range(len(self.key)):
                    p = 0
                    for z in range(len(self.key)):
                        p += self.pix[x][z] * self.key[z][y]
                    self.r.append(p)
            self.r = np.array(self.r)
            self.r.resize(len(self.key), len(self.key[0]))

            # alternative r array to show encrypted image

            self.r_alt = np.array(self.r) # because self.r=self.r_alt in python would change r if r_alt is changed(by reference)
            self.r_alt.resize(len(self.key), len(self.key[0]))

            # print(np.shape(pix)) # dimensions or array
            self.r %= 255  # to keep array elements in range of 0-255(RGB range) in order to show encrypted image
            self.new = Image.fromarray(self.r)  # forming image from array
            self.new.show()  # encrypted image   ******
        except ValueError as v:
            tkinter.messagebox.showerror("Upload Image First",v)
        except Exception as ex:
            tkinter.messagebox.showerror("Key not generated",ex)

    def btnSend(self):
        try:
            if(self.path.name=='\0'):
                raise Exception
            elif(self.key is None):
                raise ValueError
            self.s=socket.socket()

            self.port = 123
            self.host = socket.gethostname()  # retuns host's name(either local(or system's) ip address or system name)
            self.s.bind((self.host, self.port))  # binding the host and port number with connection
            self.s.listen(5)  # server starts listening to requests(atmost 5)

            while True:

                self.c = self.s.accept()[0]  # connection established

                # converting numpy array to bytes using pickling

                self.str1 = pickle.dumps(self.r_alt)
                self.str2 = pickle.dumps(self.key)

                # sending data to client

                self.c.send(self.str1)
                self.c.send(self.str2)

                exit(0)

        except Exception as ex:
            tkinter.messagebox.showerror("Upload Image First",ex)

        except ValueError as v:
            tkinter.messagebox.showerror("Key not generated",v)


root=Tk()
root.title("Server")
form_obj=form(root)
root.mainloop()

