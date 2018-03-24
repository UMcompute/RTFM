
# Real-time Fire Monitoring (RTFM)

This repository contains the source code for the real-time fire monitoring project (RTFM) at the University of Michigan. The goal of this project was to develop a fire-monitoring simulator "prototype" using previously-generated data from Fire Dynamics Simulator (FDS) as the input. The current real-time components of this system include an automated sensor simulator, an event-detection model for assessing fire hazards at each sensor location, and the main RTFM program which ties these features together (the "hub" for data coordination). As a post-processing step, the results of the event-detection model calculations are converted into XML-based schedules for use with BIM software to animate the fire hazards on a per-sensor basis throughout the building, assuming one per room. This post-processed data visualization relies on Bentley AECOsim Building Designer for schedule simulation.

## Getting Started

These instructions were designed to get this software built and running on your local machine for research, development, and testing purposes. This guide was developed and tested for Ubuntu users only, so far. Specifically, Ubuntu 16.04 was used for the most recent deployment and testing. Visualization with BIM is the only part that is not universally available (the only non-open source component).

### Prerequisites

It is expected that your machine has at least Python 2.7 or 3.x installed. You also need to have the gnu compiler for g++ and check that the "make" tool is available as well. Use the "which" command in your Linux terminal to check for these three components before proceeding with the remaining instructions (and get this main tools installed if you do NOT have them on your machine):
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

2. LCM recommends you also have these two packages for certain features: "openjdk-6-jdk" and "python-dev". For RTFM, it is recommended to add python-dev as well:
	```
	$ sudo apt-get install python-dev
	```

