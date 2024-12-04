#!/usr/bin/env python3


# import required packages
import csv
import random
from datetime import datetime, timedelta

# example time and format for datetime translation
example_time = "2022.04.02 14:24:41 EDT"
time_format = '%Y.%m.%d %H:%M:%S EDT'

# read the csv log file as a list
with open('challenge-log.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    # cut off the heading "Username, Login Time, ...", so we ignore
    # the row 0
    rows = list(reader)[1:]


# a dictionary that stores previous login time
login_dict = {}

for row in rows:
    # get the username, login_date, and duration
    username = row[0]
    login_date = datetime.strptime(row[1], time_format)
    duration = timedelta(seconds=int(row[2]))

    # check data
    #print(repr(username))
    #print(repr(login_date))
    #print(repr(duration))

    # if this is a first occurance,
    if not username in login_dict:
        # put the login info (date, duration) to the dictionary
        login_dict[username] = (login_date, duration)
    else:
        # if we have already observed the user has been logged in before,
        # get the time
        prev_time = login_dict[username]
        prev_end = prev_time[0] + prev_time[1]
        # check if the new login has happened before the last login's logout
        if prev_end > login_date:
            # print username
            print(username)

        # update the time with the last login time
        login_dict[username] = (login_date, duration)
