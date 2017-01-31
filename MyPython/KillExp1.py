import subprocess
import psutil   # error because psutil is not avail in non-Windows OS


print(" ")
print("test code started")


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.get_children(recursive=True):
        proc.kill()
    process.kill()


sensorDir = '/home/pbeata/Research/FireMonitoring/SENSORS/3_RemoteRepoSSH/'
sensorName = 'SimpleSensor.exe'
fullExePath = sensorDir + sensorName

proc = subprocess.Popen(fullExePath, shell=True)
try:
    proc.wait(timeout=3)
except subprocess.TimeoutExpired:
    kill(proc.pid)

print("test code completed")
print(" ")
