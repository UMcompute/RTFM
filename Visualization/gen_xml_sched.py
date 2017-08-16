from lxml import etree
import csv
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================

# input and setup
NUM_ROOMS = 4
minTime = 0.0     # seconds
maxTime = 600.0   # seconds

edmBaseFile = "edm_output"
baseFileName = "example"
pathToFile = "C:\\Users\\pbeata\\Desktop\\"
taskFile = "task_template.csv"

eventLabels = ['initial', 'warning', 'threat', 'severe']

# starting color id #'s correspond to G-Y-O-R in ABD
# finishing color id #'s correspond to Y-O-R-R in ABD
startColor =  ['65280', '65535', '32767', '255']
finishColor = ['65535', '32767', '255',   '255']
numLevels = len(eventLabels)

preamble = ["Name", "TimeFormat", "File", "FileFormat", \
"StartDate", "EarlyStartDate", "LateStartDate", "FinishDate", \
"EarlyFinishDate", "LateFinishDate", "CreationDate" ]

preamleValues = ["Untitled", "s", baseFileName, "1", \
"2017-10-16T07:00:00", "2017-10-16T07:00:00", "2017-10-16T07:00:00", "2017-10-16T07:10:00", \
"2017-10-16T07:10:00", "2017-10-16T07:10:00", "2017-10-01T07:00:00" ]

firstLine = '<?xml version="1.0"?>\n'
finalOption = "ExtendedAttributes"
datePrefix = "2017-10-16T"

#==============================================================================
#	READ EDM OUTPUT FROM CSV FILES
for i in range(0, NUM_ROOMS):
  edmFile = edmBaseFile + "_" + str(i) + ".csv"
  A = np.loadtxt(edmFile, delimiter=",")
  if (i == 0):
    numSteps = np.shape(A)[0]
    numCols = np.shape(A)[1]
    allData = np.zeros((numSteps, numCols, NUM_ROOMS))
  allData[:,:,i] = A

# get the time array
edmTime = allData[:,0,0]

# get all individual warning columns
WARN = np.zeros((numSteps, NUM_ROOMS, 3))
for i in range(0, NUM_ROOMS):
  WARN[:,i,0] = allData[:,10,i]   # smoke toxicity
  WARN[:,i,1] = allData[:,11,i]   # burn threats
  WARN[:,i,2] = allData[:,12,i]   # fire status

# compare all hazards for each time step to assess threat
threatLevel = np.zeros((numSteps,NUM_ROOMS))
for i in range(0, NUM_ROOMS):
  for j in range(0, numSteps):
    s = int(WARN[j, i, 0])    # smoke warning
    b = int(WARN[j, i, 1])    # burn warning
    f = int(WARN[j, i, 2])    # fire warning

    if ((s==1) or (b==1) or (f==1)):
      threatLevel[j,i] = 1

    if ((s==1 and b==1) or (b==1 and f==1) or (s==1 and f==1)):
      threatLevel[j,i] = 2

    if ((s==1) and (b==1) and (f==1)):
      threatLevel[j,i] = 3  
    
    if ((s==2) or (b==2) or (f==2)):
      threatLevel[j,i] = 3

# plot the threat level results to check
fig1, ax = plt.subplots()
for i in range(0, NUM_ROOMS):
  ax.plot(edmTime, threatLevel[:,i])
fig1.tight_layout()
#plt.show()

# determine start time of each threat (per room) if it exists
startTime = [[] for x in xrange(NUM_ROOMS)]
numEvents = [[] for x in xrange(NUM_ROOMS)]
for i in range(0, NUM_ROOMS):
  for j in range(0, numLevels):
    startTime[i].append(-1.0)
    numEvents[i].append(1)
    if (j == 0):
      startTime[i][j] = minTime
    else:
      checkIndex = np.argmax(threatLevel[:,i] > j-1)
      if (checkIndex != 0):
        startTime[i][j] = edmTime[checkIndex]
      else:
        numEvents[i][j] = 0

# check event output before writing
for i in range(0, NUM_ROOMS):
  print(startTime[i])
  #print(numEvents[i])

#==============================================================================

