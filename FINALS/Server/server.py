import socket 
import threading
import os
from time import sleep
import csv
import pandas as pd
from random import randint
#server headers
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
Parent_dir="E:\\PYTHON_LAB_STUFF\\CN project python\\FINALS\\Server"
msgnamescheck=["msg",".txt"]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
def alert(conn,addr):
    ale = conn.recv(1024).decode(FORMAT)
    if ale == DISCONNECT_MESSAGE:
        connected = False
        print(f"[{addr}] {ale}")
        conn.close()
        print("close")
def fil(conn,addr,i):
    k=str(i)
    f=open("mm_%s.txt" %k ,'w')
    msg = conn.recv(1024).decode(FORMAT)
    f.write(msg)
    print(f"[{addr}] {msg}")
def createclassroom(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    id=msg.strip().split(',')
    print("id:-",id)
    path = os.path.join(Parent_dir,id[2]) 
    print('path',path)
    os.mkdir(path)
    if(id[1]=="teacher"):
        df = pd.read_csv('teacher.csv',index_col="name")
    else:
        df = pd.read_csv('student.csv',index_col="name")  
    for row_series in df.values:
        print("before update:-",row_series)
    i=0
    for row_series in df.values:
        print("current rows:--",row_series)
        if(row_series[0]==id[0]):
            print("checking:-",type(row_series[2]))
            temp=row_series[2]
            print("edited:-",temp)
            try:
                df.iloc[i,2] = temp + id[2]+':'
            except:
                df.iloc[i,2] =id[2]+':'
        i+=1
    for row_series in df.values:
        print("after updated:-",row_series)
    if(id[1]=="teacher"):
        df.to_csv('teacher.csv')
    else:
        df.to_csv('student.csv') 
          

    print(f"classroom:[{addr}] {msg}")

def joinclassrooms(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    id=msg.strip().split(',')
    print("id:-",id)
    path = Parent_dir
    print('path',path)
    folderfileslist=os.listdir(path)
    print(folderfileslist)
    isthere=False
    for folder in folderfileslist:
        if(folder==id[2]):
            isthere=True
    if(isthere==False):
        send_msg="False".encode(FORMAT)
        conn.send(send_msg)
        return
    if(id[1]=="teacher"):
        df = pd.read_csv('teacher.csv',index_col="name")
    else:
        df = pd.read_csv('student.csv',index_col="name")  
    for row_series in df.values:
        print("before update:-",row_series)
    i=0
    for row_series in df.values:
        print("current rows:--",row_series)
        if(row_series[0]==id[0]):
            print("checking:-",type(row_series[2]))
            temp=row_series[2]
            print("edited:-",temp)
            try:
                df.iloc[i,2] = temp + id[2]+':'
            except:
                df.iloc[i,2] =id[2]+':'
        i+=1
    for row_series in df.values:
        print("after updated:-",row_series)
    if(id[1]=="teacher"):
        df.to_csv('teacher.csv')
    else:
        df.to_csv('student.csv') 
    send_msg="True".encode(FORMAT)
    conn.send(send_msg)
    print(f"classroom:[{addr}] {msg}")


def message(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    s=msg.split(':')
    path=os.path.join(Parent_dir,s[0])
    folderfileslist=os.listdir(path)
    nooffiles=len(folderfileslist)
    print("files",nooffiles)
    print("no.of files",nooffiles)
    path+="\\msg"+str(nooffiles+1)+".txt"
    print(path)
    mess=open(path,'w')
    mess.write(s[1])
    print(f"message:[{addr}] {msg}")
def sendbackmessages(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    msg.strip()
    path=os.path.join(Parent_dir,msg)
    print("sent file location:",path)
    k=os.listdir(path)
    p=len(k)
    print("total number of folders:",p)
    sleep(0.2)
    send_msg=str(p).encode(FORMAT)
    conn.send(send_msg)
    sleep(0.2)
    for file in os.listdir(path):
        if any(x not in file for x in msgnamescheck):
            m="file"+":"+file
        else:
            msgpath=path+"\\"+file
            f=open(msgpath)
            m=f.read()
            m="msg"+":"+m
        send_msg=str(m).encode(FORMAT)
        conn.send(send_msg)
        sleep(0.2)
def getdocs(conn,addr):
    filename = conn.recv(1024).decode(FORMAT)
    print("filename:-",filename)
    filedir = conn.recv(1024).decode(FORMAT)
    print("filedir:-",filedir)
    msg_byte = conn.recv(1024).decode(FORMAT)
    print("msg_byte:-",msg_byte)
    msg = conn.recv(int(msg_byte))
    path=os.path.join(Parent_dir,filedir,filename)
    fil=open(path,'wb')
    fil.write(msg)

def sendfiles(conn,addr):
    filepath = conn.recv(1024).decode(FORMAT)
    print(filepath)
    print(f"message:[{addr}] {filepath}")
    path=Parent_dir+"\\"+filepath
    f=open(path,'rb')
    m=f.read()
    sleep(0.5)
    lengthoffile=len(m)
    file_length=str(lengthoffile).encode(FORMAT)
    conn.send(file_length)
    sleep(0.5)
    conn.send(m)
    sleep(0.2)
def teachersignup(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    row=msg.split(',')
    row.append(None)
    print("teacher:-",row)
    f=open('teacher.csv', 'a+',)
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()
def studentsignup(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    row=msg.split(',')
    row.append(None)
    print("student:-",row)
    f=open('student.csv', 'a+',)
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def logincheck(conn,addr):
    found=False
    msg = conn.recv(1024).decode(FORMAT)
    id=msg.strip().split(',')
    if(id[2]=="1"):
        f=open('teacher.csv','r')
    else:
        f=open('student.csv','r')
    csvreader = csv.reader(f)
    for row in csvreader:
        if(len(row)>=1):
            print(row)
            if(row[1]==id[0]):
                if(row[2]==id[1]):
                    found=True
                    break
    f.close()
    sleep(0.2)
    print("found:-",found)
    fondornot=str(found).encode(FORMAT)
    conn.send(fondornot)
def sendclassrooms(conn,addr):
    classroomlst=""
    msg = conn.recv(1024).decode(FORMAT)
    id=msg.strip().split(',')
    if(id[1]=="teacher"):
        f=open('teacher.csv','r')
        print("opened teacher")
    else:
        f=open('student.csv','r')
        print("opened student")
    csvreader = csv.reader(f)
    for row in csvreader:
            if(len(row)>=1 and row[1]==id[0]):
                print("row:-",row)
                if(len(row[3])==0):
                    classroomlst="-"
                else:
                    classroomlst=row[3]
                break
    print("clases:-",classroomlst)
    classes=str(classroomlst).encode(FORMAT)
    sleep(0.2)
    conn.send(classes)

def sendtextcaptcha(conn,addr):
    num = randint(0,1070)
    print("random value:-",num)
    dir_list = os.listdir(Parent_dir+"\\samples")
    print("random file chosen:-",dir_list[num])
    f=open(Parent_dir+"\\samples\\"+dir_list[num],"rb")
    m=f.read()
    size=str(len(m)).encode(FORMAT)
    sleep(0.2)
    conn.send(size)
    sleep(0.2)
    conn.send(m)
    sleep(0.2)
    imgname=str(dir_list[num]).encode(FORMAT)
    conn.send(imgname)
    sleep(0.2)
    print("image sent")


def handle_client(conn, addr):
    sleep(0.2)
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        if(connected==False):
            return
        msg_type = conn.recv(HEADER).decode(FORMAT)
        if msg_type:
            print("type:-",msg_type)
            if(msg_type=="alert"):
                alert(conn,addr)
            if(msg_type=="filee"):
                fil(conn,addr,i)
                i+=1
            if(msg_type=="classroom"):
                createclassroom(conn,addr)
            if(msg_type=="message"):
                message(conn,addr)
            if(msg_type=="send"):
                sendbackmessages(conn,addr)
            if(msg_type=="doc"):
                getdocs(conn,addr)
            if(msg_type=="download"):
                sendfiles(conn,addr)
            if(msg_type=="teachersignup"):
                teachersignup(conn,addr)
            if(msg_type=="studentsignup"):
                studentsignup(conn,addr)
            if(msg_type=="login"):
                logincheck(conn,addr)
            if(msg_type=="sendclassrooms"):
                sendclassrooms(conn,addr)
            if(msg_type=="joinclassroom"):
                joinclassrooms(conn,addr)
            if(msg_type=="textcaptcha"):
                sendtextcaptcha(conn,addr)
            
    print("closed")
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()