import os
import subprocess
import time
# from subprocess import Popen

for x in range(3):

	# os.system("./A")
	# p = Popen("./A")
	# p = os.popen("./A")
	proc = subprocess.Popen('./a.out', shell=True)
	print(proc.pid)
	'''
	NOTE: If you really wanted to implement a robust main loop
	for the fire monitoring project, you would need to provide
	some preprocessing "check" to make sure that the compiled
	executable existed in the project directory first. Otherwise,
	this Popen command used here would not work when it can't
	find ./A where it expects it.

	We should be very careful with shell=True!!! This code has
	been warned as a security issue (don't let that exe be 
	a user input because if they provide rm-rf everything 
	could be DELETED).
	'''

	os.system("echo 'hello world from shell!'")
	os.system("ps")
	print("time to wait ... ")

	# time.sleep(12)
	proc.wait()
	#proc.terminate()
	#proc.wait()

	# NOTE: don't ignore the terminate command ==> need to investigate

	update = "finished with time step: " + str(x)
	print(update)

print("finished with MainLoop.py")

