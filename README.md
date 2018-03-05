
# Real-time Fire Monitoring (RTFM)

This repository contains the source code for the real-time fire monitoring project (RTFM) at the University of Michigan. The goal of the software project was to provide a fire-monitoring simulator using previously data generated from Fire Dynamics Simulator (FDS). The current real-time components of this system include an automated sensor simulator, an event detection model for assessing fire hazards at each sensor location, and the main RTFM program which ties these features together. As a post-processing step, the results of the event detection model calculations are converted into XML-based schedules for use with BIM software to animate the fire hazards on a per-sensor basis throughout the building, assuming one per room.

## Getting Started

These instructions were designed to get this project built and running on your local machine for development and testing purposes. This guide was developed and tested for Ubuntu users only, so far. Specifically, Ubuntu 16.04 was used for the most recent deployment and testing. 

### Prerequisites

It is expected that your machine has at least Python 2.7 or 3.x installed. You also need to have the gnu compiler for g++ and check that the "make" tool is available as well. Use the "which" command in the terminal to check for these three components before proceeding with the remaining instructions:
```
$ which g++
/usr/bin/g++
$ which python
/usr/bin/python
$ which make
/usr/bin/make
```

### LCM Dependency

This project requires Lightweight Communications and Marshalling (LCM) for message-passing between applications written in dissimilar programming languages. While the build instructions for LCM are provided on their own website (https://lcm-proj.github.io/build_instructions.html), they have been reproduced here for completeness. Use these instructions to install LCM in Ubuntu:

1. LCM requires two packages: "build-essential" and "libglib2.0-dev". You can get these via the "sudo apt-get install [package-name]" command:
	```
	$ sudo apt-get install build-essential
	$ sudo apt-get install libglib2.0-dev
	```

2. LCM recommends you also have these two packages for certain features: "openjdk-6-jdk" and "python-dev". For RTFM, it is good to add python-dev as well:
	```
	$ sudo apt-get install python-dev
	```

3. Download the LCM zip file from their website (https://github.com/lcm-proj/lcm/releases). This guide was made when LCM was in version 1.3.1, so I downloaded "lcm-1.3.1.zip" in the present. Save it to your $HOME directory or somewhere you can find it. Note that it will "build in source" with these default instructions, so make sure the unpacked files in the next step are in a stable location.

4. Open the terminal, navigate to the location of "lcm-x.y.z.zip" from Step 3. Unzip the LCM zip file:
	```
	$ cd /path/to/lcm/zip
	$ unzip lcm-x.y.z.zip
	```

5. Change into that unzipped directory and build LCM:
	```
	$ cd lcm-x.y.z
	$ sudo ./configure
	$ sudo make
	$ sudo make install
	$ sudo ldconfig
	```

6. Check that LCM is available by running this command (you should see all the help options fill your terminal if LCM was properly installed):
	```
	$ lcm-gen --help
	```
**Note**: Running LCM on a networked machine (i.e., a university computer) causes errors for sending messages on the system multicast. You won't see the error here, but you will see it if you try to use LCM in an application later. I do not have a solution for this, except to say that it would best to build and run RTFM on your laptop where you have sudo access and control of the network firewalls. 

### Configure and Run RTFM

There are two more requirements for specific Python packages needed to run RTFM. They are the widely used "numpy" module and a tool for building XML files called "lxml". You can add them from the terminal using the following commands:

```
$ sudo apt-get install python-pip
$ sudo -H pip install numpy
$ sudo apt-get install python-lxml
```

Clone this repository to a stable location. This project builds in its source with based on a few simple scripts: while not employing a robust build system, this approach is sufficient for getting set up quickly and easily. Keep this cloned repository because it will be used for running RTFM simulations:

```
$ cd /where/to/build/
$ git clone https://github.com/pbeata/RTFM.git
$ cd RTFM/Exec
$ ./config.sh
```

This config bash script is used to "make" the sensor simulator and the event detection model (build developed in C++).  It also prepares the individual data files for the test based on the provided output file (propane_two_fire_devc.csv file) from FDS. The "lcm-gem" command used in this process to prepare the data structures needed for exchanging data between C++ and Python programs in RTFM. 

Assuming there were no major errors in the configure step, you are now ready to test RTFM for yourself! To run the code, simply execute the "run" script now:

```
$ ./run.sh
```

Some errors that you could see are related to Python packages numpy and lxml, which are both used by RTFM. If errors related to the absence of these packages arise, then go back and make sure they are installed properly (see above).

By default, this test will use the input values stored in "input.txt" of this same directory. Now you will be prompted with 2-3 questions:

1. Do you want to launch the event detection model? (0 is no, 1 is yes)
2. Do you want to launch the sensor simulator? (0 or 1)
3. (if you answered yes to #1, then...) Do you want to convert event detection output into XML format? (0 or 1)

Answer yes (1) to all three questions. Watch as the time stamp from the simulated sensor module is printed to the terminal along with the summary statistics at the end of the run. Check in the RTFM/Output/ directory to see the output of the event detection model (SensorLog-*.txt) and the resulting XML files generated based on that output. 

The schedules contained in the XML files are formatted for use with Bentley Systems' AECOsim Building Designer BIM platform to visualize the evolving hazards during a fire event. 

## Results of the Test

When you run the simulation with the provided input parameters, the results are as follows. Compare the values in the "Sensor Simulator Summary" and the "Main RTFM Summary" with your results to see if the values match. This test was run with the following input parameters (RTFM/Exec/input.txt):
* Number of sensors:  4
* Maximum time:  600 sec
* Nominal time step:  1.1 sec
* Sensor failure probability:  0.0  (*no sensors will "fail" in this test*)

```
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
```

## Authors

* **Paul A. Beata** - *Ph.D. Student* - [pbeata on GitHub](https://github.com/pbeata)
* This work was described in our Fire Technology journal paper from 2018 (ADD LINK TO JOURNAL).


## Acknowledgments

* This README file was based on the template provided by [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md).
* This README file was edited and written with [StackEdit](https://stackedit.io/).
