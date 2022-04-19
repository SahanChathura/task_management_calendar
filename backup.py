import smtplib
import mysql.connector
import datetime
# from datetime import datetime
from twilio.rest import Client

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="calendar@nie",
    database="calendar"
)

mycursor = mydb.cursor(buffered=True)

# yesterday = datetime.today() + datetime.timedelta(days=1)
# print(yesterday)
today = datetime.date.today()
yesterday = today + datetime.timedelta(days=1)
# date = datetime.today().strftime('%Y-%m-%d')
date = yesterday.strftime('%Y-%m-%d')
# date = "2021-07-07"
print(date)
mycursor.execute("SELECT * FROM meeting_list WHERE date=%s ORDER BY time ASC", (date,))
body = ""
bodytitle = ""
bodydate = ""
bodyplace = ""
bodytime = ""
bodyendtime = ""
bodydescription = ""
for a in mycursor:
    bodytitle = "Title : " + a[1]
    bodydate = "Date :" + a[2]
    bodyplace = "Palce :" + a[3]
    bodytime = "Strat Time :" + a[4]
    bodyendtime = "End Time :" + a[5]
    bodydescription = "Description :" + a[6]

    print(bodydate, bodytitle)
    chk = bodytitle + "\n" + bodydate + "\n" + bodyplace + "\n" + bodytime + "\n" + bodyendtime + "\n" + bodydescription + "\n ------------------------------------------------------------------------- \n"
    body = body + "\n" + chk

# send whatapp msg
# account_sid = 'AC124ddf4971a179a0c4e50d5c4a688d3f'
# auth_token = 'dda019f4401cc9a7cff933d0c798bc55'
# client = Client(account_sid, auth_token)
# whatsappmsg = body
# message = client.messages.create(
#     from_='whatsapp:+14155238886',
#     body=whatsappmsg,
#     to='whatsapp:+94713730870'
# )

# sent email
receiver = "dg@nie.edu.lk"
sender = "admin@nie.ac.lk"
pw = "QWERqwer@#2021"
subject = "Meetings Schedule for " +date
message = MIMEMultipart()
message['From'] = sender
message['To'] = receiver
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))
text = message.as_string()

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login(sender, pw)
mail.sendmail(sender, receiver, text)
mail.close()
print("Email Send")
