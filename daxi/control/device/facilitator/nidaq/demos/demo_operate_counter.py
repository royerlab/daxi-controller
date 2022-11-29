# this demo acts like a device facilitator and configs/controls a counter

# prepare counter
# get configuration for the ao task bundle
import datetime
from time import sleep

from daxi.ctr_devicesfacilitator.nidaq.nidaq import Counter
from daxi.globals_configs_constants_general_tools_needbettername.constants import virtual_tools_configs_path
from daxi.globals_configs_constants_general_tools_needbettername.parser import NIDAQConfigsParser

p = NIDAQConfigsParser()
p.set_configs_path(virtual_tools_configs_path)
section = 'Virtual Tools Section'
keyword = 'counter'
configs = \
    p.get_configs_by_path_section_keyword(section, keyword)

# prepare a counter
counter = Counter()
counter.set_configurations(counter_configs=configs)

# counter get ready
counter.get_ready()

# counter start
counter.start()

# test counter of counting
frame_number_pre = 0
frame_number = 0

counting = True
while counting:
    while frame_number == frame_number_pre:
        frame_number = counter.read()
        sleep(0.001)
    current_time = datetime.datetime.now()
    print('frame number is ' + str(frame_number) + ', curren time is ' + str(current_time))
    frame_number_pre = frame_number
    if frame_number_pre > 100:
        counting = False

# stop counter
counter.stop()

# close counter
counter.close()
