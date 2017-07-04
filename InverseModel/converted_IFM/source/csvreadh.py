import numpy as np


def csvreadh_func(filename=None):
  my_data = np.genfromtxt(filename, delimiter=',')
  numRowsHeader = 4
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
  #print('size of csv data: ' + str(mrows) + ' by ' + str(ncols))
  return dataMat
