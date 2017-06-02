#from numpy import *
import numpy as np
import matplotlib.pyplot as plt


numfire = 4
for counter in range(1, numfire + 1):
	print counter

data = np.loadtxt("../input/data4.txt")

timein = data[:,0]
print("length of timein is " + str(len(timein)))

m = data.shape[0]
n = data.shape[1]

hrrin = data[:, 1:n]
print("size of hrrin is " + str(hrrin.shape[0]) + " by " + str(hrrin.shape[1]))


'''
for row in range(0, m):
for col in range(0, n):
	print(str(data[row, col]))
print("\n")

plt.plot(timein, hrrin[:,0], "-o")
plt.show()
'''


# Simple data to display in various forms
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

plt.close('all')
'''
# Just a figure and one subplot
f, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')
'''
# Two subplots, the axes array is 1-d
#f, axarr = plt.subplots(2, sharex=True)
f, axarr = plt.subplots(4, sharex=True)
axarr[0].plot(x, y)
#axarr[0].set_title('Sharing X axis')
axarr[1].scatter(x, y)
axarr[2].plot(x, y)
axarr[3].scatter(x, y)

#plt.show()



def dosomething( thelist ):
  for element in thelist:
    print element


dosomething( ['1','2','3'] )
alist = ['red','green','blue']
dosomething( alist )  



def add(a, b):
  print "ADDING %d + %d" % (a, b)
  return a + b


def add_vectors(a, b):
	n = len(a)
	m = len(b)
	if n == m:
		c = np.zeros(n)
		for i in range(0, n):
			c[i] = a[i] + b[i]
	else:
		print "error: a and b must have same length to add them!"
	return c


x = 12.0
y = 24.0
z = add(x, y)
print z

xx = np.zeros(4) + 2.0
yy = np.zeros(4) + 10.0
zz = add_vectors(xx, yy)
dosomething(zz)



# read csv file
import csv
 
ifile = open('../output/test.csv', 'rb')
reader = csv.reader(ifile)
 
rownum = 0
for row in reader:
	# Save header row.
	if rownum ==0:
		header = row
	else:
		colnum = 0
		for col in row:
			print '%-8s: %s' % (header[colnum], col)
			colnum += 1
	rownum += 1
 
ifile.close()


filename = '../output/exp_signal_xc_n.csv'
my_data = np.genfromtxt(filename, delimiter=',')
print type(my_data)

mrows = np.shape(my_data)[0] 
ncols = np.shape(my_data)[1]
print(str(mrows) + ' by ' + str(ncols))

rownum = 0
for row in my_data:
	if rownum < 4:
		# do nothing (these are header rows only)
		x = 1
		print row
	elif rownum == 4:
		print row
		'''
		for v in row:
			print(str(float(v)))
			print type(v)
			print v * 20.0
		'''
	else:
		#print row
		y = 1
	rownum += 1
