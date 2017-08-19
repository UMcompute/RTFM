import urllib
import re
import httplib
import requests
import random


# need to include error handling for when site does not exist!
def download_updates(server_file_url, room):
  response = urllib.urlopen(server_file_url)
  csv = response.read()
  csv_str = str(csv)
  lines = csv_str.split("\\n")
  dest_url = 'room_' + str(room) + '.txt'
  fw = open(dest_url, 'w')
  for line in lines:
    fw.write(line + "\n")
  fw.close()

  fw1 = open('temp_log_' + str(room) + '.txt', 'a')
  fw2 = open('O2_log_' + str(room) + '.txt', 'a')
  fw3 = open('CO_log_' + str(room) + '.txt', 'a')
  fw4 = open('flux_log_' + str(room) + '.txt', 'a')
  
  for line in lines:
    line = line.strip(',')
    newData = []
    for number in line.split(','):
      newData.append(float(number))
    # column 0 is time (used in all log files)
    # column 1 is temperature
    fw1.write('%f, %f \n' % (newData[0], newData[1]))
    # column 2 is O2
    fw2.write('%f, %f \n' % (newData[0], newData[2]))
    # column 3 is CO
    fw3.write('%f, %f \n' % (newData[0], newData[3]))
    # column 6 is heat flux
    fw4.write('%f, %f \n' % (newData[0], newData[6]))
    
  fw1.close()
  fw2.close()
  fw3.close()
  fw4.close()
