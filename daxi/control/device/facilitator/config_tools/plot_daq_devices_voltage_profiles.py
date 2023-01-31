import numpy
from bokeh.palettes import Category20
from bokeh.plotting import figure, show
from bokeh.models import Legend

from daxi.control.device.facilitator.config_tools.configuration_generator_base import NIDAQDevicesConfigsGeneratorBase


def plot_daq_voltage_profiles(configs: NIDAQDevicesConfigsGeneratorBase = None, data_points_to_show=10000):
    """
    This function will take in a finished data generator class, find all the available daq card data profiles,
    and plot them together for inspection purposes.

    @param data_points_to_show:
    @param configs:
    @return:
    """
    """
    display number of samples of the metronome
    metronome frequency
    time axis
    exposure/readout cycles marks.


    """
    metro_freq = configs.configs_metronome['frequency']
    t_expo = configs.process_configs['process configs']['acquisition parameters']['exposure time (ms)']
    expo_tick_n = t_expo / 1000 * metro_freq
    t_readout = configs.process_configs['process configs']['acquisition parameters']['camera read out time (ms)']
    readout_tick_n = t_readout / 1000 * metro_freq
    n_slices_per_stack = configs.process_configs['process configs']['acquisition parameters']['n slices']

    msgs = ['Number of frames per stack: ' + str(n_slices_per_stack),
            'Metronome frequency: ' + str(metro_freq) + ' Hz',
            'Exposure time: ' + str(t_expo) + ' ms, ' + str(expo_tick_n) + ' ticks',
            'Readout time: ' + str(t_readout) + ' ms' + str(readout_tick_n) + ' ticks'
            ]

    # show number of frames per stack
    # show metronome frequency, exposure time and readout time.

    legends = []
    lines = []
    print(type(configs))

    # plot exposure-readout ticks
    expo_readout_profile = ([1] * int(expo_tick_n) + [-1] * int(readout_tick_n)) * int(n_slices_per_stack)
    lines.append(expo_readout_profile[:data_points_to_show])
    legends.append('exposure(1) and readout(-1) profile')

    # plot scanning galvo profiles
    if 'data for view 1' in configs.configs_scanning_galvo.keys():
        lines.append(configs.configs_scanning_galvo['data for view 1'][:data_points_to_show])
        legends.append('SG view 1')

    if 'data for view 2' in configs.configs_scanning_galvo.keys():
        lines.append(configs.configs_scanning_galvo['data for view 2'][:data_points_to_show])
        legends.append('SG view 2')

    # plot switching galvo 1 and 2 profiles
    if 'data for view 1' in configs.configs_view_switching_galvo_1.keys():
        lines.append(configs.configs_view_switching_galvo_1['data for view 1'][:data_points_to_show])
        legends.append('VSG-1 view 1')

    if 'data for view 2' in configs.configs_view_switching_galvo_1.keys():
        lines.append(configs.configs_view_switching_galvo_1['data for view 2'][:data_points_to_show])
        legends.append('VSG-1 view 2')

    if 'data for view 1' in configs.configs_view_switching_galvo_2.keys():
        lines.append(configs.configs_view_switching_galvo_2['data for view 1'][:data_points_to_show])
        legends.append('VSG-2 view 1')

    if 'data for view 2' in configs.configs_view_switching_galvo_2.keys():
        lines.append(configs.configs_view_switching_galvo_2['data for view 2'][:data_points_to_show])
        legends.append('VSG-2 view 2')

    # plot gamma galvo strip reduction profile
    if 'data for view 1' in configs.configs_gamma_galvo_strip_reduction.keys():
        lines.append(configs.configs_gamma_galvo_strip_reduction['data for view 1'][:data_points_to_show])
        legends.append('gamma galvo strip reduction, view 1')

    if 'data for view 2' in configs.configs_gamma_galvo_strip_reduction.keys():
        lines.append(configs.configs_gamma_galvo_strip_reduction['data for view 2'][:data_points_to_show])
        legends.append('gamma galvo strip reduction, view 2')

    colors_list = Category20[20][:len(legends)]
    p = figure(width=1500, height=700)
    legend_it = []
    # configure the line plots
    for (colr, leg, line_data) in zip(colors_list, legends, lines):
        # c = p.line(numpy.arange(len(line_data)), line_data, color=colr, legend_label=leg, line_width=2)
        c = p.line(numpy.arange(len(line_data)), line_data, line_width=2, color=colr, alpha=0.9,
                   muted_color=colr, muted_alpha=0.1)
        legend_it.append((leg, [c]))

    # add texts to be displayed in the legend box
    for msg in msgs:
        # c = p.line(numpy.arange(len(line_data)), line_data, color=colr, legend_label=leg, line_width=2)
        c = p.line([0], [0], line_width=0.2, color='white', alpha=0.8,
                   muted_color='white', muted_alpha=0.2)
        legend_it.append((msg, [c]))

    legend = Legend(items=legend_it)
    legend.click_policy = "mute"
    p.add_layout(legend, 'right')
    show(p)
