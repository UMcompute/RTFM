import urllib
import re

# update the IP address, port, and file name to get from the visualization module
WIN_OS_IP = "141.213.169.232"
PORT = "8080"
FILENAME = "status.txt"

# use urllib package to get file from server
full_download_name = "http://" + WIN_OS_IP + ":" + PORT + "/" + FILENAME
full_save_name = "./" + FILENAME
start_main = 0

# [ insert  while loop start ]

# check if the status file contains the start key
urllib.urlretrieve(full_download_name, full_save_name)
file = open(full_save_name, "r")
for line in file:
  if re.search("start", line):
    print("time to start main program")
    start_main = 1
file.close()

# [ insert while loop end ]

print("move on to main time loop...")