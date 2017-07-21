import numpy as np


def csvreadh_func(filename=None):
  my_data = np.genfromtxt(filename, delimiter=',')
  numRowsHeader = 0   # ROWS TO SKIP IN CSV FILE
  mrows = np.shape(my_data)[0] 
  ncols = np.shape(my_data)[1]
  dataMat = np.zeros((mrows - numRowsHeader, ncols))
  rownum = 0
  for row in my_data:
    if rownum >= numRowsHeader:
      colnum = 0
      for v in row:
        dataMat[rownum - numRowsHeader][colnum] = v
        colnum += 1
    rownum += 1
  return dataMat


A = csvreadh_func('signal_exp.csv')
numsignal = 8
num_sec = 501

xp = np.linspace(0.0, 500.0, 51)
xi = np.linspace(0.0, 500.0, num_sec)

B = np.zeros((num_sec,numsignal))

for i in range(0, numsignal):
  yp = A[:,i]
  yi = np.interp(xi, xp, yp)
  B[:,i] = yi




# function defining the significant digits to be printed
def my_format(value):
  return "%.6f" % value

fw = open('interp_data.csv', 'w')
for i in range(0, num_sec):
  for v in B[i,:]:
    fw.write(str(my_format(v)) + ',')
  fw.write('0.0 \n')
fw.close()
