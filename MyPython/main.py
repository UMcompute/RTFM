import subprocess
import time
import os
import signal

print("this is the start of main.py")

print("   Main Menu: ")

answer = '2'
while answer == '2':
  answer = raw_input('  Start new sensor? (1/0) ')
  print ' You chose ' + answer

  if answer == '1':
    sensorDir = raw_input('   what is the sensor directory? ')
    sensorName = raw_input('    what is the sensor source code name? ')
  elif answer == '0':
    print('no sensor will be used!')
  else:
    print("***error: please enter only 1 (yes) or 0 (no)");
    answer = '2'


# start the single sensor for dev mode at beginning of Main program only

# requires that we know where the sensor is located
sensorDir = '/home/pbeata/Research/FireMonitoring/SENSORS/3_RemoteRepoSSH/'
# requires this application be compiled first
sensorName = 'SimpleSensor.exe'   
fullExePath = sensorDir + sensorName


# OPTION 0

'''
#proc = subprocess.Popen(fullExePath, shell=True)
#print(proc.pid)

# terminate the single sensor
#killProc = 'kill ' + str(proc.pid)
#os.system("ps")
#os.system(killProc)
'''

# OPTION 1

'''
# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
pro = subprocess.Popen(fullExePath, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 

# assume some calculations take 3 seconds
print("sleep for 3 seconds... then kill proc")
time.sleep(3)
os.system("ps")

# Send the signal to all the process groups
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  
os.system("ps")
'''

# OPTION 2

# start the sensor program
p = subprocess.Popen("exec " + fullExePath, shell=True)

# assume some calculations take 3 seconds
print("sleep for 3 seconds... then kill proc")
time.sleep(3)

# kill the sensor program
p.kill()

# can python run the Makefile of a c++ app for us too?


print("this is the end of main.py")

