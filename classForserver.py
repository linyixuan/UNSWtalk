import sys,os
import re,time
import functools
import fileinput
import shutil

students_dir = "dataset-medium";

def allpost():
    allPostInDir = []
    alluser = os.listdir(students_dir)
    for username in alluser:
        filespath = os.path.join(students_dir,username)
        files = os.listdir(filespath)
        reg = '[-\d]+.txt'
        posts = getPostList(reg,username,files)
        allPostInDir.extend(list(posts))
    return allPostInDir

def sortFile(x,y):
    tx = tuple([int(i) for i in re.split('\D+',x) if i])
    ty = tuple([int(i) for i in re.split('\D+',y) if i])
    if len(tx) < len(ty):
        return -1
    if len(tx) > len(ty):
        return 1
    if tx > ty:
        return -1
    if tx < ty:
        return 1
    return 0
def readDir(dirName):
    dirPath = os.path.join(students_dir,dirName)
    if os.path.exists(dirPath):
        postFiles = os.listdir(dirPath)
        postFiles.sort(key=functools.cmp_to_key(sortFile))
        #print(postFiles)
    return postFiles
def accountEnityty(username):
    a = account()
    a.username  = username
    if not a.isActive():
        return a
    filepath = os.path.join(students_dir, username, "student.txt")
    if not os.path.exists(filepath):
        return a
    with open(filepath) as file:
        for line in file:
            if line:
                line = line.strip()
                data = line.split(": ")
                if data[0] == "birthday":
                    a.birthday = data[1]
                elif data[0] == "courses":
                    a.course = re.sub('\(|\)', '', data[1]) if len(data) == 2 else a.course
                elif data[0] == "email":
                    a.email = data[1]
                elif data[0] == "home_suburb":
                    a.home_suburb = data [1]
                elif data[0] == "home_longitude":
                    a.home_longitude = data[1]
                elif data[0] == "home_latitude":
                    a.home_latitude = data[1]
                elif data[0] == "full_name":
                    a.full_name = data[1]
                elif data[0] == "friends":
                    a.friends = re.sub('\(|\)', '', data[1]) if len(data) == 2 else a.friends
                elif data[0] == "password":
                    a.password = data[1]
                elif data[0] == "program":
                    a.program = data[1]
                elif data[0] == "profile":
                    profile = data[1]
                    a.profile=profile.split('\\n')
                elif data[0] == "gender":
                    a.gender = data[1]
                elif data[0] == "notified":
                    if "rue" in data[1]:
                        a.notified = True
                    else:
                        a.notified = False
                elif "notification" in data[0]:
                    a.notification = re.sub('\(|\)','',data[1]) if len(data)==2 else a.notification
    if a.course:
        a.courseList = a.course.split(", ") if a.course else []
    if a.friends:
        fl = a.friends.split(", ") if a.friends else []
        f = [re.sub('\D', '', i) for i in fl if i]
        a.friendsList = ['z' + i for i in f if i]
    if a.notification:
        a.notificationList = a.notification.split(", ") if a.notification else []

    imgpath = os.path.join(students_dir, username, "img.jpg")
    if os.path.exists(imgpath):
        a.headimage = imgpath
    return a

def postEntity(username,filename):
    p = post()
    filepath = os.path.join(students_dir, username, filename)
    if not os.path.exists(filepath):
        return p
    with open(filepath,encoding="utf-8") as file:
        for line in file:
            if line:
                line = line.strip()
                data = line.split(": ")
                if data[0] == "message":
                    q = data[1].split("\\n")
                    p.message =list(q)
                elif data[0] == "from":
                    p.poster = accountEnityty(data[1])
                elif data[0] == "time":
                    p.time = data [1]
                elif data[0] == "longitude":
                    p.longitude = data[1]
                elif data[0] == "latitude":
                    p.latitude = data[1]
                elif data[0] == "picture":
                    p.picture = data[1]
                elif data[0] == "nlike":
                    p.nlike = int(re.sub('\D','',data[1]))
                elif data[0] == "nunlike":
                    p.nunlike = int(re.sub('\D','',data[1]))


    p.filename = filename
    p.filepath = filepath
    p.username = username

    return p
def getPostList(reg,username,files):
    posts = []
    for filename in files:
        if re.match(reg, filename):
            postentity = postEntity(username, filename)
            posts.append(postentity)
    return posts

