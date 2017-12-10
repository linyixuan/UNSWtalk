#!/web/cs2041/bin/python3.6.3

# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk/

import os,re,time
from threading import Thread
import subprocess
from flask import Flask, render_template, session , url_for,request,send_from_directory,redirect
from flask_mail import  Message, Mail

from classForserver import *

students_dir = "dataset-medium"
loginPage = "login.html"
postWallPage = "postWall.html"
registerPage = "loginRegister.html"
forgetPasswordPage = "loginForgetPassword.html"
postOnePage = "postOne.html"
searchFriendsPage = "searchFriends.html"
searchPostPage = "searchPost.html"
settingPage = "setting.html"
profilePage = "profile.html"
friendListPage = "friendList.html"
infoPage = "waitActivate.html"
changePasswordPage = "changepassword.html"
notificaionPage = "notification.html"

UPLOAD_FOLDER='/static/upload/'
ALLOWED_EXTENSIONS=set(['jpg'])

app = Flask(__name__,static_folder='', static_url_path='')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "unswtalkserver@gmail.com"
app.config['MAIL_PASSWORD'] = "unswtalkserver01"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
mail = Mail(app)
app.add_url_rule('/dataset-medium/<path:filename>',endpoint='dataset-medium',build_only=True)

@app.route('/', methods=['GET','POST'])
def start():
    return render_template(loginPage)

@app.route('/loginPage', methods=['GET','POST'])
def getloginPage():
    return render_template(loginPage)

@app.route('/changePasswordPage', methods=['GET','POST'])
def getChangePasswordPage():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    return render_template(changePasswordPage,currentuser= user)

@app.route('/forgetPasswordPage', methods=['GET'])
def getForgetPasswordPage():
    return render_template(forgetPasswordPage)

@app.route('/registerPage', methods=['GET'])
def getregisterPage():
    return render_template(registerPage)
@app.route('/searchPostPage', methods=['GET','POST'])
def getsearchPostPage():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    return render_template(searchPostPage,info="",currentuser = user,rec = "",results="",rinfo="",plen = 0)

@app.route('/searchFriendsPage', methods=['GET','POST'])
def getsearchFriendsPage():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    return render_template(searchFriendsPage,info="",currentuser = user,rec = "",results="",rinfo="",plen = 0)

@app.route('/settingPage', methods=['GET','POST'])
def getsettingPage():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
       return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    return render_template(settingPage,info="",currentuser = user,target = user,type="setting")