# WRITE THE XML FILE BASED ON THE TASK TIMES
taskCounter = 0   # used to give unique UID to each task
for room in range(0, NUM_ROOMS):
  fileName = baseFileName + str(room+1) + ".xml"
  fullName = pathToFile + fileName
  root = None

  # start the main tree
  root = etree.Element("Project", xmlns="http://schemas.microsoft.com/project")

  # create an attribute for each of the preamble components
  counter = 0
  preamleValues[0] = "Room-" + str(room+1) + "-Events"
  preamleValues[2] = fullName
  for option in preamble:
    root.append(etree.Element(option))
    root[counter].text = preamleValues[counter]
    counter += 1
  root.append(etree.Element(finalOption))

  # create the tree of tasks for BIM
  taskTree = etree.SubElement(root, "Tasks")
  taskList = []
  for i in range(0, numLevels):
    if (numEvents[room][i] != 0):
      taskList.append(etree.SubElement(taskTree, "Task"))
  print("Room %d has %d events" % (room+1, len(taskList)) )

  # get all the task attributes listed in the template file
  with open(taskFile, 'r') as f:
    reader = csv.reader(f)
    taskAttrib = list(reader)

  # cycle through all tasks and add templated values
  i = 0
  for k in range(0, numLevels):
    if (numEvents[room][k] != 0):
      #==============================================================
      # unique task details
      roomDetails = []
      roomDetails.append("0")                     # Flag
      roomDetails.append(eventLabels[k] + "-" +str(room+1))   # Name
      roomDetails.append("1")                     # ConstructionType
      # start times
      myStart = int(startTime[room][k])
      S = int(myStart%60)
      M = int((myStart - S) / 60)
      if (M < 10):
        M = "0" + str(M)
      if (S < 10):
        S = "0" + str(S)
      realTime = "07" + ":" + str(M) + ":" + str(S)
      #print(realTime)
      roomDetails.append(datePrefix + realTime)   # Start
      roomDetails.append(datePrefix + realTime)   # Early Start
      roomDetails.append(datePrefix + realTime)   # Late Start
      # end times 
      try:
        endTime = startTime[room][k+1]
        if (endTime != -1.0):
          myEnd = startTime[room][k+1]
        else:
          checkIndex = np.argmax(startTime[room][:] > -1.0)
          if (checkIndex > k):
            myEnd = startTime[room][checkIndex]
      except IndexError:
        myEnd = maxTime
      S = int(myEnd%60)
      M = int((myEnd - S) / 60)
      if (M < 10):
        M = "0" + str(M)
      if (S < 10):
        S = "0" + str(S)
      realTime = "07" + ":" + str(M) + ":" + str(S)
      #print(realTime)
      roomDetails.append(datePrefix + realTime)   # Finish
      roomDetails.append(datePrefix + realTime)   # Early Finish
      roomDetails.append(datePrefix + realTime)   # Late Finish
      #==============================================================
      taskList[i].append(etree.Element(taskAttrib[0][0]))
      # updated to give each task a unique UID just in case of conflict in ABD later
      #taskList[i][0].text = str(i+1)
      taskCounter += 1
      taskList[i][0].text = str(taskCounter)
      for j in range(1, len(taskAttrib)):
        taskList[i].append(etree.Element(taskAttrib[j][0]))
        if (j < 10):
          taskList[i][j].text = roomDetails[j-1]
        else:
          if (taskAttrib[j][0] == "StartColor"):
            taskList[i][j].text = startColor[k]
          elif (taskAttrib[j][0] == "FinishColor"):
            taskList[i][j].text = finishColor[k]
          else:
            taskList[i][j].text = taskAttrib[j][1]
      taskList[i][-1].text = preamleValues[-1]
      taskList[i].append(etree.Element("ExtendedAttribute"))
      taskList[i][-1].append(etree.Element("UID"))
      taskList[i][-1][0].text = str(i+1)
      taskList[i][-1].append(etree.Element("FieldID"))
      taskList[i][-1][1].text = "188743750"
      taskList[i][-1].append(etree.Element("Value"))
      taskList[i][-1][2].text = "0"
      i += 1

  # add the calendar info to the end of the file
  root.append(etree.Element("CalendarUID", xmlns=""))
  root[-1].text = "1"
  root.append(etree.Element("MinutesPerDay", xmlns=""))
  root[-1].text = "1440"
  root.append(etree.Element("MinutesPerWeek", xmlns=""))
  root[-1].text = "10080"
  root.append(etree.Element("DaysPerMonth", xmlns=""))
  root[-1].text = "30"

  # start the calendar tree
  calTree = etree.SubElement(root, "Calendars", xmlns="")
  calendar = etree.SubElement(calTree, "Calendar")
  calendar.append(etree.Element("UID"))
  calendar[-1].text = "1"
  calendar.append(etree.Element("Name"))
  calendar[-1].text = "Standard"
  calendar.append(etree.Element("IsBaseCalendar"))
  calendar[-1].text = "1"
  calendar.append(etree.Element("BaseCalendarUID"))
  calendar[-1].text = "-1"
  week = etree.SubElement(calendar, "WeekDays")
  for i in range(1, 8):
    week.append(etree.Element("WeekDay"))
    week[-1].append(etree.Element("DayType"))
    week[-1][-1].text = str(i)
    week[-1].append(etree.Element("DayWorking"))
    week[-1][-1].text = "1"
    week[-1].append(etree.Element("WorkingTimes"))
    week[-1][-1].append(etree.Element("WorkingTime"))
    week[-1][-1][-1].append(etree.Element("FromTime"))
    week[-1][-1][-1][-1].text = "00:00:00"
    week[-1][-1][-1].append(etree.Element("ToTime"))
    week[-1][-1][-1][-1].text = "00:00:00"

  # check the results in the terminal
  #print(etree.tostring(root, pretty_print=True))

  # write schedule to output file
  fw = open(fileName, 'w')
  fw.write(firstLine)
  fw.write(etree.tostring(root, pretty_print=True))
  fw.close()

