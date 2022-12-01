## Processes Facilitator Classes:
0. ProcessesFcltr
1. AcquisitionFcltr
2. AlignmentFcltr
3. CalibrationFcltr
4. InspectionFcltr
5. NavigationFcltr
6. SystemFcltr

ProcessesFcltr is the chief of all other Fcltr classes. 

The Main gui will have a few buttons, that says mode:

acquisition, alignment, calibration, inspection, navigation

click on each button would handover the job to the corresponding facilitator.

### 0. ProcessesFcltr
Think about what this class handles.
This ProcessesFcltr communicate with all the GUI components, and connect SystemFcltr with all the rest of the 
focused-processes facilitators.
It should have a button that says "start" to start the corresponding processes, and a "stop" button to stop everything.
when start is clicked, there has to be a router to route the processes delivered by the SystemFcltr intot he hands
of the focused processes facilitators (AcquisitionFcltr, AlignmentFcltr, CalibrationFcltr, InspectionFcltr, and 
NavigationFcltr).


### 1. AcquisitionFcltr
This facilitator coordinates all the actions regarding data acquisiton in a non-interactive fashion.
The data acquisition can be grouped into different acquisition mode, that are configured from a GUI panel, 
or loaded and modified from a template.
Note that acquisition facilitator do not handle scripting. Scripting is coordianted at the system facilitator's level.

The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
when the choice is a type of acquisition process, the process would be handed over to the AcquisitionFcltr by the 
ProcessesFcltr, and this AcquisitionFcltr would then generate configuraiton panels based on the parameters of choice.

1. 6 scanning mode with different sequences across position, color, view.
2. light sheet scan + static sample acquisition
3. O1 scan static light sheet, static sample.
4. O3 scan, static light sheet, static sample.

### 2. AlignmentFcltr
The alignment facilitator coordiantes all the actions regarding alignment modules. 
the there are only one layer of organization regarding alignemnt, each serves a single purpose.
The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
when the choice is a type of alignment process, the process would be handed over to the AlignmentFcltr by the 
ProcessesFcltr, and this AlignmentFcltr would then generate configuration panels based on the parameters of choice.

here is a list of alignment modules that would be required for DaXi microscope:
1. set static voltages for all galvos.
2. align SG starting/ending position to the center of the field of view.
2. conjugate O1 and O2
3. align O3 at oblique plane detection
4. autofocus (scan light sheet, scan objective, calculate refocus, etc.)
5. center the embryo: first perform 1 full scan, and move the stage to make sure the embryo is centered in the FOV of the 
acquisition.

### 3. CalibrationFcltr
The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
when the choice is a type of calibration process, the process would be handed over to this CalibrationFcltr by the 
ProcessesFcltr, and this CalibrationFcltr would then generate configuration panels based on the parameters of choice.

Here is a list of calibration modules that would be required for DaXi microscope:
1. scanning galvo voltage/distance calibration
2. magnification calibration at co-axial detection
3. pixel size calibration at oblique plane detection
4. water pump calibration
5. temperature control calibration

### 4. InspectionFcltr
The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
when the choice is a type of inspection process, the process would be handed over to this InspectionFcltr by the 
ProcessesFcltr, and this InspectionFcltr would then generate configuration panels based on the parameters of choice.

1. inspect proper scanning of all galvos.
2. inspect proper switch of all lasers
3. inspect proper scanning and control of the ASI stage
4. inspect proper coordinated control of the ASI stage scanning and SG scanning
5. inspect proper control of the Hamamatsu camera - synchronization for each frame
6. inspect proper data output of the Hamamatsu camera (data gets saved at various of different acquisition rates, where is the limit)

### 5. NavigationFcltr
The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
when the choice is a type of navigation process, the process would be handed over to this NavigationFcltr by the 
ProcessesFcltr, and this NavigationFcltr would then generate configuration panels based on the parameters of choice.

1. move the sample around with free run camera
2. move the sample around with free run lightsheet scan
3. open floor - may add some real time analysis to the processes, make it open.

### 6. SystemFcltr
The system facilitator will take the user input parameters, suggest additional options, and allow the user to choose
a set of parameters.
SystemFcltr interfaces with the ProcessesFcltr, which then relay the processes to the corresponding focused-processes 
facilitators.

1. scripting tool
2. manage highest level GUI (all buttons and displays)
3. manage loading and exporting existing processes.
4. mip display 
5. based on user input parameters, suggest options of the pre-configured acquisition parameteres
for example, set sample range, pixel size, display options of different combinations of:
N, tE+tR, Vs

for each combination, display the time resolution, and axial resolution.                                                     
