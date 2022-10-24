import nidaqmx
import nidaqmx.system
import numpy as np
import time

# create a task to set a device to "go home", meaning the neutral position with everything centered.
def gohome(params):
    if params['verbose']:
        print('Now setting ['+params['controlled device name']+'] to the '+
              'home position [voltage = '+str(params['home voltage'])+'v] with ' +
              '[offset = '+str(params['home offset voltage'])+'v,'+str(params['home offset option'])+'] '+
              'through channel [\''+params['channel_string']+'\']')
    if params['channel I/O type'] == "AO":
        task = nidaqmx.Task(params['controlled device name'] )
        task.ao_channels.add_ao_voltage_chan(params['channel_string'])
        params['task']=task
        time.sleep(1)  # for manual inspection to make sure it took action.
        try:
            if params['home offset option'] is True:
                value = params['home voltage'] + params['home offset voltage']
            else:
                value = params['home voltage']

            task.write(value,auto_start=True)
            if params['verbose']: print('Task perfromed successfully.')
        except:
            if params['verbose']: print('Failed performing the task.')
        task.close()
    else:
        if params['verbose']: print('only DAQ AO channel is supported currently')
    if params['verbose']:
        print('Task closed.')


def gohome_all(paramslist):
    # create an AO task
    task = nidaqmx.Task()
    values = []
    # go through allt he pramslist and (1) add AO channels and (2) prepare write values list.
    for params in paramslist:
        if params['verbose']:
            print('Now setting [' + params['controlled device name'] + '] to the ' +
                  'home position [voltage = ' + str(params['home voltage']) + 'v] with ' +
                  '[offset = ' + str(params['home offset voltage']) + 'v,' + str(params['home offset option']) + '] ' +
                  'through channel [\'' + params['channel_string'] + '\']')

        # add all the AO channels to the AO tasks
        if params['channel I/O type'] == "AO":
            task.ao_channels.add_ao_voltage_chan(params['channel_string'])
            params['task'] = task

            # generate the value for this AO channel
            try:
                if params['home offset option'] is True:
                    value = params['home voltage'] + params['home offset voltage']
                else:
                    value = params['home voltage']

                # append the value to the value list
                values.append(value)
                if params['verbose']: print('Task performed successfully.')
            except:
                if params['verbose']: print('Failed performing the task.')

        else:
            if params['verbose']: print('only DAQ AO channel is supported currently')

    task.write(values, auto_start=True)
    return task