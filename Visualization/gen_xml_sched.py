from lxml import etree
import csv

#==============================================================================

# input and setup
fileName = "example.xml"
fullName = "C:\\Users\\pbeata\\" + fileName
taskFile = "task_template.csv"

#eventLabels = ['ambient', 'warning', 'threat', 'severe']
eventLabels = ['Ambient_Initial', 'First_Warning', 'Major_Threat']

preamble = ["Name", "TimeFormat", "File", "FileFormat", \
"StartDate", "EarlyStartDate", "LateStartDate", "FinishDate", \
"EarlyFinishDate", "LateFinishDate", "CreationDate" ]

preamleValues = ["Untitled", "s", fullName, "1", \
"2017-08-01T08:29:35", "2017-07-29T13:42:51", "2017-07-29T13:42:51", "2017-08-01T16:55:02",\
"2017-08-13T13:42:52", "2017-08-13T13:42:52", "2017-07-29T13:42:51" ]

firstLine = '<?xml version="1.0"?>\n'
finalOption = "ExtendedAttributes"

#==============================================================================

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
