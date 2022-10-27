import click
from daxi.ctr_processesfacilitator.acquisition.acquisition_facilitator import AcquisitionFcltr
from daxi.ctr_devicesfacilitator.devicefacilitator import DevicesFcltr
#todo figure out how to do the following later.
"""
eventually, would want to run the command line as:
>>> daxi -c [configs file path] to perform a process pre-defined in a configuration file.

but now, implement in a simple way just so we can use it.
python cli/firstcli.py -c [path-to-configs] 

"""

@click.command()
@click.option('--process', '-p', default='rconfigs', help='choose "rconfigs" to run from configuration file')
@click.option('--configs_path', '-c', prompt='the full path of the configuration file',
              help='input the full path of the process configuration file')

class CliInvoker():
    """
    this is the invoker type in the command pattern.
    perhaps for the sake of symmetry, we can also have GuiInvoker, or ther invokers.
    """
    def __init__(self):
        """
        history: command line interface history
        """
        self.history = []

    def invoke(self, command):
        """

        :param command: in DaXi controller, the command object here should be a focused process facilitator. the cli
        should act as if it is a general process facilitator that composes and logs the actions for a specific
        process. - assemble the team, and hand over the tasks.
        :return:
        """
        self.history.append(command)
        command.execute() # the focused process facilitators alls hould have an execute method. develop the abstraction
        # when many focused process facilitators are implemented.


def acquire(process_type, configs_path):
    """
    this acquire() acts like a client in the "command pattern", it may serve the purpose of a ProcessFcltr

    it loads the configs that acts as data, and perform the acquisition (concrete command), which serves the purpose
    of focused facilitators.
    will do abstraction for FocusedFcltr in the future when more focused facilitators are implemented.

    The receiver is the DevicesFcltr - that contains the composition of all physical devices of a daxi microscope,
    and drives the deives for one type of daq cycle. (change of daq cycle data should be done at the concrete command level,
    (not the client level) - the focused processes fcltrs, and it drives the methods in the DevicesFcltr to start, stop,
     re-write data, etc, and specifically controls the devices by calling th emethods offered by the DevicesFcltr.
     The focused processes fcltrs also drives the focused data fcltrs through the general data facilitator type.
    the implementation of all device fcltrs are currently on hold (need to use dexp and napari)

    process fcltr (like a client in command pattern), will look at the chosen process,
    and ask general purpose DevicesFcltr and DataFcltr to provide
    suitable focused fcltrs (like concrete commands), each of which would access their receivers to
    perform specific process tasks.

    it seems like the command, object composition, and aggregation patterns all fit well here (probably...)
    """
    # receiver
    device_fcltr = DeviceFcltr() # this is the receiver object
    configs = get_configs(configs_path) # this is the data that is delivered to the receiver through the command.
    acquisition = AcquisitionFcltr() # this is the command object. it does not create nor destroy the device_fcltr, it only access the device_fcltr. destroying
    # acquisition do not destroy the device_fcltr instances.

    invoker.invoke(concrete_command=acquisition(receiver=device_fcltr, data=configs))

    # invoker takes a concrete command that takes a receiver with it, it invokes the method of a receiver through the
    # execute() method in the concrete command.
    # the invoker also logs this execution.

if __name__ == '__main__':
    acquire()