import os
import paramiko
import stat
class Amdr:
    def __init__(self,ip,user,mdp,port):
        self.ssh = paramiko.SSHClient() 
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, username=user, password=mdp, port=port)
        print("connected")
        self.sftp = self.ssh.open_sftp()

    def upper(self,path,doss):
        dir = os.listdir(path)
        path2 = path
        try:
            self.ssh.exec_command('mkdir /root/drive/'+doss)
        except FileExistsError:
            pass 
        path2 = "/root/drive/" + doss + "/"
        print("launch")
        for x in dir:
            path3 = path + "\\" + x 
            print(path3)
            if os.path.isfile(path3):
                local = path3
                remo = path2 + x 
                self.sftp.put(local,remo)    
            if os.path.isdir(path3):
                do = 0
                self.upfiler(path2,x,doss,do,path3)
                path3 = path
                path2 = "/root/drive/" + doss + "/"
            else:
                local = path3
                remo = path + x 
                self.sftp.put(local,remo)
                
    def upfiler(self,path,x,doss,do,di):
        if do != 0:
            print(di)
            print(x)
            x = x + "\\" + do
            o=do.replace(" ", "\ ")
            print(path + o)
            path2 = path.replace(" ", "\ ") 
            self.ssh.exec_command('mkdir '+ path2 + o)
            path = path + do + "/"
        else:
            o=x.replace(" ", "\ ")
            print(os.path.abspath(x) + " mdr")
            self.ssh.exec_command('mkdir '+ path + o)
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
                self.sftp.put(local,remo)
            elif os.path.isdir(x + "\\" + y):
                self.upfiler(path,x,doss,y,di)
    def downer(self,pa,doss):
        pat = pa
        print (pat,doss)
        try:
            os.mkdir(pat +r'\\' + doss)
            pat = pat + '\\' + doss + "\\"
        except FileExistsError:
            a = 1
            pat = pat +'\\' + doss +"\\"
        remo = "/root/drive/" + doss + "/"
        dir = self.sftp.listdir(remo)
        for x in dir:
            print(x)
            if stat.S_ISREG(self.sftp.stat(os.path.join(remo, x)).st_mode):
                try:
                    local = pat +  x
                    rem = remo + x
                    print(local,rem)
                    self.sftp.get(rem,local)
                except:
                    pass
            if stat.S_ISDIR(self.sftp.stat(os.path.join(remo, x)).st_mode):
                try:
                    do = 0
                    pa = pat
                    self.downfile(pa,remo,x,doss,do)
                    remo = "/root/drive/" + doss + "/"
                except:
                    pass
    def downfile(self,path,remo,x,doss,do):
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
        dir = self.sftp.listdir(remo)
        for x in dir:   
            if stat.S_ISREG(self.sftp.stat(os.path.join(remo, x)).st_mode):
                local = path + x
                rem = remo + x
                print(local,rem)
                self.sftp.get(rem,local)
            if stat.S_ISDIR(self.sftp.stat(os.path.join(remo, x)).st_mode):
                self.downfile(path,remo,x,doss,do)
