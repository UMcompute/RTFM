import urllib
import re
import httplib
import requests
import random


# need to include error handling for when site does not exist!
# (see example below)
def download_updates(server_file_url):
  response = urllib.urlopen(server_file_url)
  csv = response.read()
  csv_str = str(csv)
  lines = csv_str.split("\\n")
  dest_url = 'new_data.txt'
  fw = open(dest_url, 'w')
  for line in lines:
    fw.write(line + "\n")
  fw.close()

  fw1 = open('temp_log.txt', 'a')
  fw2 = open('o2_log.txt', 'a')
  fw3 = open('hrr_log.txt', 'a')
  fw4 = open('flux_log.txt', 'a')
  
  for line in lines:
    line = line.strip(',')
    newData = []
    for number in line.split(','):
      newData.append(float(number))
    # column 0 is time (used in all log files)
    # column 1 is temperature
    fw1.write('%f, %f \n' % (newData[0], newData[1]))
    # column 2 is oxygen concentration
    fw2.write('%f, %f \n' % (newData[0], newData[2]))
    # column 3 is heat release rate
    fw3.write('%f, %f \n' % (newData[0], newData[3]))
    # column 4 is heat flux
    fw4.write('%f, %f \n' % (newData[0], newData[4]))
    
  fw1.close()
  fw2.close()
  fw3.close()
  fw4.close()

  
'''

def get_numbers():
    with open("yourfile.txt") as input_file:
        for line in input_file:
            line = line.strip()
            for number in line.split():
                yield float(number)
        
'''
  
'''
def download_stock_data(csv_url):
  response = urllib.urlopen(csv_url)
    # read the data from the url you are pointing to; all text stored in variable csv:
  csv = response.read()
  csv_str = str(csv)
  lines = csv_str.split("\\n")
    # use 'r' (for raw) before a file pass in order to provide an address here
  idNum = random.randrange(1, 1000)
  dest_url = 'update_' + str(idNum) + '.csv'
    fx = open(dest_url, 'w')
    for line in lines:
    fx.write(line + "\n")
    fx.close()
#dest_url = r'downloadedData.csv'



a="http://141.212.44.191:8080"
try:
  print "your server exists"
  #print urllib.urlopen(a)
except:
  print a + " site does not exist!"

#print("example of downloading files from the web")
#goog_url = a + "/update.csv"
#download_stock_data(goog_url)


fileName = a + "/update.csv"
download_updates(fileName)
print("new data downloaded!")
'''