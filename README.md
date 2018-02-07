# RTFM

This repository contains the source code for the real-time fire monitoring project (RTFM) at the University of Michigan. 


# Requirements

This guide was developed and tested for Ubuntu users only. It is expected that your machine has at least Python 2.7 or 3.x installed. You also need to have the gnu compiler for g++ and also check that the make command is working:

$ which python
/usr/bin/python

$ which g++
/usr/bin/g++

$ which make
/usr/bin/make


# LCM Dependency

This project requires Lightweight Communications and Marshalling (LCM). While the build instructions for LCM are provided on their website (https://lcm-proj.github.io/build_instructions.html), they have been reproduced here for completeness. Use these instructions to install LCM in Ubuntu:

1. LCM requires two packages: "build-essential" and "libglib2.0-dev". You can get these via the command "sudo apt-get install [package-name]"

2. LCM recommends you also have these two packages for certain features (you can likely skip this step for using LCM with RTFM): "openjdk-6-jdk" and "python-dev".

3. Download the LCM zip file from their website (https://github.com/lcm-proj/lcm/releases). This guide was made when LCM was in version 1.3.1, so I downloaded "lcm-1.3.1.zip" in the present. Save it to your $HOME directory or somewhere you can find it. Note that it will "build in source" with these default instructions, so make sure the unpacked files in the next step are in a stable location.

4. Open the terminal, navigate to the location of lcm-x.y.z.zip from Step 3. Unzip the LCM zip file:
$ cd /path/to/lcm/zip
$ unzip lcm-x.y.z.zip

5. Change into that unzipped directory and build LCM:
$ cd lcm-x.y.z.zip
$ sudo ./configure
$ sudo make
$ sudo make install
$ sudo ldconfig

6. Check that LCM is available by running this command (you should see all the help options fill your terminal):
$ lcm-gen --help


# Configure and Run RTFM

Clone this repository to a stable location (this project builds in its source with a few primitive scripts).

$ git clone https://github.com/pbeata/RTFM.git
$ cd RTFM/Exec
$ ./config.sh

Assuming there were no major errors that you could solve with a quick Google search, you are now ready to test RTFM for yourself! To run the code, simply execute the run script now:

$ ./run.sh

By default, it will use the input values stored in "input.txt" of this same directory. Now you will be prompted with 2-3 questions. 

1. Do you want to launch the event detection model? (0 is no, 1 is yes)
2. Do you want to launch the sensor simulator? (0 or 1)
3. (if you answered yes to #1, then...) Do you want to convert event detection output into XML format? (0 or 1)

Answer yes (1) to all three questions. Watch as the time stamp from the simulated sensor module is printed to the terminal along with the summary statistics at the end of the run. Check in the RTFM/Output/ directory to see the output of the event detection model and the resulting XML files generated based on that output. 

The schedules contained in the XML files are formatted for use with Bentley Systems' AECOsim Building Designer BIM platform to visualize the evolving hazards during a fire event. 


# Sample Output

pbeata@Paul-Laptop:~/Desktop/RTFM/Exec$ ./run.sh 

[START MAIN RTFM]

Ready to launch Event Detection Model? (Enter 0 or 1) 1
Ready to launch the Sensor Simulator? (0 or 1) 1
Do you want to convert EDM output to XML? (0 or 1) 1

  {Started Event Detection Model}

../EventDetection/EDM.ex has input file: ../Exec/input.txt 

  {Started Sensor Simulator}

../Sensors/SensorSim.ex has input file: ../Exec/input.txt 

  time = 0.815 sec
  time = 1.762 sec
  time = 3.144 sec
  time = 3.787 sec
  ...
  ...
  ...
  time = 596.923 sec
  time = 597.809 sec
  time = 598.590 sec
  time = 599.699 sec

  {Sensor Simulator Summary}
    0 sensors failed
    4 total sensors
    0.00 percent failure rate
    599.867 total time [sec]


  {End of Event Detection Model}

  {Finished Writing EDM Output to XML}


  Messages received from all 4 sensors:
  [561, 569, 559, 567]

  [MAIN RTFM SUMMARY]
    2256 total number of data messages received
    559 minimum messages sent from sensor #2
    569 maximum messages sent from sensor #1
    564.00 average messages sent from all sensors
    3.76 average messages received per second
    599.867 total time in MAIN RTFM

[END MAIN RTFM]