def editStudentFile(student):
    filepath = os.path.join(students_dir, student.username, "student.txt")
    if os.path.exists(filepath):
        output = open(filepath, 'w')
        line = "zid: " + student.username + "\n"
        output.write(line)
        line = "password: " + student.password + "\n"
        output.write(line)
        line = "email: " + student.email + "\n"
        output.write(line)
        line = "gender: " + student.gender + "\n"
        output.write(line)
        line = "full_name: " + student.full_name + "\n"
        output.write(line)
        line = "birthday: " + student.birthday + "\n"
        output.write(line)
        line = "profile: " + "\n".join(student.profile) + "\n"
        output.write(line)
        line = "program: " + student.program + "\n"
        output.write(line)
        line = "courses: " + "(" + student.course + ")" + "\n"
        output.write(line)
        line = "friends: " + "(" + student.friends + ")" + "\n"
        output.write(line)
        line = "home_suburb: " + student.home_suburb + "\n"
        output.write(line)
        line = "home_longitude: " + student.home_longitude + "\n"
        output.write(line)
        line = "home_latitude: " + student.home_latitude + "\n"
        output.write(line)
        line = "notified: " + str(student.notified) + "\n"
        output.write(line)
        line = "notification: (" + student.notification +")"+ "\n"
        output.write(line)
        output.close()
        return True
    return False

def editPostFile(apost):
    apost = post()
    filepath = os.path.join(students_dir, apost.username, apost.filename)
    if not os.path.exists(filepath):
        return False
    output = open(filepath, 'w')
    line = "from: " + apost.poster.username + "\n"
    output.write(line)
    line = "message: " + apost.message + "\n"
    output.write(line)
    line = "longitude: " + apost.longitude+"\n"
    output.write(line)
    line = "latitude: " + apost.latitude +"\n"
    output.write(line)
    line = "time: " + apost.time + "\n"
    output.write(line)
    line = "nlike: " + apost.nlike+"\n"
    output.write(line)
    line = "nunlike: " + apost.nunlike+"\n"
    output.write(line)
    line = "picture: " + apost.picture + "\n"
    output.write(line)
    output.close()


class post:
    def __init__(self):
        self.time = ""
        self.message = ""
        self.poster = account()
        self.picture = ""
        self.latitude = ""
        self.longitude = ""
        self.comments = []
        self.filename = ""
        self.filepath = ""
        self.username = ""
        self.nlike = 0
        self.nunlike = 0

    def newPost(self,time,message,poster):
        self.time = time
        self.message = message
        self.poster = poster
    def readCommentsFromDir(self):
        comments = []
        files = readDir(self.username)
        fn = self.filename.split(".")
        reg = fn[0]+"-\d*"+"\."+fn[1]
        comments = getPostList(reg, self.username, files)
        return comments

    def makeComment(self,mfilename,content,commenter):
        dirpath = os.path.join(students_dir,self.username)
        if not os.path.isdir(dirpath):
            return False
        if mfilename:
            fn = re.search(r'(\d+)\.txt',mfilename).group(1)
            newn = int(fn)+1
            newfilname = re.sub('\d+.txt',str(newn)+".txt",mfilename)
        else:
            newfilname = re.sub('.txt',"-0.txt",self.filename)
        filepath = os.path.join(students_dir, self.username, newfilname)
        output = open(filepath, 'w')
        line = "from: " + commenter + "\n"
        output.write(line)
        line = "message: " +content + "\n"
        output.write(line)
        line = "longitude: " + "\n"
        output.write(line)
        line = "latitude: "  + "\n"
        output.write(line)
        t = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        line = "time: " + t+"\n"
        output.write(line)
        line = "nlike: 0" + "\n"
        output.write(line)
        line = "nunlike: 0" + "\n"
        output.write(line)
        output.close()

