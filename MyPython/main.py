import subprocess
import time
import os
import signal

print("this is the start of main.py")

# start the single sensor for dev mode at beginning of Main program only
sensorDir = '/home/pbeata/Research/FireMonitoring/SENSORS/3_RemoteRepoSSH/'
sensorName = 'SimpleSensor.exe'
fullExePath = sensorDir + sensorName
#proc = subprocess.Popen(fullExePath, shell=True)
#print(proc.pid)


# terminate the single sensor
#killProc = 'kill ' + str(proc.pid)
#os.system("ps")
#os.system(killProc)


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

print("this is the end of main.py")

