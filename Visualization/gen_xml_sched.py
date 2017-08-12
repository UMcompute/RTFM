from lxml import etree
import csv

#==============================================================================

# input and setup
fileName = "example.xml"
fullName = "C:\\Users\\pbeata\\" + fileName
taskFile = "task_template.csv"
eventLabels = ['ambient', 'warning', 'threat', 'severe']

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
  for j in range(0, len(taskAttrib)):
    taskList[i].append(etree.Element(taskAttrib[j][0]))
    taskList[i][j].text = taskAttrib[j][1]

# check the results in the terminal
print(etree.tostring(root, pretty_print=True))

# write schedule to output file
fw = open(fileName, 'w')
fw.write(firstLine)
fw.write(etree.tostring(root, pretty_print=True))
fw.close()
