import praw
import config
import time
import datetime
import time
import csv
import datetime
import os
import sys


def bot_login():
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Test 1")
    return r


def send_email(latest_comments):

    comments_for_email = ''

    for c in latest_comments:
        comments_for_email += "\n- " + c.body.encode('ascii', errors='ignore').decode('ascii')

    try:
        os.system('python3 emailtest.py ' + '"{}" '.format("Big Brother Alert") + '"{}"'.format(comments_for_email))
        print("Send notification")
    except:
        print("Error sending notification")


def save_to_spreadsheet(latest_comments):
    comments_string = ""

    for comment in latest_comments:
        comments_string = comments_string + ',' + comment.body.replace(",", "")

    csv_title = str(datetime.datetime.now().date())

    time_stamp = datetime.datetime.now().time()

    with open(csv_title + '.csv', 'a') as doc:
        row = str(time_stamp.hour) + ":" + str(time_stamp.minute) + ',' + str(len(latest_comments)) + ',' + comments_string
        row = row.replace('\n', '')
        doc.write(row + '\n')


notifications = False

post_id = sys.argv[1]

if int(sys.argv[2]) == 1:
    notifications = True

delay = int(sys.argv[3])

notification_threshold = int(sys.argv[4])
 
r = bot_login()



old_minute = 0
latest_comments = []

while True:

    try:

        for comment in r.subreddit('bigbrother').stream.comments():

            post_id = list(r.subreddit('BigBrother').hot(limit=1))[0].id

            new_minute = str(datetime.datetime.now().time().minute)

            if new_minute != old_minute:
                print("New minute - " + post_id)
                print("Last minute: " + str(len(latest_comments)))
                save_to_spreadsheet(latest_comments)

                if len(latest_comments) >= 15:
                    send_email(latest_comments)

                latest_comments = []

            if comment.submission.id == post_id:
                print(comment.body)

                latest_comments.append(comment)

            old_minute = new_minute

    except e:
        time.sleep(60)
