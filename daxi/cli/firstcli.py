import click
from daxi.control.device.facilitator.devicesfacilitator import DevicesFcltr
from daxi.control.process.facilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.control.process.facilitator.processes_facilitator import load_process_configs
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_configs_yaml_path
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected

"""
eventually, would want to run the command line as:
>>> daxi -c [configs file path] to perform a process pre-defined in a configuration file.

but now, implement in a simple way just so we can use it.
python cli/firstcli.py -c [path-to-configs] 
# todo figure out how to do the following later.
"""


class CliInvoker:
    """
    this is the invoker type in the command pattern.
    perhaps for the sake of symmetry, we can also have GuiInvoker, or other invokers.
    """

    def __init__(self):
        """
        history: command line interface history
        """
        self.history = []
        self.process = None

    def add_process(self, process):
        """
        :param process: in DaXi controller, the command object here should be a focused process facilitator. the cli
        should act as if it is a general process facilitator that composes and logs the actions for a specific
        process. - assemble the team, and hand over the tasks.
        :return:
        """
        self.history.append(process)
        self.process = process
        assert self.process is not None

    def execute_process(self, device_fcltr, process_configs):
        """ this will execute the command with the configurations specified in configs """
        self.process.execute(devices_fcltr=device_fcltr,  # device facilitator here is the receiver
                             process_configs=process_configs)
                             # and process_configs is the data that specifies the command action.
        # the focused process facilitators all should have an execute method. develop the abstraction
        # when many focused process facilitators are implemented.


@click.command()
@click.option('--configs_path', '-c', prompt='the full path of the configuration file. For template, it should be\n'
              + process_configs_yaml_path,
              help='please type in the full path of the process configuration fil, it should be\n'
                   + process_configs_yaml_path
              )
def acquire(configs_path):
    """
    familiarize with with "command pattern" before you re-start implementing this module.
    the client organizes the command, the receiver and the data. It gets the data, choose the appropriate command and
    asks it to "execute". the command would take the data, and execute by driving the specific receivers.

    ** Regarding client:
    this acquire() acts like a client, it may serve the purpose of a ProcessFcltr (general purpose process fcltr).
    It loads the configs that acts as data, and perform the acquisition (concrete command), which serves the purpose
    of focused facilitators.
     - side note - will do abstraction for FocusedFcltr in the future when more focused facilitators are implemented.

    ** Regarding data:
    it is the configurations, specified in the configs_path file.
    configs_path should be a yaml file, that has the configurations.
    it will tell you the process type, the process configurations, and the device configurations.
    Here we are implementing with mode1 acquisition as a starting point. the process configurations would contain
    acquisition parameters (likewise, there should be calibration parameters, alignment parameters,
    inspection parameters, etc.), and device parameters. (16 pieces of physical and virtual devices).
    This data would be passed to the receiver by the command upon request by the client, and the receiver will
    translate and populate the specific configurations upon "receive configurations". the "receive configurations"
    method should produce something identical to the method to load the configurations.

    These configurations should be pared with the device_configs_core (when generate I guess?), as well as the alignment
    and calibration records. configuration should not generate data, it should only store the configurations. unless the
    data gets changed. but it should be reproducible with version control. - maybe save the numpy array later.
    it should contain information enough for the client to know which focused process facilitator to use
    it should contain all the specific acquisition parameter that is suggeste and chose from the SystemFcltr.
    it should also contain the specific information for the command to handle all the receiveres. but this is specific for
    some titles for the process.

    ** Regarding receiver:
    The receiver is the DevicesFcltr - that contains the composition of all physical devices of a daxi microscope,
    and drives the devices for one type of daq cycle. (change of daq cycle data should be done at the concrete command
    level, (not the client level) - the focused processes fcltrs, and it drives the methods in the DevicesFcltr to
    start, stop, re-write data, etc, and specifically controls the devices by calling th emethods offered by the
    DevicesFcltr. The focused processes fcltrs also drives the focused data fcltrs through the general data facilitator
    type. the implementation of all device fcltrs are currently on hold (need to use dexp and napari)

    ** Regarding command:
    process fcltr (like a client in command pattern), will look at the chosen process,
    and ask general purpose DevicesFcltr and DataFcltr to provide
    suitable focused fcltrs (like concrete commands), each of which would access their receivers to
    perform specific process tasks.

    what a client do:
    receiver = Receiver()
    cmd = CommandImplementation(receiver)  the command takes a receiver upon initiation
    invoker = Invoker()
    invoker.command(cmd) , with the data.
    invoker.execute() the invoker tells the command to execute

    it seems like the command, object composition, and aggregation patterns all fit well here (probably...)

    check out the following pattern and implement the structure:
    https://www.geeksforgeeks.org/command-method-python-design-patterns/


    """
    print('will perform acquisition specified in' + configs_path)
    # get the configuration files (that specifies the execution of the process). it is the data that will be delivered
    # to the receiver through the command (this is the data)
    configs = load_process_configs(path=configs_path)

    # create a DevicesFcltr (this is the receiver)
    device_fcltr = DevicesFcltr(devices_connected=devices_connected)

    # create the AcquisitionFcltr that takes the DevicesFcltr (this is the command)
    acquisition = AcquisitionFcltr()  # in this case the command is not aware of the receiver,
    # but instead the receiver would be passed to the command by the invoker.
    # this is the command object. it does not create or destroy the device_fcltr,

    # create an invoker
    invoker = CliInvoker()

    # it only access the device_fcltr. destroying
    # acquisition do not destroy the device_fcltr instances.
    invoker.add_process(process=acquisition)  # log the process after execute.
    # now the invoker invokes the command (process) with specification stored in the data (process_configs).
    invoker.execute_process(device_fcltr=device_fcltr, process_configs=configs)

    # invoker takes a concrete command that takes a receiver with it, it invokes the method of a receiver through the
    # execute() method in the concrete command.
    # the invoker also logs this execution.


if __name__ == '__main__':
    acquire()
