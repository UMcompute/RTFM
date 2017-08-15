from lxml import etree
import csv
import numpy as np
#import matplotlib.pyplot as plt

#==============================================================================

# input and setup
NUM_ROOMS = 4
maxTime = 600.0   # seconds

edmBaseFile = "edm_output"
baseFileName = "example"
fileName = "example.xml"
fullName = "C:\\Users\\pbeata\\" + fileName
taskFile = "task_template.csv"

eventLabels = ['warning', 'threat', 'severe']

preamble = ["Name", "TimeFormat", "File", "FileFormat", \
"StartDate", "EarlyStartDate", "LateStartDate", "FinishDate", \
"EarlyFinishDate", "LateFinishDate", "CreationDate" ]

preamleValues = ["Untitled", "s", fullName, "1", \
"2017-10-16T07:00:00", "2017-10-16T07:00:00", "2017-10-16T07:00:00", "2017-10-16T07:10:00", \
"2017-10-16T07:10:00", "2017-10-16T07:10:00", "2017-10-01T07:00:00" ]

firstLine = '<?xml version="1.0"?>\n'
finalOption = "ExtendedAttributes"

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

'''
print(threatLevel)
fig1, ax = plt.subplots()
for i in range(0, NUM_ROOMS):
  ax.plot(edmTime, threatLevel[:,i])
fig1.tight_layout()
plt.show()
'''
#==============================================================================

numLevels = 3
for i in range(0, NUM_ROOMS):
  events = []
  for j in range(0, numLevels):
    checkIndex = np.argmax(threatLevel[:,i] > j)
    if (checkIndex != 0):
      events.append(edmTime[checkIndex])
  print(events)



# start the main tree
root = etree.Element("Project", xmlns="http://schemas.microsoft.com/project")

# create am attribute for each of the preamble components
counter = 0
for option in preamble:
  root.append(etree.Element(option))
  root[counter].text = preamleValues[counter]
  counter += 1
root.append(etree.Element(finalOption))

# create the tree of tasks for BIM
taskTree = etree.SubElement(root, "Tasks")
taskList = []
for i in range(0, len(eventLabels)):
  taskList.append(etree.SubElement(taskTree, "Task"))

# get all the task attributes listed in the template file
with open(taskFile, 'r') as f:
  reader = csv.reader(f)
  taskAttrib = list(reader)

# cycle through all tasks and add templated values
for i in range(0, len(taskList)):
  taskList[i].append(etree.Element(taskAttrib[0][0]))
  taskList[i][0].text = str(i+1)
  for j in range(1, len(taskAttrib)):
    taskList[i].append(etree.Element(taskAttrib[j][0]))
    taskList[i][j].text = taskAttrib[j][1]
  taskList[i].append(etree.Element("ExtendedAttribute"))
  taskList[i][-1].append(etree.Element("UID"))
  taskList[i][-1][0].text = str(i+1)
  taskList[i][-1].append(etree.Element("FieldID"))
  taskList[i][-1][1].text = "188743750"
  taskList[i][-1].append(etree.Element("Value"))
  taskList[i][-1][2].text = "0"

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
print(etree.tostring(root, pretty_print=True))

# write schedule to output file
fw = open(fileName, 'w')
fw.write(firstLine)
fw.write(etree.tostring(root, pretty_print=True))
fw.close()