@app.route('/profilePage', methods=['GET','POST'])
def getprofilePage():
    currentuser = request.args.get('currentuser', '')
    target = request.args.get('target', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    tuser = account()
    tuser = accountEnityty(target)
    if currentuser == target:
        type = "setting"
    else:
        type = "show"
    return render_template(profilePage, currentuser=user, target=tuser, type=type)


@app.route('/notificaionPage', methods=['GET','POST'])
def getnotificaionPage():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    notificaion = user.notificationList
    return render_template(notificaionPage, currentuser=user, target = user,notificaion=notificaion)

@app.route('/editProfile', methods=['GET','POST'])
def editProfile():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    target = account()
    target = accountEnityty(currentuser)
    target.full_name = request.form.get('target.full_name', '')
    target.email = request.form.get('target.email','')
    target.profile = [request.form.get('target.profile','')]
    target.program = request.form.get('target.program','')
    target.course = request.form.get('target.course','')
    target.home_suburb = request.form.get('target.home_suburb','')
    target.home_latitude = request.form.get('target.home_latitude','')
    target.home_longitude = request.form.get('target.home_longitude','')
    target.birthday = request.form.get('target.birthday','')
    target.gender = request.form.get('target.gender','')
    headimage = request.form.get('target.headimage','')
    if headimage:
        target.headimage = headimage
    target.notified = request.form.get('target.notified','')
    editStudentFile(target)
    return render_template(profilePage,currentuser = target,target = target,type = "setting")

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get('username','')
    password = request.form.get('password','')
    session[username] = username
    user = account()
    user.username = username
    if not user.isExists() or not username:
        return render_template(loginPage, error="Unknow username!")
    user = accountEnityty(username)
    if user.password != password:
        return render_template(loginPage, error="Wrong password!",P1 = user.password,p2=password)
    if not user.isActive():
        return render_template(loginPage, error="This account is not active!")

    posts = user.readAllPostFromDir()
    plen= len(posts)
    return render_template(postWallPage,currentuser = user,target = user,posts = posts,plen= plen)

@app.route('/logout', methods=['GET','POST'])
def logout():
    username = request.args.get('currentuser', '')
    if username in session:
        session.pop(username, None)
    return render_template(infoPage, logout = "Success to log out!")

@app.route('/deleteAccount', methods=['GET','POST'])
def deleteAccount():
    currentuser = request.form.get('currentuser', '')
    user = account()
    user = accountEnityty(currentuser)
    user.deleteAccount()
    if currentuser in session:
        session.pop(currentuser, None)
    return render_template(infoPage, logout = "Success to delete this account!")

@app.route('/home', methods=['GET','POST'])
def home():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    posts = user.readAllPostFromDir()
    plen = len(posts)
    return render_template(postWallPage, currentuser=user, target=user, posts=posts,type = "home",plen= plen)

@app.route('/isLike', methods=['GET','POST'])
def isLike():
    pass

@app.route('/newPost', methods=['GET','POST'])
def newPost():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    postType = request.form.get('postType','')
    content = request.form.get('content','')
    tusername = request.form.get('tusername','')
    tfilename = request.form.get('tfilename','')
    pagesource = request.form.get('source','')

    if "newpost" in postType:
        posts = user.readSelfPostsFromDir()
        mfilename = posts[0].filename if len(posts)>0 else ""
        user.makePost(mfilename,content)
        posts = user.readAllPostFromDir()
        plen = len(posts)
        return render_template(postWallPage, currentuser=user, target=user, posts=posts, type="home", plen=plen)
    else:
        tpost = post()
        tpost = postEntity(tusername, tfilename)
        comments = tpost.readCommentsFromDir()
        mfilename = comments[0].filename if len(comments) > 0 else ""
        tpost.makeComment(mfilename,content,currentuser)
        comments = tpost.readCommentsFromDir()
        plen = len(comments)
        if postOnePage in pagesource:
            return render_template(postOnePage, tpost=tpost, currentuser=user, comments=comments, plen=plen)
        else:
            posts = user.readAllPostFromDir()
            plen = len(posts)
            return render_template(postWallPage, currentuser=user, target=user, posts=posts, type="home", plen=plen)
@app.route('/deletePost', methods=['GET','POST'])
def deletePost():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    pfilename = request.form.get('pfilename', '')
    pusername = request.form.get('pusername', '')
    tpost = postEntity(pusername, pfilename)
    comments = tpost.readCommentsFromDir()
    path = os.path.join(students_dir,pusername,pfilename)
    if os.path.exists(path):
        os.remove(path)
    for c in comments:
        if os.path.exists(c.filepath):
            os.remove(c.filepath)
    posts = user.readSelfPostsFromDir()
    plen = len(posts)
    return render_template(postWallPage, currentuser=user, target=user, posts=posts, type="home", plen=plen)

@app.route('/postDetail', methods=['GET','POST'])
def postDetail():
    currentuser = request.form.get('currentuser', '')
    pfilename = request.form.get('pfilename', '')
    pusername = request.form.get('pusername','')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    tpost = post()
    tpost = postEntity(pusername,pfilename)
    comments = tpost.readCommentsFromDir()
    plen=len(comments)
    return render_template(postOnePage,tpost = tpost,currentuser=user,comments =comments,plen=plen)

@app.route('/personDetail', methods=['GET','POST'])
def personDetail():
    currentuser = request.args.get('currentuser', '')
    target = request.args.get('target', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    tuser = account()
    tuser = accountEnityty(target)
    posts = tuser.readSelfPostsFromDir()
    plen = len(posts)
    return render_template(postWallPage, currentuser=user, target=tuser, posts=posts,type = "person",plen=plen)

@app.route('/friendList', methods=['GET','POST'])
def friendList():
    currentuser = request.args.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    list = user.getFriendList()
    plen = len(list)
    return render_template(friendListPage,currentuser = user,friendlist=list,plen=plen)

@app.route('/searchFriends', methods=['GET','POST'])
def searchFriends():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    sname = request.form.get('search_form_name','')
    susername = request.form.get('search_form_username', '')
    user = account()
    user = accountEnityty(currentuser)
    results,recommend,rmax = user.searchFriend(susername,sname)
    rec = [recommend[0]] if rmax == 0and len(recommend)!=0 else list(recommend)
    plen = len(results)
    rinfo = "The user has "+str(rmax) +" common friends with you"
    info = "\""+sname+"\" and \"" +susername+"\""
    return render_template(searchFriendsPage,info=info,currentuser = user,rec = rec,results=results,rinfo=rinfo ,plen = plen)

@app.route('/searchPosts', methods=['GET','POST'])
def searchPosts():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    psting = request.form.get('search_form_post','')
    isall = request.form.get('isall','')
    user = account()
    user = accountEnityty(currentuser)
    if "false" in isall:
        allposts = user.readAllPostFromDir()
    else:
        allposts = allpost()
    results = []
    recommend = []
    rmax = 0
    reg = reg1 = ".*"+psting+".*" if psting else ".*"
    for post in allposts:
        m = str(post.message)
        if re.match(reg,m):
            results.append(post)
        nc = post.readCommentsFromDir()
        if len(nc) >rmax:
            rmax = len(nc)
            recommend.clear()
            recommend.append(post)
        elif len(nc) == rmax:
            recommend.append(post)
    rec = [recommend[0]] if rmax == 0and len(recommend)!=0 else list(recommend)
    plen = len(results)
    rinfo = "The hotest post which has "+str(rmax)+" comments"
    info = "\""+psting+"\""
    if len(rec) >3:
        rec = list(rec[0:3])
    return render_template(searchPostPage,info=info,currentuser = user,rec = rec,results=results,rinfo=rinfo ,plen = plen)

@app.route('/addFriendRequest', methods=['GET','POST'])
def addFriendRequest():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    target = request.form.get('target', '')
    user = account()
    user = accountEnityty(currentuser)
    info = "Sending add friend request to "+target+" !"
    tuser = account()
    tuser = accountEnityty(target)
    n = user.full_name if user.full_name else user.username
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    n = t+" You receive a friend request from "+ n+" ["+user.username+"] ";
    tuser.notification += ", "+n
    editStudentFile(tuser)
    if tuser.email and tuser.notified:
        #mssg = url_for('notificaionPage',currentuser =tuser.username)
        #send_email(user.email,'There is a friend request for you',mssg)
        msg = Message('There is a friend request for you', sender='unswtalkserver@gmail.com',
                      recipients=[user.email])
        msg.html = "<h1>Hi! Please click the link below to view this request.</h>" + \
                   "<h3><a href='http://127.0.0.1:5000/notificaionPage?currentuser=" + tuser.username + "'>View Notification</a></h3>"
        mail.send(msg)

    return render_template(infoPage,info = info)

@app.route('/addFriend', methods=['GET','POST'])
def addFriend():
    currentuser = request.form.get('currentuser', '')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    message = request.form.get('message', '')
    if message:
        s = re.findall(r'\[[z\d]+\]',message)
        fusername = s[0][1:-1]
        if len(s) == 1:
            if fusername in user.friends:
                return render_template(infoPage, fail="User:" + fusername + " is in your friend list!")
            user.friends += ", "+fusername
            fuser = accountEnityty(fusername)
            fuser.friends += ", " + user.username
            n = fuser.full_name if fuser.full_name else fuser.username
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            n = t + " " + n + " become your friend!";
            fuser.notification += ", " + n
            editStudentFile(fuser)
            editStudentFile(user)
    user = accountEnityty(currentuser)
    list = user.getFriendList()
    plen = len(list)
    return render_template(friendListPage,currentuser = user,friendlist=list,plen=plen)

@app.route('/deleteFriend', methods=['GET','POST'])
def deleteFriend():
    currentuser = request.form.get('currentuser', '')
    dusername = request.form.get('dusername','')
    if not currentuser in session:
        return render_template(loginPage, error="Please log in!")
    user = account()
    user = accountEnityty(currentuser)
    tuser = account()
    tuser = accountEnityty(dusername)
    reg = ", "+dusername
    treg = ", "+currentuser
    user.friends = re.sub(reg,'',user.friends)
    tuser.friends =re.sub(treg,'',tuser.friends)
    editStudentFile(tuser)
    editStudentFile(user)
    user = accountEnityty(currentuser)
    list = user.getFriendList()
    plen = len(list)
    return render_template(friendListPage, currentuser=user, friendlist=list, plen=plen)

@app.route('/register', methods=['GET','POST'])
def register():
    firstname = request.form.get('first_name','')
    lastname = request.form.get('last_name','')
    username = request.form.get('username','')
    email = request.form.get('email','')
    password = request.form.get('password','')
    passwordconfir = request.form.get('password_confirmation','')
    user = account()
    user.username = username
    if not checkUsername(username):
        return render_template(registerPage, error = "is invalid, please input your zNumber!")
    if user.isExists():
        return render_template(registerPage, error="existed!")
    if not checkPassword(password,passwordconfir):
        return render_template(registerPage, passwordError="can't match!")
    user.password = password
    user.full_name = firstname + " "+ lastname
    user.email = email
    user.register()
    # mssg = "<h1>Hi! Welcome to UNSWtalk! Please click the link below to activate your account.</h>" + \
    #            "<h3><a href='activate?username=" + user.username + "'>Activate Account</a></h3>"
    # send_email(user.email,'Activate your UNSWtalk account!',mssg)
    msg = Message('Activate your UNSWtalk account!', sender='unswtalkserver@gmail.com',
                  recipients=[user.email])
    msg.html= "<h1>Hi! Welcome to UNSWtalk! Please click the link below to activate your account.</h>" + \
               "<h3><a href='http://127.0.0.1:5000/activate?username="+user.username+"'>Activate Account</a></h3>"
    mail.send(msg)
    return render_template(infoPage,info = "Please check your email and activate this account!")

@app.route('/activate', methods=['GET','POST'])
def activate():
    username = request.args.get('username', '')
    user = account()
    user.username = username
    if user.activate():
        return render_template(infoPage,success = "Activation is success!")
    else:
        return render_template(infoPage, fail="User:"+username+" Oops, activation is fail! Please try it again!")

@app.route('/changePassword', methods=['GET','POST'])
def changePassword():
    username = request.form.get('currentuser', '')
    if not username in session:
        return render_template(loginPage, error="Please log in!")
    password = request.form.get('password', '')
    passwordconfir = request.form.get('password_confirmation', '')
    user = account()
    user.username = username
    user = accountEnityty(username)
    if not checkUsername(username):
        return render_template(changePasswordPage, error="is invalid, please input your zNumber!")
    if not user.isExists():
        return render_template(changePasswordPage, error="not existed!")
    if not checkPassword(password, passwordconfir):
        return render_template(changePasswordPage, passwordError="can't match!")
    user.password = password

    if user.recover():
        user.confirmChangePassword()
        return render_template(profilePage,currentuser = user,target = user,type = "setting")
    else:
        return render_template(infoPage, fail="User:"+username+" Oops, change password is fail! Please try it again!")

@app.route('/recoverPassword', methods=['GET','POST'])
def recoverPassword():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    passwordconfir = request.form.get('password_confirmation', '')
    user = account()
    user.username = username
    user = accountEnityty(username)
    if not checkUsername(username):
        return render_template(forgetPasswordPage, error="is invalid, please input your zNumber!")
    if not user.isExists():
        return render_template(forgetPasswordPage, error="not existed!")
    if not checkPassword(password, passwordconfir):
        return render_template(forgetPasswordPage, passwordError="can't match!")
    user.password = password
    if not user.email:
        return render_template(infoPage,
                               fail="User:" + username + " Sorry, can't change your password because your email is invaild")
    if user.recover():

        msg = Message('Change your UNSWtalk account password!', sender='unswtalkserver@gmail.com',
                      recipients=[user.email])
        msg.html = "<h1> Please click the link below to confirm your change.</h>" + \
                   "<h3><a href='http://127.0.0.1:5000/confirmChange?username=" + user.username + "'>Confirm this password change</a></h3>"
        mail.send(msg)

        # mssg = url_for('confirmChange',username =user.username)
        #
        # send_email(user.email,'Change your UNSWtalk account password!',mssg)
        return render_template(infoPage, info="Please check your email and confirm this change!")
    else:
        return render_template(infoPage, fail="User:"+username+" Oops, recover password is fail! Please try it again!")

@app.route('/confirmChange', methods=['GET','POST'])
def confirmChange():
    username = request.args.get('username', '')
    user = account()
    user.username = username
    if user.confirmChangePassword():
        return render_template(infoPage, success="Change is success!")
    else:
        return render_template(infoPage, fail="User:" + username + " Oops, this change is fail! Please try it again!")

@app.route('/editImage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['headimage']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template(infoPage,info = "update image success")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

def checkUsername(username):
    if re.match('z\d{7}',username):
        return True
    else:
        return False
def checkPassword(password,passwordconfir):
    if password == passwordconfir:
        return True
    else:
        return False
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def send_email(to, subject, message):
    mutt = [
            'mutt',
            '-s',
            subject,
            '-e', 'set copy=no',
            '-e', 'set realname=UNSWtalk',
            '--', to
    ]

    subprocess.run(
            mutt,
            input = message.encode('utf8'),
            stderr = subprocess.PIPE,
            stdout = subprocess.PIPE,
    )



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,port=5000)