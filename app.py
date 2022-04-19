import http.client
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import base64
from flask_mail import Mail, Message
from datetime import date
import json
import os.path
import os

app = Flask(__name__)
app.secret_key = "Secret Key"
wsgi_app = app.wsgi_app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "maharagamanie8@gmail.com"
app.config['MAIL_PASSWORD'] = "DG@nie123"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# SqlAlchemy Database Configuration With Mysql
DATA = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root',
                                                                             password='calendar@nie',
                                                                             server='localhost',
                                                                             database='calendar')

app.config['SQLALCHEMY_DATABASE_URI'] = DATA
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class MeetingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingName = db.Column(db.String(200))
    date = db.Column(db.String(300))
    place = db.Column(db.String(200))
    time = db.Column(db.String(300))
    endtime = db.Column(db.String(300))
    description = db.Column(db.TEXT)
    userName = db.Column(db.String(300))

    def __init__(self, meetingName, date, place, time, endtime, description, userName):
        self.meetingName = meetingName
        self.date = date
        self.place = place
        self.time = time
        self.endtime = endtime
        self.description = description
        self.userName = userName


class PendingMeetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingName = db.Column(db.String(200))
    date = db.Column(db.String(300))
    place = db.Column(db.String(200))
    time = db.Column(db.String(300))
    endtime = db.Column(db.String(300))
    description = db.Column(db.TEXT)
    requester = db.Column(db.String(200))
    userName = db.Column(db.String(200))

    def __init__(self, meetingName, date, place, time, endtime, description, requester, userName):
        self.meetingName = meetingName
        self.date = date
        self.place = place
        self.time = time
        self.endtime = endtime
        self.description = description
        self.requester = requester
        self.userName = userName


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(200))
    email = db.Column(db.String(300))
    password = db.Column(db.String(300))
    userToken = db.Column(db.String(300))

    def __init__(self, userName, email, password, userToken):
        self.userName = userName
        self.email = email
        self.password = password
        self.userToken = userToken


class MeetingListSchema(ma.Schema):
    class Meta:
        fields = ("id", "meetingName", "date", "place", "time", "endtime", "description", "userName")


todaymeeting = MeetingListSchema()
todaymeeting = MeetingListSchema(many=True)


class PendingMeetingSchema(ma.Schema):
    class Meta:
        fields = ("id", "meetingName", "date", "place", "time", "endtime", "description", "requester", "userName")


pendMeeting = PendingMeetingSchema()
pendMeeting = PendingMeetingSchema(many=True)


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/userregister')
def userregister():
    return render_template("userregister.html")


@app.route('/userregister/register', methods=['POST'])
def saveuser():
    if request.method == 'POST':
        registerName = request.form['name']
        registerEmail = request.form['email']
        registerPassword = request.form['password']

        userToken = base64.b64encode(registerName.encode("utf-8"))
        decode = base64.b64decode(userToken).decode("utf-8")
        print(decode)
        userdetails = User(registerName, registerEmail, registerPassword, userToken)
        db.session.add(userdetails)
        db.session.commit()
        return render_template("userregister.html")


@app.route('/home/<accessToken>')
def Index(accessToken):
    print(accessToken)
    if accessToken == "cm9vdA==":
        return render_template("index.html", accessToken=accessToken)
    if accessToken == "YWRtaW4=":
        return render_template("admin.html", accessToken=accessToken)
    checkToken = User.query.filter_by(userToken=accessToken)
    usertoken = ""
    for b in checkToken:
        usertoken = b.userToken
    if usertoken == "":
        return redirect(url_for('login'))
    else:
        return render_template("test.html", accessToken=accessToken)


# @app.route('/checklogin', methods=['POST'])
# def checklogin():
#     if request.method == 'POST':
#         userID = request.form['email']
#         userPass = request.form['password']
#         if userID == "root" and userPass == "root@123":
#             accessToken = "rootmember"
#             return redirect(url_for('Index', accessToken=accessToken))
#         elif userID == "user" and userPass == "user@nie":
#             accessToken = "usermember"
#             return redirect(url_for('Index', accessToken=accessToken))
#         else:
#             return redirect(url_for('login'))


@app.route('/checklogin', methods=['POST'])
def checklogin():
    if request.method == 'POST':
        useremail = request.form['email']
        userPass = request.form['password']
        # print(useremail, userPass)
        userDetails = User.query.filter_by(email=useremail, password=userPass)
        accessToken = ""
        for a in userDetails:
            # print(a.userName)
            # print(a.email)
            accessToken = a.userToken
        # print(accessToken)
        if accessToken == "":
            return redirect(url_for('login'))
        else:
            return redirect(url_for('Index', accessToken=accessToken))


