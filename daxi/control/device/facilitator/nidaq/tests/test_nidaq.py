# test_nidaq.py
import nidaqmx
import pytest
from time import sleep
import os
from daxi.control.device.facilitator.nidaq.nidaq import Metronome, TaskBundleAO, SubTaskAO
from daxi.control.device.facilitator.nidaq.counter import Counter
from daxi.control.device.facilitator.config_tools.generate_functions import DAQDataGenerator
from daxi.globals_configs_constants_general_tools_needbettername.python_globals import devices_connected
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser
from daxi.globals_configs_constants_general_tools_needbettername.constants import virtual_tools_configs_path


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_get_counter():
    # first, get the counter configuration file.
    p = NIDAQConfigsParser()
    p.set_configs_path(virtual_tools_configs_path)

    assert hasattr(p, 'configs_path')
    counter_configs = p.get_counter_configs()

    # create a counter
    counter = Counter()

    # populate the configurations to this Counter object:
    counter.set_configurations(counter_configs)

    # now ask the counter to get ready (initiate the daq CI task)
    counter.get_ready()
    assert hasattr(counter, 'task_handle')
    assert isinstance(counter.task_handle, nidaqmx.task.Task)

    # now start the counter
    counter.start()

    # now read the count from the counter
    c = counter.read()
    assert isinstance(c, int)
    assert c == counter.initial_count

    # now stop the counter
    counter.stop()

    # now close the counter
    counter.close()


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_get_metronome():
    # first, get the metronome configuration file (this step should be equivament to a manager action)
    p = NIDAQConfigsParser()
    p.set_configs_path(virtual_tools_configs_path)

    assert hasattr(p, 'configs_path')
    metronome_configs = p.get_metronome_configs()

    # create a metronome

    metronome = Metronome()
    # populate the configurations ot this metronome object:
    metronome.set_configurations(metronome_configs)

    # now ask the metronome to get ready (initiate the daq CO task)
    metronome.get_ready()
    assert hasattr(metronome, 'task_handle')  # make sure the nidaqmx task is initiated
    assert isinstance(metronome.task_handle, nidaqmx.task.Task)  # make sure it is a valid nidaqmx.task.Task.

    # now start the metronome
    metronome.start()

    # now stop the metronome
    metronome.stop()

    # now close the metronome
    metronome.close()


@pytest.mark.skipif(devices_connected is False, reason="This test requires daq cards to be connected.")
def test_get_oscilloscope_channel1():
    """
    We are fixing the actual list of physical devices for DaXi microscope.
    Here we have 3 testing channels, oscilloscope_channel1, oscilloscope_channel2, and oscilloscope_channel3.
    we should also have other devices.
    This test makes sure we can test the performance of the oscilloscope_channel1 based on the default configurations.

    Things we want to assert:
    1. configuration of this physical device is a dictionary, and has all the attributes (redundancy, keep)
    2. make sure the generation of sinusoidal wave is correct

    This test shall be performed without awareness of the facilitator, and it should display the actions of a
    facilitator
    :return:
    """
    # todo need to have a function generator module, it's associated tests and demos.
    # todo need to have AOTaskBundle testers, but dont use the TaskBundleAO here
    # also test the generator module here in this test.

    # 1. get subtask configurations, and AO bundle configuration
    configs_path = virtual_tools_configs_path
    assert os.path.isfile(configs_path)
    p1 = NIDAQConfigsParser()
    p1.set_configs_path(configs_path)
    assert os.path.isfile(p1.configs_path)
    configs = p1.get_oscilloscope1_configs()
    assert isinstance(configs, dict)

    # 2. prepare the subtask
    subtask = SubTaskAO(configs)
    # now we know this subtask data generator is sinusoidal
    dg = DAQDataGenerator()
    data_configs = configs['data configs']
    subtask.data = dg.getfcn_sinusoidal(amplitude=data_configs['amplitude'],
                                        center_voltage=data_configs['center voltage'],
                                        sample_number=data_configs['sample number'],
                                        initial_phase=data_configs['initial phase'],
                                        )

    # 3. get metronome for task bundle
    p2 = NIDAQConfigsParser()
    p2.set_configs_path(virtual_tools_configs_path)
    metronome_configs = p2.get_metronome_configs()
    metronome = Metronome()
    metronome.set_configurations(metronome_configs)
    metronome.get_ready()

    # 4. prepare AO task bundle
    # get task config
    p3 = NIDAQConfigsParser()
    p3.set_configs_path(virtual_tools_configs_path)
    section = 'Physical Devices Section'
    keyword = 'AO_task_bundle'
    task_bundle_ao_configs = \
        p3.get_configs_by_path_section_keyword(section, keyword)

    # prepare the object
    taskbundle_ao = TaskBundleAO()

    # set the ao task bundle configurations
    taskbundle_ao.set_configurations(task_bundle_ao_configs)

    # add metronome
    taskbundle_ao.add_metronome(metronome)

    # add sub-task
    taskbundle_ao.add_subtask(subtask)

    # configure sub-task data generator (this action would be organized into a manager class)
    # taskbundle_ao get ready
    taskbundle_ao.get_ready()

    # start
    metronome.start()
    taskbundle_ao.start()

    taskbundle_ao.stop()
    sleep(0.1)
    taskbundle_ao.start()
    sleep(0.1)
    taskbundle_ao.close()
    metronome.close()
