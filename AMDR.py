import os
import paramiko
import stat
from tkinter import *
from tkinter import Tk, StringVar, Label, Entry, Button
from functools import partial
def config():
    global sftp
    global ssh
    file = open("mdp.txt", "r")
    mdp = file.read()
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('id', username='username', password=mdp, port='port')
    print("connected")
    sftp = ssh.open_sftp()
    aff()
def aff():
    root = Tk()
    root.title("Amdr")
    root.geometry("1920x1080")
    root.minsize(400, 300)
    root.config(background='#260A85')
    frame = Frame(root, bg = "#260A85")
    framebis =  Frame(root, bg = "#260A85")
    title = Label(root, text = "Welcome in Amdr", font = ("Arial", 25), bg = "#260A85", fg = "#FFFFFF")
    title.pack()
    paths = StringVar(root)
    turl = Label(framebis, text = "chemin du fichier/dossier (dossier uniquement pour dl)", font = ("Arial", 25), bg = "#260A85", fg = "#FFFFFF")
    turl.pack()
    path = Entry(framebis, text = "path", textvariable = paths,font = ("Arial", 25), bg = "#FFFFFF", fg = "#260A85" )
    path.pack()
    dossS = StringVar(root)
    Tlabel = StringVar(root)
    tur = Label(framebis, text = "nom du fichier sur le serveur (nom donne a l'upload)", font = ("Arial", 25), bg = "#260A85", fg = "#FFFFFF")
    tur.pack()
    doss = Entry(framebis, text = "Nom du dossier", textvariable = dossS,font = ("Arial", 25), bg = "#FFFFFF", fg = "#260A85" )
    doss.pack()
    lunch = Button(frame, text = "upload",font = ("Arial", 25), bg = "#FFFFFF", fg = "#260A85", command = partial(upper, path,dossS,Tlabel))
    lunch.pack()
    lunc = Button(frame, text = "download",font = ("Arial", 25), bg = "#FFFFFF", fg = "#260A85", command = partial(downer, path,dossS,Tlabel))
    lunc.pack()
    frame.pack(side = BOTTOM)
    turl = Label(framebis,textvariable = Tlabel , font = ("Arial", 25), bg = "#260A85", fg = "#FFFFFF")
    turl.pack()
    framebis.pack(expand = YES)
    root.mainloop()
def upper(path,doss,Tlabel,root):
    path2 = path.get()
    doss = doss.get()
    dir = os.listdir(path2)
    try:
        ssh.exec_command('mkdir /root/drive/'+doss)
    except FileExistsError:
        pass 
    path = "/root/drive/" + doss + "/"
    Tlabel.set("Begining process")
    for x in dir:
        path3 = path2 + "\\" + x 
        print(path3)
        if os.path.isfile(path3):
            local = path3
            remo = path + x 
            sftp.put(local,remo)    
        if os.path.isdir(path3):
            do = 0
            upfiler(path,x,doss,do,path3)
            path3 = path2
            path = "/root/drive/" + doss + "/"
        else:
            local = path3
            remo = path + x 
            sftp.put(local,remo)
    Tlabel.set("done")
def downer(pa, doss,Tlabel):
    doss = doss.get()
    pat = str(pa.get())
    print (pat,doss)
    try:
        os.mkdir(pat +r'\\' + doss)
        pat = pat + '\\' + doss + "\\"
    except FileExistsError:
        a = 1
        pat = pat +'\\' + doss +"\\"
    remo = "/root/drive/" + doss + "/"
    dir = sftp.listdir(remo)
    Tlabel.set("begining process")
    for x in dir:
        print(x)
        if stat.S_ISREG(sftp.stat(os.path.join(remo, x)).st_mode):
            try:
                local = pat +  x
                rem = remo + x
                print(local,rem)
                sftp.get(rem,local)
            except:
                pass
        if stat.S_ISDIR(sftp.stat(os.path.join(remo, x)).st_mode):
            try:
                do = 0
                pa = pat
                downfile(pa,remo,x,doss,do)
                remo = "/root/drive/" + doss + "/"
            except:
                pass
    Tlabel.set("done")
def downfile(path,remo,x,doss,do):
    print(x)
    if do != 0:
        remo = remo  + do + "/"
        path = path + r"\\" + do + "\\"
        print(path)
        try:
            os.mkdir(path + r"\\" + do)
        except FileExistsError:
            pass
    else:
        remo = remo  + x + "/"
        print(x, "rrs")
        print(path, "ee")
        try:
            os.mkdir(path + r"\\" + x)
            path = path + r"\\" + x + "\\"
        except FileExistsError:
            pass
    dir = sftp.listdir(remo)
    for x in dir:   
        if stat.S_ISREG(sftp.stat(os.path.join(remo, x)).st_mode):
            try:
                local = path + x
                rem = remo + x
                print(local,rem)
                sftp.get(rem,local)
            except:
                pass
        if stat.S_ISDIR(sftp.stat(os.path.join(remo, x)).st_mode):
            downfile(path,remo,x,doss,do)

def upfiler(path,x,doss,do,di):
    if do != 0:
        print(di)
        print(x)
        x = x + "\\" + do
        o=do.replace(" ", "\ ")
        print(path + o)
        path2 = path.replace(" ", "\ ")
        ssh.exec_command('mkdir '+ path2 + o)
        path = path + do + "/"
    else:
        o=x.replace(" ", "\ ")
        print(os.path.abspath(x) + " mdr")
        ssh.exec_command('mkdir '+ path + o)
        path = path + x + "/"
        print(x)
        x = di
    print(di)
    dir = os.listdir(x)
    print(x)
    for y in dir:
        print("fefefefef " + path)
        print( x + "\\" + y)
        g = path
        if os.path.isfile(x + "\\" + y):
            local = x + "\\" + y
            remo = path + y
            print(remo)
            sftp.put(local,remo)
        elif os.path.isdir(x + "\\" + y):
            upfiler(path,x,doss,y,di)
config()