class account:
    def __init__(self):
        self.username = ""
        self.password= ""
        self.email = ""
        self.gender ="unknow"
        self.headimage = ""
        self.birthday = ""
        self.course = ""
        self.home_suburb = ""
        self.full_name = ""
        self.home_longitude = ""
        self.home_latitude = ""
        self.friends = ""
        self.program = ""
        self.courseList = []
        self.friendsList = []
        self.profile = ""
        self.active = False
        self.notified = False
        self.notification =""
        self.notificationList = []
    def newAccount(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
    def getFriendList(self):
        list = []
        for username in self.friendsList:
            user = account()
            user = accountEnityty(username)
            list.append(user)
        return list

    def readSelfPostsFromDir(self):
        posts = []
        files = readDir(self.username)
        posts = getPostList('\d+.txt',self.username,files)
        return posts
    def readAllPostFromDir(self):
        posts = []
        allPosts = []
        usernames = [self.username] + self.friendsList
        for username in usernames:
            dirPath = os.path.join(students_dir, username)
            if os.path.exists(dirPath):
                files = os.listdir(dirPath)
                posts = getPostList("\d+.txt",username,files)
                allPosts +=list(posts)
        allPosts.sort(key=lambda x:x.time,reverse = True)
        return allPosts
    def isExists(self):
        dirPath = os.path.join(students_dir, self.username)
        if self.username:
            if os.path.exists(dirPath):
                return True
            else:
                return False
        else:
            return False

    def isActive(self):
        filepath = os.path.join(students_dir, self.username, "student.txt")
        if os.path.exists(filepath):
            self.active = True
            return True
        else:
            self.active = False
            return False
    def register(self):
        dirpath = os.path.join(students_dir, self.username)
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        filepath = os.path.join(students_dir, self.username, "temp_student.txt")
        output = open(filepath,'w')
        line = "zid: "+self.username +"\n"
        output.write(line)
        line = "password: " +self.password +"\n"
        output.write(line)
        line = "email: " + self.email + "\n"
        output.write(line)
        line = "full_name: " + self.full_name + "\n"
        output.write(line)
        output.close()

    def activate(self):
        filepath = os.path.join(students_dir, self.username, "temp_student.txt")
        newpath = os.path.join(students_dir, self.username, "student.txt")
        if os.path.exists(filepath):
            os.rename(filepath,newpath)
            self.active = True
            return True
        return False
    def recover(self):
        dirpath = os.path.join(students_dir, self.username)
        if not os.path.isdir(dirpath):
            return False
        filepath = os.path.join(students_dir, self.username, "recover.password")
        output = open(filepath, 'w')
        line = self.password
        output.write(line)
        output.close()
        return True
    def confirmChangePassword(self):
        cfilepath = os.path.join(students_dir, self.username, "recover.password")
        recover = ""
        if os.path.exists(cfilepath):
            file = open(cfilepath,'r')
            recover = file.readline()
            file.close()
        else:
            return False
        filepath = os.path.join(students_dir, self.username, "student.txt")
        if os.path.exists(filepath):
            output = open(filepath, 'w')
            line = "zid: " + self.username + "\n"
            output.write(line)
            line = "password: " + recover+ "\n"
            output.write(line)
            line = "email: " + self.email + "\n"
            output.write(line)
            line = "gender: " + self.gender + "\n"
            output.write(line)
            line = "full_name: " + self.full_name + "\n"
            output.write(line)
            line = "birthday: " + self.birthday + "\n"
            output.write(line)
            line = "profile: " + self.profile + "\n"
            output.write(line)
            line = "program: " + self.program + "\n"
            output.write(line)
            line = "courses: " + "("+self.course + ")"+ "\n"
            output.write(line)
            line = "friends: " + "("+self.friends +")"+ "\n"
            output.write(line)
            line = "home_suburb: " + self.home_suburb + "\n"
            output.write(line)
            line = "home_longitude: " + self.home_longitude + "\n"
            output.write(line)
            line = "home_latitude: " + self.home_latitude + "\n"
            output.write(line)
            line = "notified: " + self.notified + "\n"
            output.write(line)
            line = "notification: " + self.notification + "\n"
            output.write(line)
            output.close()
            os.remove(cfilepath)
            return True
        return False

    def searchFriend(self,susername,sname):
        allusers = os.listdir(students_dir)
        results = []
        recommend = []
        rmax = 0
        reg1 = ".*" + susername + ".*" if susername else ".*"
        reg2 = ".*" + sname + ".*" if sname else ".*"
        for user in allusers:
            if re.match(reg1,user) and user !=self.username:
                u = account()
                u = accountEnityty(user)
                if user not in self.friendsList :
                    c = retB = list(set(self.friendsList).intersection(set(u.friendsList)))
                    if len(c) > rmax:
                        rmax = len(c)
                        recommend.clear()
                        recommend.append(u)
                    elif len(c) == rmax:
                        recommend.append(u)
                if re.match(reg2,u.full_name):
                    results.append(u)
        return results,recommend,rmax
    def deleteAccount(self):
        path = os.path.join(students_dir,self.username)
        if os.path.exists(path):
            shutil.rmtree(path)

    def makePost(self,mfilename,content):
        dirpath = os.path.join(students_dir,self.username)
        if not os.path.isdir(dirpath):
            return False
        if mfilename:
            fn = re.search(r'(\d+)\.txt',mfilename).group(1)
            newn = int(fn)+1
            newfilname = str(newn)+".txt"
        else:
            newfilname = "0.txt"
        filepath = os.path.join(students_dir, self.username, newfilname)
        output = open(filepath, 'w')
        line = "from: " + self.username + "\n"
        output.write(line)
        line = "message: " +content + "\n"
        output.write(line)
        line = "longitude: " + "\n"
        output.write(line)
        line = "latitude: "  + "\n"
        output.write(line)
        t = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        line = "time: " + t+"\n"
        output.write(line)
        output.close()






