@app.route('/delete/<accessToken>', methods=['GET', 'POST'])
def delete(accessToken):
    did = request.args.get('id')
    deletedata = MeetingList.query.get(did)
    db.session.delete(deletedata)
    db.session.commit()
    return redirect(url_for('Index', accessToken=accessToken))


@app.route('/addMeeting/<accessToken>', methods=['POST'])
def addMeeting(accessToken):
    if request.method == 'POST':
        meetingName = request.form['meetingName']
        meetingDate = request.form['date']
        place = request.form['place']
        meetingTime = request.form['Time']
        endtime = request.form['endtime']
        description = request.form['Description']
        useName = base64.b64decode(accessToken).decode("utf-8")

        meetingData = MeetingList(meetingName, meetingDate, place, meetingTime, endtime, description, useName)
        db.session.add(meetingData)
        db.session.commit()

        return redirect(url_for('Index', accessToken=accessToken))


@app.route('/reqwestMeeting/<accessToken>', methods=['POST'])
def reqwestMeeting(accessToken):
    if request.method == 'POST':
        print(accessToken)
        meetingName = request.form['meetingName']
        meetingDate = request.form['date']
        place = request.form['place']
        meetingTime = request.form['Time']
        endtime = request.form['endtime']
        description = request.form['Description']
        requester = accessToken
        useName = base64.b64decode(requester).decode("utf-8")

        requestMeeting = PendingMeetings(meetingName, meetingDate, place, meetingTime, endtime, description, requester,
                                         useName)
        db.session.add(requestMeeting)
        db.session.commit()
        return redirect(url_for('Index', accessToken=accessToken))


@app.route('/showMeeting', methods=['GET'])
def showMeeting():
    date = request.args.get('dates')
    todayMeeting = MeetingList.query.filter_by(date=date).order_by(MeetingList.time.asc()).all()
    # ordered_query = todayMeeting.order_by(MeetingList.time.asc)
    # # newtodaymeeting = MeetingList.query.order_by(MeetingList.time()).filter_by(date=date)
    output = todaymeeting.dump(todayMeeting)
    return jsonify({'meetings': output})


@app.route('/tblAllMeetings', methods=['GET'])
def tblAllMeetings():
    monthNum = request.args.get('monthNum')
    calendarCurrentDate = date.today()
    if monthNum == '600':
        startMonth = calendarCurrentDate
        endMonth = 'yyyy-mm-31'
        endMonth = endMonth.replace("yyyy", str(calendarCurrentDate.year))
        if calendarCurrentDate.month < 10:
            changeMonth = "0" + str(calendarCurrentDate.month)
            endMonth = endMonth.replace("mm", str(changeMonth))
        else:
            endMonth = endMonth.replace("mm", str(calendarCurrentDate.month))

        qry = MeetingList.query.filter(MeetingList.date.between(str(startMonth), endMonth)).order_by(
            MeetingList.date.asc(), MeetingList.time.asc()).all()
        chkout = todaymeeting.dump(qry)
        return jsonify({'meetings': chkout})

    else:
        startMonth = 'yyyy-mm-01'
        endMonth = 'yyyy-mm-31'
        startMonth = startMonth.replace("yyyy", str(calendarCurrentDate.year))
        endMonth = endMonth.replace("yyyy", str(calendarCurrentDate.year))
        startMonth = startMonth.replace("mm", str(monthNum))
        endMonth = endMonth.replace("mm", str(monthNum))
        qry = MeetingList.query.filter(MeetingList.date.between(startMonth, endMonth)).order_by(
            MeetingList.date.asc()).all()
        # print(startMonth, endMonth)
        chkout = todaymeeting.dump(qry)
        return jsonify({'meetings': chkout})


@app.route('/allDetails', methods=['GET'])
def allDetails():
    id = request.args.get('id')
    allDetails = MeetingList.query.filter_by(id=id)
    output = todaymeeting.dump(allDetails)
    return jsonify({'meetings': output})


# details for suggesting
@app.route('/detailsSuggesting', methods=['GET'])
def detailsSuggesting():
    id = request.args.get('id')
    detailsSuggesting = PendingMeetings.query.filter_by(id=id)
    output = pendMeeting.dump(detailsSuggesting)
    return jsonify({'meetings': output})


@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))


