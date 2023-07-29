
import os
import tkinter as tk              
from tkinter import END,LEFT,RIGHT,Button, Entry, IntVar, Label, StringVar, Text,Canvas,Frame,LabelFrame, Variable,Scrollbar, Radiobutton, font  as tkfont 
import socket
from PIL import ImageTk, Image ,ImageFont, ImageDraw
import threading
from time import sleep
from tkinter import filedialog
import sys
from hashlib import sha512
import lc4
class variable_holder(object):
    classroomlst=[]
    currentclassname=""
    currentusername=""
    currentuserprofession=""
    imgname = ""

    @classmethod
    def getclassroomlist(cls,lst):
        cls.classroomlst=lst
        print("got it",cls.classroomlst)
    @classmethod
    def gtcurrentclassname(cls,name):
        cls.currentclassname=name
        print("got it",cls.currentclassname)
    @classmethod
    def gtcurrentusername(cls,name):
        cls.currentusername=name
        print("got it",cls.currentusername)
    @classmethod
    def gtcurrentuserproffesion(cls,name):
        if(name==1):
            pro="teacher"
        else:
            pro="student"
        cls.currentuserprofession=pro
        print("got it",cls.currentuserprofession)
    @classmethod
    def getcaptchaname(cls,name):
        cls.imgname=name[:-4]
        print("got it",cls.imgname)

class clientinterface:
    def __init__(self):
        print("client started")
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = sys.argv[1]
        self.ADDR = (self.SERVER,self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    
    def sendalert(self,msg):
        message = msg.encode(self.FORMAT)
        msg_type= "alert"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.5)
        self.client.send(message)

    def sendfile(self):
        f=open("kk.txt")
        data=f.read()
        message = data.encode(self.FORMAT)
        msg_type = "filee"
        send_length = str(msg_type).encode(self.FORMAT)
        self.client.send(send_length)
        sleep(1)
        self.client.send(message)

    def sendclassroom(self,msg):
        msg=variable_holder.currentusername+','+variable_holder.currentuserprofession + ','+msg
        message = msg.encode(self.FORMAT)
        msg_type= "classroom"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)
    
    def joinclassroom(self,msg):
        msg=variable_holder.currentusername+','+variable_holder.currentuserprofession + ','+msg
        message = msg.encode(self.FORMAT)
        msg_type= "joinclassroom"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)
        sleep(0.2)
        status=self.client.recv(2048).decode(self.FORMAT)
        return status


    def sendmessage(self,msg):
        message=variable_holder.currentusername +"-"+ msg
        msg=message
        msg=variable_holder.currentclassname+":"+msg
        message = msg.encode(self.FORMAT)
        msg_type= "message"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)

    def senddocs(self,docdir):
        f=open(docdir,'rb')
        message=f.read()
        msg_type= "doc"
        lstofdir=docdir.split('/')
        filename=lstofdir[len(lstofdir)-1]
        filename_byte=str(filename).encode(self.FORMAT)
        send_type = str(msg_type).encode(self.FORMAT)
        filedir=str(variable_holder.currentclassname).encode(self.FORMAT)
        msg_bytes=str(len(message)).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.5)
        self.client.send(filename_byte)
        sleep(0.5)
        self.client.send(filedir)
        sleep(0.5)
        self.client.send(msg_bytes)
        sleep(0.5)
        self.client.send(message)
    
    def getmessagesfromserver(self):
        message = variable_holder.currentclassname.encode(self.FORMAT)
        msg_type="send"
        send_type=str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.5)
        self.client.send(message)
        sleep(0.2)
        lstofmessages=[]
        msg=""
        lengthofmessage=self.client.recv(2048).decode(self.FORMAT)
        if(lengthofmessage==0):
            exit
        print("length of file:",lengthofmessage)
        for i in range(int(lengthofmessage)):
            msg=self.client.recv(2048).decode(self.FORMAT)
            lstofmessages.append(msg)
            print("msg:-",msg)
        sleep(0.2)
        for i in range(int(lengthofmessage)):
            if "msg:" in lstofmessages[i]:
                text=lstofmessages[i].split(":")
                text[1]=text[1].strip()
                lstofmessages[i]=":".join(text)
        return lstofmessages
    
    def downloadfromserver(self,filename):
        filepath = filename.encode(self.FORMAT)
        msg_type= "download"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(filepath)
        lengthof_file=self.client.recv(2048).decode(self.FORMAT)
        print("length og file:-",lengthof_file)
        msg=self.client.recv(int(lengthof_file))
        justthefilename=str(filename).split("\\")
        print("justfilename:-",justthefilename)
        path=os.getcwd() + str("\\") + justthefilename[1]
        print("download file:-",path)
        f=open(path,'wb')
        f.write(msg)

    def signupteacher(self,msg):
        message = msg.encode(self.FORMAT)
        msg_type= "teachersignup"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)
    def signupstudent(self,msg):
        message = msg.encode(self.FORMAT)
        msg_type= "studentsignup"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)

    def logincheck(self,id):
        message = id.encode(self.FORMAT)
        msg_type= "login"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)
        sleep(0.2)
        msg=self.client.recv(1024).decode(self.FORMAT)
        print("msgcheck:-",msg)
        return msg
    def addingclassroomsback(self):
        classdetails=variable_holder.currentusername+","+variable_holder.currentuserprofession
        message = classdetails.encode(self.FORMAT)
        msg_type= "sendclassrooms"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(1)
        self.client.send(message)
        sleep(0.2)
        print("getting classes")
        msg=self.client.recv(1024).decode(self.FORMAT)
        print("classes of list-",msg)
        if(msg=="-"):
            classes=[]
        else:
            msg=msg.strip()
            classes=msg.split(':')[:-1]
        variable_holder.getclassroomlist(classes)
    def gettextcaptcha(self):
        msg_type="textcaptcha"
        img=open("Images/temp.PNG",'wb')
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.1)
        imgsize=self.client.recv(1024)
        print("size",imgsize)
        imgdata=self.client.recv(int(imgsize))
        imgname=self.client.recv(1024).decode(self.FORMAT)
        variable_holder.getcaptchaname(imgname)
        img.write(imgdata)
    def closeprogram(self):
        done="!DISCONNECT"
        message = done.encode(self.FORMAT)
        msg_type= "alert"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.3)
        self.client.send(message)
    