3. Download the LCM zip file from their website (https://github.com/lcm-proj/lcm/releases). This guide was made when LCM was in version 1.3.1, so I downloaded "lcm-1.3.1.zip" in the present. Save it to your $HOME directory or somewhere you can find it. Note that it will "build in source" with these default instructions, so make sure the unpacked files in the next step are in a stable location (do NOT delete them after).

4. Open the terminal, navigate to the location of "lcm-x.y.z.zip" from Step 3l; x.y.z for me was 1.3.1, as mentioned above. Unzip the LCM zip file:
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

**Note**: Running LCM on a networked machine (i.e., a university computer) causes errors for sending messages on the system multicast. You won't see the error immediately here, but you will see it if you try to use LCM in our RTFM application later. I do not have a solution for this, except to say that it would be best to build and run RTFM on your personal laptop where you have sudo access and control of the network firewalls, if needed.  

### Configure and Run RTFM

There are two more requirements for specific Python packages needed to run RTFM. They are the widely used "numpy" module and a tool for building XML files called "lxml". You can add them from the terminal using the following commands. The command to add the Python pip installer is given here as well:

```
$ sudo apt-get install python-pip
$ sudo -H pip install numpy
$ sudo apt-get install python-lxml
```

Clone this repository to a stable location. This project builds in its source based on a few simple scripts: while not employing a robust build system, this approach is sufficient for getting set up quickly and easily. Keep this cloned repository because it will be used for running RTFM simulations:

```
$ cd /where/you/want/to/build/
$ git clone https://github.com/pbeata/RTFM.git
$ cd RTFM/Exec
$ ./config.sh
```

This config bash script is used to "make" the sensor simulator and the event-detection model (both developed in C++).  It also prepares the individual data files for the test based on the provided output file from FDS (e.g., the propane_two_fire_devc.csv file used in the example of our journal paper). The "lcm-gen" command is used in this process to prepare the data structures needed for exchanging data between C++ and Python programs in our RTFM system. 

Assuming there were no major errors in the configure step, you are now ready to test RTFM for yourself! To run the code, simply execute the "run.sh" script now:

```
$ ./run.sh
```

This test will automatically use the input values stored in "input.txt" of this same directory. Now you will be prompted with 2-3 questions when the main RTFM program starts running:

1. Do you want to launch the event detection model? (0 is no, 1 is yes)
2. Do you want to launch the sensor simulator? (0 or 1)
3. <<if you answered yes to #1, then...>> Do you want to convert event detection output into XML format? (0 or 1)

Answer yes (1) to all three questions. Watch as the time stamp from the simulated sensor module is printed to the terminal along with the summary statistics at the end of the run. Check in the RTFM/Output/ directory to see the output of the event-detection model (SensorLog-*.txt) and the resulting, corresponding XML files (BIM schedules) generated based on that output.

The schedules contained in the XML files are formatted for use with Bentley Systems' AECOsim Building Designer BIM platform to visualize the evolving hazards during a fire event. Specifically, the Animation Producer is used to playback the monitoring events at this stage of the research. This is proprietary software, so not all users will have access to it or the BIM model used in our paper. However, the rest of the project is open-source up to this point. 

## Results of the Test

When you run the simulation with the provided input parameters, the results are as follows. Compare the values in the "Sensor Simulator Summary" and the "Main RTFM Summary" with your results to see if the values match. This test was run with the following input parameters (RTFM/Exec/input.txt):
* Number of sensors:  4
* Maximum time:  600.0 sec
* Nominal time step noise:  0.0 sec
* Sensor failure probability:  0.0  (*no sensors will "fail" in this sample test*)

```
**pbeata@pbeata:~/RTFM/Exec $ ./config.sh**

[UNIQUE SENSOR DATA FILES: 4]

[TOTAL OF 4 SENSOR FILES AVAILABLE]

g++ -g -Wall -O3 -c SensorEvent.cpp -o SensorEvent.o -llcm -std=c++11
...
...
g++ -g -Wall -O3 DataHandler.o SensorEDM.o main_edm.o -o EDM.ex -llcm -std=c++11
(attempted to delete old Output/ in base directory)

**pbeata@pbeata:~/RTFM/Exec $ ./run.sh**

[START MAIN RTFM]

Ready to launch Event Detection Model? (Enter 0 or 1) 1
Ready to launch the Sensor Simulator? (0 or 1) 1
Do you want to convert EDM output to XML? (0 or 1) 1

        {Started Event Detection Model}

../EventDetection/EDM.ex has input file: ../Exec/input.txt

        {Started Sensor Simulator}

../Sensors/SensorSim.ex has input file: ../Exec/input.txt

  time = 0.000 sec
  time = 1.000 sec
  time = 2.000 sec
  ...
  ...
  time = 599.000 sec
  time = 600.000 sec

	{Sensor Simulator Summary}
	  0 sensors failed
	  4 total sensors
	  0.00 percent failure rate
	  600.000 total time [sec]

	{End of Event Detection Model}

	Event start times for each room (in XML schedules):
	  [0.0, 150.0, 321.0, 524.0, -1.0]
	  [0.0, 55.0, 229.0, 229.0, 306.0]
	  [0.0, 187.0, 529.0, -1.0, -1.0]
	  [0.0, 163.0, 472.0, -1.0, -1.0]

	{Finished Writing EDM Output to XML}

	Messages received from all 4 sensors:
	[601, 601, 601, 601]

	[MAIN RTFM SUMMARY]
	  2404 total number of data messages received
	  601 minimum messages sent from sensor #0
	  601 maximum messages sent from sensor #0
	  601.00 average messages sent from all sensors
	  4.01 average messages received per second
	  600.000 total time in MAIN RTFM

[END MAIN RTFM]
```

Finally, you can also plot the input/output shown in our journal paper by navigating to the PostProcess/ directory and typing these commands individually:
```
python plot_input.py
python plot_output.py
```

## Authors

* **Paul A. Beata** - *Ph.D. Student* - [pbeata on GitHub](https://github.com/pbeata)
* This work was presented in our Fire Technology journal paper from 2018 (TODO: ADD LINK TO JOURNAL HERE).
* How to cite this work: (TODO: ADD CITATION INFO)

## Acknowledgments

* This project was funded by the Chief Donald J. Burns Memorial Research Grant via SFPE.
* This README file was based on the template provided by [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md).
