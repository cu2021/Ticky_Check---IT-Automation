import sys
import re
import operator
import csv

users = {}

errors = {}

with open('syslog.log') as file:
    # read each line
    for line in file.readlines():
        match = re.search(
            r"ticky: ([\w+]*):? ([\w' ]*)[\[[#0-9]*\]?]? ?\((.*)\)$", line)
        keyword, msg, user = match.group(1), match.group(2), match.group(3)
        if keyword == "ERROR":
            if msg not in errors.keys():
                errors[msg] = 1
            else:
                errors[msg] += 1


        if user not in users.keys():
            users[user] = {}
            users[user]['INFO'] = 0
            users[user]['ERROR'] = 0
        if keyword == 'INFO':
            if user not in users.keys():
                users[user] = {}
                users[user]['INFO'] = 0
            else:
                users[user]["INFO"] += 1
        elif keyword == 'ERROR':
            if user not in users.keys():
                users[user] = {}
                users[user]['INFO'] = 0
            else:
                users[user]['ERROR'] += 1

errors_list = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)

per_user_list = sorted(users.items(), key=operator.itemgetter(0))

file.close()
with open('user_statistics.csv', 'w', encoding='UTF8', newline='') as user_csv:
    user_csv.write('Username,INFO,ERROR\n')
    for user, value in per_user_list:
        user_csv.write(str(user) + ',' +
                       str(value['INFO']) + ',' + str(value['ERROR']) + '\n')
user_csv.close()

with open('error_message.csv', 'w', encoding='UTF8', newline='') as error_csv:
    error_csv.write('Error,Count\n')

    for key, value in errors_list:
        error_csv.write(str(key) + ',' + str(value)+"\n")
error_csv.close()
