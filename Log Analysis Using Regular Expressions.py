#!/usr/bin/env python3

import re
import operator
import csv

error_message = dict()
user_statistics = dict()

f = open("syslog.log")
for line in f:
  line = line.strip()
  line = line.rstrip()
  #print(line)
  match = re.search(r": ERROR ([\w ,']*) ", line)
  match2 = re.search(r"\(([\w ,.]*)\)", line)
  print(line,match2)
  if(match2!=None):
    user = match2.group()[1:]
    user = user[:-1]
    if(user not in user_statistics.keys()):
      user_statistics[user] = [0,0]
    if("ERROR" in line):
      user_statistics[user][1] = user_statistics[user][1] + 1
    if("INFO" in line):
      user_statistics[user][0] = user_statistics[user][0] + 1

  if(match!=None):
    result = match.group()[8:]
    result = result[:-1]
    if(result not in error_message.keys()):
      error_message[result] = 1
    else:
      error_message[result] = error_message[result] + 1
error_message_list = sorted(error_message.items(), key = operator.itemgetter(1), reverse=True)
user_statistics_list = sorted(user_statistics.items(), key = operator.itemgetter(0))
#print(error_message_list)
#print(user_statistics_list)
f.close()

with open('error_message.csv', 'w') as f:
  #configure writer to write standard csv file
  writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(["Error", "Count"])
  for item in error_message_list:
    #Write item to outcsv
    writer.writerow([item[0], item[1]])

with open('user_statistics.csv', 'w') as f:
  #configure writer to write standard csv file
  writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(["Username", "INFO", "ERROR"])
  for item in user_statistics_list:
    #Write item to outcsv
    writer.writerow([item[0], item[1][0], item[1][1]])
