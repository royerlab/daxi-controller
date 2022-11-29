devicefacilitator design notes
current colleciton of devices:
stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta,
oscilloscope_channel1
oscilloscope_channel2
oscilloscope_channel3
oscilloscope_channel4

1.set_configurations(acquisition_config_panel)
	panel is the pannel of all virtual and physical devices to be used in this task, with the given configurations.
	read all the relevant configurations
	get metronome
	get counter
	get ao bundle and ao subtasks
	get do bundle and do subtasks

2. prepare sub tasks and calculate the data for all sub tasks.

3. prepare metronome.
4. prepare AO task bundle.
5. add metronome and subtasks to the task bundle

6. everybody_get_ready
	# the order of poeple to get ready perhaps matters.
	counter.get_ready()
	metronome.get_ready()
	aobundle.get_ready()
	dobundle.getready()

7. now start the concert.

8. wait for user input

9. stop the concert.


during view switching - should enable soft transitioning of the view switching galvos.
Perhaps this should be a function handled by the device facilitator as specified for each 
acquisition mode.



# each method is like a skill for this facilitator, and each time when we add an extra
# acquisition mode, we implement an extra method for the device facilitator
3.1 acquisition_mode1_start()
	properly starts everybody
3.2 acquisition_mode1_stop()
	properly stops everybody
3.3 acquisition_mode1_close()
	properly closes everybody.


4. acquisition_mode2_start()
...

acquisition mode shall be determined by the acquisition_config_panel_1
The connection port of the configuration panels should be defined per microscope, but the tempalte should follow the same format.
6 different data acquisition modes:
aqstn_panel_1 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.  loop order [position, ]
aqstn_panel_2 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
aqstn_panel_3 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
aqstn_panel_4 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
aqstn_panel_5 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
aqstn_panel_6 - data acquisition - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
[mode 1] - [layer 1: position] - [layer 2: view] - [layer 3: color] - [layer 4: slice]  141.692 # this mode is probably meaning less. would it be?
[mode 2] - [layer 1: position] - [layer 2: view] - [layer 3: slice] - [layer 4: color]  141.646
[mode 3] - [layer 1: position] - [layer 2: view] - [layer 3: slice, color]  70.846
[mode 4] - [layer 1: position, view] - [layer 2: color] - [layer 3: slice]  141.692
[mode 5] - [layer 1: position, view] - [layer 2: slice] - [layer 3: color]  141.646
[mode 6] - [layer 1: position, view] - [layer 2: slice, color] 70.846

generate_data function should be used based on this one perhaps? let's think about it.


x different inspection acquisition modes:
inspect DAQ card (use NIMAX)
1. aqstn_panel_7.1/2/3/4/5 - sinusoidal scan of SG/VS1/VS2/beta/gamma.
2. aqstn_panel_8.1/2/3/4/5 - raster scan of SG/VS1/VS2/beta/gamma with soft retraction
3. aqstn_panel_9 - inspect stage - can move as expected
4. aqstn_panel_10 - inspect camera - can acquire data and save out data as expected
5. aqstn_panel_11 - data saving inspection

x different alignment and calibration acquisition modes:
1. align O3:
    template - stage, cam, LED, lasers, water pump, metronome, counter1, counter2, SG, VS1, VS2, gamma, beta, mode index.
    grand facilitator coordinates with the area facilitator. it read from the grand config panel.
    give the corresponding configs to the corresponding area facilitator
    each area facilitator facilitates the activities in their own area.
2. calibration SG speed.
3. calibration pivot galvo.
4. calibrate strip reduction galvo.

devicefcltr.set_configurations
devicefcltr.get_ready
devicefcltr.start