@app.route('/update/<accessToken>', methods=['POST'])
def updateMeeting(accessToken):
    if request.method == 'POST':
        id = request.form['updteid']
        updateData = MeetingList.query.get(id)
        updateData.meetingName = request.form['meetingName']
        updateData.date = request.form['date']
        updateData.place = request.form['place']
        updateData.time = request.form['Time']
        updateData.endtime = request.form['endtime']
        updateData.description = request.form['Description']

        db.session.commit()
        return redirect(url_for('Index', accessToken=accessToken))


@app.route('/showPendingMeeting/<accessToken>', methods=['GET'])
def showPendingMeeting(accessToken):
    pendingMeeting = PendingMeetings.query.filter_by(requester=accessToken).order_by(PendingMeetings.time.asc()).all()
    output = pendMeeting.dump(pendingMeeting)
    return jsonify({'meetings': output})


@app.route('/pendingdelete/<accessToken>', methods=['GET', 'POST'])
def pendingdelete(accessToken):
    did = request.args.get('id')
    deletedata = PendingMeetings.query.get(did)
    db.session.delete(deletedata)
    db.session.commit()
    return redirect(url_for('Index', accessToken=accessToken))


@app.route('/allPendingMeeting', methods=['GET'])
def allPendingMeeting():
    allpendingMeeting = PendingMeetings.query.order_by(PendingMeetings.time.asc()).all()
    output = pendMeeting.dump(allpendingMeeting)
    return jsonify({'meetings': output})


@app.route('/approveRequest/<accessToken>', methods=['GET'])
def approveRequest(accessToken):
    mid = request.args.get('id')
    meetingName = ""
    date = ""
    place = ""
    time = ""
    endtime = ""
    description = ""
    userName = ""
    approveQuery = PendingMeetings.query.filter_by(id=mid).all()
    for i in approveQuery:
        meetingName = i.meetingName
        date = i.date
        place = i.place
        time = i.time
        endtime = i.endtime
        description = i.description
        userName = i.userName
    if meetingName != "":
        insertQuery = MeetingList(meetingName, date, place, time, endtime, description, userName)
        db.session.add(insertQuery)
        db.session.commit()

        rows = User.query.with_entities(User.email).filter_by(userName=userName).all()
        usr_email = rows[0][0]
        # print(usr_email)

        usr_email = usr_email
        subject = "Accepting your Meeting Request"
        msg = "Dear " + userName + ",\n\n" "Your Meeting Request has been Approved. \n \nMeeting Name: " + meetingName + "\n" + "Date :" + date + "\n" "Start Time :" + time + "\nPlace :" + place + "\n\nThank You...."

        message = Message(subject, sender="maharagamanie8@gmail.com", recipients=[usr_email])
        message.body = msg
        mail.send(message)

        deleteQuery = PendingMeetings.query.get(mid)
        db.session.delete(deleteQuery)
        db.session.commit()
        return jsonify({'result': "sucess"})


@app.route('/deleteRequest/<accessToken>', methods=['POST'])
def deleteRequest(accessToken):
    mid = request.form['id']
    # print(mid)

    smeetingName = request.form['mname']
    sdate = request.form['mdate']
    stime = request.form['mtime']
    sdescription = request.form['description']
    userName = ""
    approveQuery = PendingMeetings.query.filter_by(id=mid).all()
    for i in approveQuery:
        meetingName = i.meetingName
        date = i.date
        place = i.place
        time = i.time
        endtime = i.endtime
        description = i.description
        userName = i.userName

        rows = User.query.with_entities(User.email).filter_by(userName=userName).all()
        usr_email = rows[0][0]

        usr_email = usr_email
        subject = "Requesting to Make  An Other Time Period  for the Meeting"
        msg = "Dear " + userName + ",\n\n" "The meeting you requested cannot be held within that time period. I kindly request you to make an other time period for that meeting.\n \n Suggestion, \nMeeting Name: " + smeetingName + "\n Date :" + sdate + "\n Place :" + place + "\n Start Time :" + stime + "\n Description :" + sdescription + "\n\n Thank You."

        message = Message(subject, sender="maharagamanie8@gmail.com", recipients=[usr_email])
        message.body = msg
        mail.send(message)

    deletedata = PendingMeetings.query.get(mid)
    db.session.delete(deletedata)
    db.session.commit()
    return redirect(url_for('Index', accessToken=accessToken))


@app.route('/test', methods=['POST'])
def test():
    clicked = request.form['name']
    print(clicked)
    return clicked


if __name__ == "__main__":
    app.run(debug=True)