class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Sans', size=18, weight="bold", slant="italic")
        #self.attributes('-fullscreen', True)
        self.geometry('1920x1080')
        self.configure(bg="#ffffff")
        container = tk.Frame(self,bg="Red")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.wm_attributes('-fullscreen', 'True')
        closeimage= ImageTk.PhotoImage(Image.open("Images/close_button.png"))
        self.quitt=Button(self,text="close",image=closeimage,padx=10,pady=10,command=self.close)
        self.quitt.place(x=1480,y=5)
        self.quitt.image=closeimage
        self.frames = {}
        for F in (StartPage, PageOne,LoginPage,SignupPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")             # change
    def close(self):
        clint.closeprogram()
        self.destroy()
        pass
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def show_page(self, page_name,name):
        '''Show a frame for the given page name'''
        print("in nams",name)
        variable_holder.gtcurrentclassname(name)
        frame = self.frames[page_name]
        self.frames[page_name].setname()
        self.frames[page_name].getmessagesback()
        frame.tkraise()
    def updateStartpage(self,page_name):
        frame = self.frames[page_name]
        self.frames[page_name].updatetitle()
    def reset_page(self):
        self.show_frame("LoginPage")
        self.frames["LoginPage"].resetpage()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        gcrbackimage=Image.open("Images/GCR_background.jpg")
        gcraddimage=Image.open("Images/GCR_add.jpg")
        gcrjoinimage=Image.open("Images/GCR_join.jpg")
        

        gcrbackimage=gcrbackimage.resize((1500,705))
        gcraddimage=gcraddimage.resize((47,45))
        gcrjoinimage=gcrjoinimage.resize((143,43))

        bg = ImageTk.PhotoImage(gcrbackimage)
        add = ImageTk.PhotoImage(gcraddimage)
        join = ImageTk.PhotoImage(gcrjoinimage)


        
        self.inc=0
        self.btnlst=[]
        tk.Frame.__init__(self, parent)
        self.config(bg="white")    
        self.controller = controller

        label1 = Label(self, image = bg,bg="white")
        label1.place(x=9,y=50)
        label1.configure(image=bg)
        label1.image=bg
        self.fram=tk.Frame(self,bg="white")
        self.fram.place(x=30,y=200)
        sleep(0.2)
        self.Buttonadd=Button(self,text="add",image=add,command=lambda:self.openNewWindow(parent))
        self.Buttonadd.place(x=1300,y=60)
        self.Buttonadd.image=add
        self.Buttonjoin=Button(self,text="join",image=join,command=lambda:self.opennewWindowjoin(parent))
        self.Buttonjoin.place(x=1100,y=60)
        self.Buttonjoin.image=join

    def restart(self):
        self.controller.reset_page()
        variable_holder.getclassroomlist([])
        variable_holder.gtcurrentclassname("")
        variable_holder.gtcurrentusername("")
        variable_holder.gtcurrentuserproffesion("")

    def addclassroomsfirst(self):
        print("created")
        print(len(variable_holder.classroomlst))
        for clas,i in zip(variable_holder.classroomlst,range(len(variable_holder.classroomlst))):
            self.gcrbuttonimage=Image.open("Images/GCR_button.jpg")
            self.gcrbuttonimage=self.gcrbuttonimage.resize((270,265))
            text_font=ImageFont.truetype("arial.ttf",35)
            edit_image=ImageDraw.Draw(self.gcrbuttonimage)
            edit_image.text((60,100),clas,("red"),font=text_font)
            self.gcrbuttonimage.save("Images/buttonim.jpg")
            im=ImageTk.PhotoImage(Image.open("Images/buttonim.jpg"))
            sleep(2)
            self.btnlst.append(Button(self.fram,image=im,text=clas,command=lambda c=i: self.controller.show_page("PageOne",self.btnlst[c].cget("text"))))
            self.btnlst[i].grid(row=0,column=self.inc,padx=10)
            self.btnlst[i].image=im
            os.remove("Images/buttonim.jpg")
            self.inc+=1
            if(self.inc==5):
                self.Buttonadd["state"]="disabled"
            print("inc value:-",self.inc)

    def addbutton(self):
        if(self.widget_name.get()==""):
            return
        print("length:-",len(variable_holder.classroomlst))
        self.gcrbuttonimage=Image.open("Images/GCR_button.jpg")
        self.gcrbuttonimage=self.gcrbuttonimage.resize((270,265))
        text_font=ImageFont.truetype("arial.ttf",35)
        edit_image=ImageDraw.Draw(self.gcrbuttonimage)
        edit_image.text((60,100),self.widget_name.get(),("red"),font=text_font)
        self.gcrbuttonimage.save("Images/buttonim.jpg")
        im=ImageTk.PhotoImage(Image.open("Images/buttonim.jpg"))
        sleep(2)
        self.btnlst.append(Button(self.fram,image=im,text=self.widget_name.get(),command=lambda c= len(self.btnlst): self.controller.show_page("PageOne",self.btnlst[c].cget("text"))))
        self.btnlst[-1].grid(row=0,column=self.inc,padx=10)
        self.btnlst[-1].image=im
        os.remove("Images/buttonim.jpg")
        self.inc+=1
        if(self.inc==5):
            self.Buttonadd["state"]="disabled"
        print("inc value:-",self.inc)
        clint.sendclassroom(self.widget_name.get())
        self.newWindow.destroy()

    def joinbutton(self):
        if(self.widget_name.get()==""):
            return
        status=clint.joinclassroom(self.widget_name.get())
        if(status=="True"):
            print("length:-",len(variable_holder.classroomlst))
            self.gcrbuttonimage=Image.open("Images/GCR_button.jpg")
            self.gcrbuttonimage=self.gcrbuttonimage.resize((270,265))
            text_font=ImageFont.truetype("arial.ttf",35)
            edit_image=ImageDraw.Draw(self.gcrbuttonimage)
            edit_image.text((60,100),self.widget_name.get(),("red"),font=text_font)
            self.gcrbuttonimage.save("Images/buttonim.jpg")
            im=ImageTk.PhotoImage(Image.open("Images/buttonim.jpg"))
            self.btnlst.append(Button(self.fram,image=im,text=self.widget_name.get(),command=lambda c= len(self.btnlst): self.controller.show_page("PageOne",self.btnlst[c].cget("text"))))
            self.btnlst[-1].grid(row=0,column=self.inc,padx=10)
            self.btnlst[-1].image=self.im
            self.inc+=1
            if(self.inc==5):
                self.Buttonjoin["state"]="disabled"
            print("inc value:-",self.inc)
            self.newWindow.destroy()
        else:
            print("not there")
    def opennewWindowjoin(self,parent):
        self.widget_name=StringVar()    
        self.newWindow = tk.Toplevel(parent)
        self.newWindow.title("New Window")
        self.newWindow.geometry("200x200")
        Label(self.newWindow,text ="enter name").pack()
        Entry(self.newWindow,textvariable=self.widget_name).pack()
        Button(self.newWindow,text="submit",command=self.joinbutton).pack()
    def openNewWindow(self,parent):
        self.widget_name=StringVar()    
        self.newWindow = tk.Toplevel(parent)
        self.newWindow.title("New Window")
        self.newWindow.geometry("200x200")
        Label(self.newWindow,text ="enter name").pack()
        Entry(self.newWindow,textvariable=self.widget_name).pack()
        Button(self.newWindow,text="submit",command=self.addbutton).pack()
    def updatetitle(self):
        if(variable_holder.currentuserprofession=="student"):
            self.Buttonadd["state"] = "disabled"
            self.Buttonjoin["state"] = "normal"
        else:
            self.Buttonadd["state"] = "normal"
            self.Buttonjoin["state"] = "disabled"
        clint.addingclassroomsback()
        self.addclassroomsfirst()
        
        

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="white")    
        self.controller = controller
        wrapper1 = Frame(self,width=300,height=700,bg="white")
        mycanvas = Canvas(wrapper1,width=700,height=300,bg="white")
        mycanvas.pack(side=LEFT)
        yscrollbar = Scrollbar(wrapper1,orient="vertical",command=mycanvas.yview,bg="white")
        yscrollbar.pack(side=RIGHT,fill="y")
        mycanvas.configure(yscrollcommand=yscrollbar.set)
        self.myframe=Frame(mycanvas,bg="white")
        mycanvas.create_window((0,0),window=self.myframe,anchor="nw")
        mycanvas.bind('<Configure>',lambda e: mycanvas.configure( scrollregion = (0,0,2000,2000)))
        wrapper1.place(x=600,y=420)

        bgclassroomimage=Image.open("Images/backgroundofclassroom.jpg")
        bgclassroomimage=bgclassroomimage.resize((1499,341))
        bg = ImageTk.PhotoImage(bgclassroomimage)
        addmessimage=Image.open("Images/Addmessages.jpg")
        addmessimage=addmessimage.resize((190,97))
        addmess = ImageTk.PhotoImage(addmessimage)
        addfilesimage=Image.open("Images/Addfiles.jpg")
        addfilesimage=addfilesimage.resize((190,97))
        addfiles = ImageTk.PhotoImage(addfilesimage)
        gobackimage=Image.open("Images/Goback.jpg")
        gobackimage=gobackimage.resize((80,40))
        goback = ImageTk.PhotoImage(gobackimage)

        self.label=Label(self,image=bg,bg="white")
        self.label.place(x=30,y=50)
        self.label.image=bg
        print("name=",variable_holder.currentclassname)
        Buttongoback=Button(self,text="goback",image=goback,command=self.goback)
        Buttongoback.image=goback
        Buttongoback.place(x=125,y=60)
        Buttonaddcontent=Button(self,text="add\nmessage",image=addmess,command=lambda: self.openwindowmess(parent))
        Buttonaddcontent.place(x=270,y=390)
        Buttonaddcontent.image=addmess
        Buttonadddoc=Button(self,text="add\nfiles",image=addfiles,command=self.openwindowdoc)
        Buttonadddoc.image=addfiles
        Buttonadddoc.place(x=270,y=520)
    def setname(self):
        self.gcrbgimage=Image.open("Images/backgroundofclassroom.jpg")
        self.gcrbgimage=self.gcrbgimage.resize((1499,341))
        text_font=ImageFont.truetype("arial.ttf",35)
        edit_image=ImageDraw.Draw(self.gcrbgimage)
        edit_image.text((300,240),variable_holder.currentclassname,("blue"),font=text_font)
        self.gcrbgimage.save("Images/bgofclassroom.jpg")
        im=ImageTk.PhotoImage(Image.open("Images/bgofclassroom.jpg"))
        self.label.config(image=im)
        self.label.image=im
        #self.label.config(text="This page is "+variable_holder.currentclassname)
        pass

    def getmessagesback(self):
        lst=clint.getmessagesfromserver()
        for message in lst:
            mfilel=message.split(":")
            frame=tk.Frame(self.myframe)
            frame.pack()
            if mfilel[0]=="msg":
                label=tk.Label(self.myframe,text=mfilel[1],font=self.controller.title_font,bg="white")
                label.pack()
            if mfilel[0]=="file":
                button=tk.Button(self.myframe,text=mfilel[1],bg="white",font=self.controller.title_font,command=lambda : self.downloadfile(variable_holder.currentclassname+"\\"+button.cget('text') ))
                button.pack()

        print(lst)

    def addmessage(self,message):
        label=tk.Label(self.myframe,text=message,font=self.controller.title_font,padx=10,pady=10,bg="white")
        label.pack(padx=10,pady=10)
        clint.sendmessage(message)
        self.newWindow.destroy()
    def openwindowmess(self,parent):  
        self.newWindow = tk.Toplevel(parent)
        self.newWindow.title("New Window")
        self.newWindow.geometry("200x200")
        Label(self.newWindow,text ="enter message").pack()
        mess=Text(self.newWindow,width=10,height=5,padx=10,pady=20)
        mess.pack()
        print(mess.get(1.0,END))
        Button(self.newWindow,text="submit",command=lambda: self.addmessage(mess.get(1.0,END))).pack()

    def openwindowdoc(self):
        self.filename=filedialog.askopenfilename(initialdir=os.getcwd,title="open the file",filetypes=(("pdf files","*.pdf"),("all files","*.*")))
        print(self.filename)
        clint.senddocs(self.filename)
        lstofdir=self.filename.split('/') 
        filename=lstofdir[len(lstofdir)-1]
        print("filename:-",filename)
        print("filepath argument:-",variable_holder.currentclassname+"\\"+filename)
        button=tk.Button(self.myframe,text=filename,bg="white",font=self.controller.title_font,command=lambda:self.downloadfile(variable_holder.currentclassname+"\\"+filename))
        button.pack()

    def downloadfile(self,filepath):
        clint.downloadfromserver(filepath)

    def goback(self):
        for widgetname in self.myframe.winfo_children():
            widgetname.destroy()  
        os.remove("Images/bgofclassroom.jpg")
        self.controller.show_frame("StartPage")

class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        signupimage=Image.open("Images/google_signup.png")
        signupbuttonimage=Image.open("Images/signup_button.png")
        signupimage=signupimage.resize((373,477))
        signupbuttonimage=signupbuttonimage.resize((279,41))
        bg = ImageTk.PhotoImage(signupimage)
        sign= ImageTk.PhotoImage(signupbuttonimage) 
        self.inc=1
        self.btnlst=[]
        tk.Frame.__init__(self, parent)
        self.config(bg="white")        
        self.controller = controller
        self.nam=StringVar()
        self.user=StringVar()
        self.passw=StringVar()
        self.profession=IntVar()
        self.fram=tk.Frame(self)
        self.fram.pack()

        label1 = Label(self, image = bg,bg="white")
        label1.place(x=600,y=100)
        label1.configure(image=bg)
        label1.image=bg
        self.name=Entry(self,textvariable=self.nam,width=15,font=('Arial 24'))
        self.name.place(x=652,y=326)
        self.name.insert(0, "Name")
        self.name.bind("<FocusIn>", self.temp_text1)
        self.username=Entry(self,textvariable=self.user,width=15,font=('Arial 24'))
        self.username.place(x=652,y=373)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.temp_text2)
        self.password=Entry(self,textvariable=self.passw,width=15,font=('Arial 24'))
        self.password.place(x=652,y=420)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.temp_text3)
        teacher = Radiobutton(self, text="teacher", variable=self.profession, value=1,font=('Arial 18'))  
        teacher.place(x=650,y=225)
        student = Radiobutton(self, text="student", variable=self.profession, value=2,font=('Arial 18'))  
        student.place(x=650,y=275)    
        Buttonlogin=Button(self,text="signup",image=sign,command=lambda:self.jumptosignup())
        Buttonlogin.place(x=645,y=465)
        Buttonlogin.image=sign

        self.error = Label(self,text="")
        self.error.place(x=650,y=540) 

    def temp_text1(self,e=None):
        self.name.delete(0,"end")
    def temp_text2(self,e=None):
        self.username.delete(0,"end")
    def temp_text3(self,e=None):
        self.password.delete(0,"end")
    def jumptosignup(self):
        if(self.nam.get()=="" or self.nam.get()=="Name" or self.user.get()=="" or self.user.get()=="Username" or self.passw.get()=="" or self.passw.get()=="Password" or self.profession.get()==0 ):
            self.error.config(text="missing parameters",fg="red")
            return
        
        msg=",".join([self.nam.get(),self.user.get(),sha512(self.passw.get().encode()).hexdigest()])
        if self.profession.get()==1:
            clint.signupteacher(msg)
        else:
            clint.signupstudent(msg)
        self.controller.show_frame("LoginPage")
             
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        clint.gettextcaptcha()
        loginimage=Image.open("Images/google_login.png")
        signimage=Image.open("Images/sign_button.png")
        loginimage=loginimage.resize((373,477))
        signimage=signimage.resize((279,41))
        bg = ImageTk.PhotoImage(loginimage)
        sign= ImageTk.PhotoImage(signimage) 
        self.inc=1
        self.btnlst=[]
        tk.Frame.__init__(self, parent)
        self.config(bg="white")
        label1 = Label(self, image = bg)
        label1.place(x=600,y=100)
        label1.configure(image=bg,bg="white")
        label1.image=bg
        self.controller = controller
        self.user=StringVar()
        self.passw=StringVar()
        self.cap=StringVar()
        self.profession=IntVar()
        self.fram=tk.Frame(self)
        self.fram.pack()
        self.username=Entry(self,textvariable=self.user,width=15,font=('Arial 24'))
        self.username.place(x=650,y=300)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.temp_text1)
        self.password=Entry(self,textvariable=self.passw,width=15,font=('Arial 24'))
        self.password.place(x=650,y=360) 
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.temp_text2)  
        img1= ImageTk.PhotoImage(Image.open("Images/start.PNG"))
        self.captcha=Label(self,text="hello",image=img1)
        self.captcha.image=img1
        self.captcha.place(x=620,y=410)
        self.textcap=Entry(self,textvariable=self.cap,width=8,font=('Arial 22'))
        self.textcap.place(x=815,y=418)

        teacher = Radiobutton(self, text="teacher", variable=self.profession, value=1,font=('Arial', 18))  
        teacher.place(x=620,y=230)
        student = Radiobutton(self, text="student", variable=self.profession, value=2,font=('Arial', 18))  
        student.place(x=820,y=230)       
        Buttonlogin=Button(self,text="login",command=self.logintoclassroom,image=sign)
        Buttonlogin.place(x=645,y=465)
        Buttonlogin.image=sign
        Buttonsignup=Button(self,text="dont have account",command=lambda:self.controller.show_frame("SignupPage"))
        Buttonsignup.place(x=820,y=515)
        self.error = Label(self)
        self.error.place(x=650,y=540)
        self.updatecaptchatext()
    def temp_text1(self,e=None):
        self.username.delete(0,"end")
    def temp_text2(self,e=None):
        self.password.delete(0,"end")   
        self.password.config(show="*")    
    def logintoclassroom(self):
        if(self.username.get()=="" or self.username.get()=="Username" or self.password.get()=="" or self.password.get()=="Password" or self.profession.get()==0 or self.textcap.get()==""):
            self.error.config(text="missing parameters",fg="red")
            return
        value=self.textcap.get()
        actualvalue=variable_holder.imgname
        print("enter value:-",value)
        print("actual value:-",actualvalue)
        if(value!=actualvalue):
            self.error.config(text="wrong captcha",fg="red")
            return
        id=self.username.get()+","+ sha512(self.password.get().encode()).hexdigest() +","+str(self.profession.get())
        isavailable=clint.logincheck(id)
        isavailable.strip()
        if isavailable=="True":
            print("switched")
            variable_holder.gtcurrentusername(self.username.get())
            variable_holder.gtcurrentuserproffesion(self.profession.get())
            self.controller.updateStartpage("StartPage")
            self.controller.show_frame("StartPage")
        else:
            self.error.config(text="wrong credentials",fg="red")
            self.loading.config(text="")     
    def updatecaptchatext(self):
        print("image updated")
        c=Image.open("Images/temp.PNG")
        c=c.resize((180,50))
        img = ImageTk.PhotoImage(c)
        print(img)
        self.captcha.configure(image=img)
        self.captcha.image=img
   

if __name__ == "__main__":
    clint=clientinterface()
    app = SampleApp()
    app.mainloop()