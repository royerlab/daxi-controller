import numpy
from bokeh.palettes import Category20
from bokeh.plotting import figure, show
from bokeh.models import Legend

from daxi.control.device.facilitator.config_tools.configuration_generator_base import NIDAQDevicesConfigsGeneratorBase


def _get_display_msgs(n_slices_per_stack,
                      metro_freq,
                      t_expo,
                      t_readout,
                      expo_tick_n,
                      readout_tick_n):
    """
    this function generate a list of display messages in the plot, convenient to check.
    @param n_slices_per_stack:
    @param metro_freq:
    @param t_expo:
    @param expo_tick_n:
    @param t_readout:
    @param readout_tick_n:
    @return:
    """
    msgs = ['Number of frames per stack: ' + str(n_slices_per_stack),
            'Metronome frequency: ' + str(metro_freq) + ' Hz',
            'Exposure time: ' + str(t_expo) + ' ms, ' + str(expo_tick_n) + ' ticks',
            'Readout time: ' + str(t_readout) + ' ms' + str(readout_tick_n) + ' ticks',
            'Number of sample ticks per frame: ' + str(expo_tick_n + readout_tick_n),
            ]
    return msgs


def plot_daq_voltage_profiles(configs: NIDAQDevicesConfigsGeneratorBase = None,
                              data_points_to_show=10000,
                              msgs=None):
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

    if msgs is None:
        msgs = _get_display_msgs(n_slices_per_stack,
                                 metro_freq,
                                 t_expo,
                                 t_readout,
                                 expo_tick_n,
                                 readout_tick_n)

    # show number of frames per stack
    # show metronome frequency, exposure time and readout time.

    legends = []
    lines = []
    print(type(configs))

    # plot exposure-readout ticks
    expo_readout_profile = ([0.5] * int(expo_tick_n) + [-0.5] * int(readout_tick_n)) * int(n_slices_per_stack)
    lines.append(expo_readout_profile[:data_points_to_show])
    legends.append('exposure(0.5) and readout(-0.5) profile')

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

    # plot beta galvo for light sheet incident angle:
    if 'data for view 1' in configs.configs_beta_galvo_light_sheet_incident_angle.keys():
        lines.append(configs.configs_beta_galvo_light_sheet_incident_angle['data for view 1'][:data_points_to_show])
        legends.append('beta galvo, lightsheet incident angle, view 1')

    if 'data for view 2' in configs.configs_beta_galvo_light_sheet_incident_angle.keys():
        lines.append(configs.configs_beta_galvo_light_sheet_incident_angle['data for view 2'][:data_points_to_show])
        legends.append('beta galvo, lightsheet incident angle, view 2')

    # plot the profile for O1
    if 'data for view 1' in configs.configs_o1.keys():
        lines.append(numpy.asarray(configs.configs_o1['data for view 1'][:data_points_to_show]) + 0.3)
        legends.append('O1, view 1')

    if 'data for view 2' in configs.configs_o1.keys():
        lines.append(numpy.asarray(configs.configs_o1['data for view 2'][:data_points_to_show]) + 0.3)
        legends.append('O1, view 2')

    # plot the profile for O3:
    if 'data for view 1' in configs.configs_o3.keys():
        lines.append(configs.configs_o3['data for view 1'][:data_points_to_show])
        legends.append('O3, view 1')

    if 'data for view 2' in configs.configs_o3.keys():
        lines.append(configs.configs_o3['data for view 2'][:data_points_to_show])
        legends.append('O3, view 2')

    # plot the profile for 405 laser when the channel is operating
    if 'data' in configs.configs_405_laser.keys():
        lines.append(numpy.asarray(configs.configs_405_laser['data'][:data_points_to_show])+0.1)
        legends.append('405 laser when it is operating, offset + 0.1 on plot.')

    # plot the profile for 488 laser when the channel is operating
    if 'data' in configs.configs_488_laser.keys():
        lines.append(numpy.asarray(configs.configs_488_laser['data'][:data_points_to_show])+0.15)
        legends.append('488 laser when it is operating, offset + 0.15 on plot.')

    # plot the profile for 561 laser when the channel is operating
    if 'data' in configs.configs_561_laser.keys():
        lines.append(numpy.asarray(configs.configs_561_laser['data'][:data_points_to_show])+0.2)
        legends.append('561 laser when it is operating, offset + 0.2 on plot.')

    # plot the profile for 639 laser when the channel is operating
    if 'data' in configs.configs_639_laser.keys():
        lines.append(numpy.asarray(configs.configs_639_laser['data'][:data_points_to_show])+0.25)
        legends.append('639 laser when it is operating, offset + 0.25 on plot.')

    # plot the profile for bright field LED when the channel is operating
    if 'data' in configs.configs_bright_field.keys():
        lines.append(numpy.asarray(configs.configs_bright_field['data'][:data_points_to_show])+0.3)
        legends.append('bright field LED when it is operating, offset + 0.3 on plot.')

    colors_list = Category20[20][:len(legends)]
    p = figure(width=1500, height=700)
    legend_it = []
    # configure the line plots
    for (colr, leg, line_data) in zip(colors_list, legends, lines):
        # c = p.line(numpy.arange(len(line_data)), line_data, color=colr, legend_label=leg, line_width=2)
        c = p.line(numpy.arange(len(line_data)), line_data, line_width=2, color=colr, alpha=0.9,
                   muted_color=colr, muted_alpha=0.01)
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


def plot_daq_voltage_profiles_single_cycle_dict(configs_dict:dict,
                                                data_points_to_show=10000,
                                                dict_key='Whats the single cycle Key?',
                                                process_configs=None):

    metro_freq = configs_dict['configs_metronome']['frequency']
    t_expo = process_configs['process configs']['acquisition parameters']['exposure time (ms)']
    expo_tick_n = t_expo / 1000 * metro_freq
    t_readout = process_configs['process configs']['acquisition parameters']['camera read out time (ms)']
    readout_tick_n = t_readout / 1000 * metro_freq
    n_slices_per_stack = process_configs['process configs']['acquisition parameters']['n slices']
    msgs = _get_display_msgs(n_slices_per_stack,
                             metro_freq,
                             t_expo,
                             t_readout,
                             expo_tick_n,
                             readout_tick_n)
    msgs.append('single cycle key: ' + dict_key)
    legends = []
    lines = []

    # plot exposure-readout ticks
    expo_readout_profile = ([0.5] * int(expo_tick_n) + [-0.5] * int(readout_tick_n)) * int(n_slices_per_stack)
    lines.append(expo_readout_profile[:data_points_to_show])
    legends.append('exposure(0.5) and readout(-0.5) profile')

    # plot scanning galvo profiles
    if 'data' in configs_dict['configs_scanning_galvo'].keys():
        lines.append(configs_dict['configs_scanning_galvo']['data'][:data_points_to_show])
        legends.append('SG')

    # plot switching galvo 1 and 2 profiles
    if 'data' in configs_dict['configs_view_switching_galvo_1'].keys():
        lines.append(configs_dict['configs_view_switching_galvo_1']['data'][:data_points_to_show])
        legends.append('VSG-1')

    if 'data' in configs_dict['configs_view_switching_galvo_2'].keys():
        lines.append(configs_dict['configs_view_switching_galvo_2']['data'][:data_points_to_show])
        legends.append('VSG-2')

    # plot gamma galvo strip reduction profile
    if 'data' in configs_dict['configs_gamma_galvo_strip_reduction'].keys():
        lines.append(configs_dict['configs_gamma_galvo_strip_reduction']['data'][:data_points_to_show])
        legends.append('gamma galvo strip reduction')

    # plot beta galvo for light sheet incident angle:
    if 'data' in configs_dict['configs_beta_galvo_light_sheet_incident_angle'].keys():
        lines.append(configs_dict['configs_beta_galvo_light_sheet_incident_angle']['data'][:data_points_to_show])
        legends.append('beta galvo, lightsheet incident angle')

    # plot the profile for O1
    if 'data' in configs_dict['configs_O1'].keys():
        lines.append(configs_dict['configs_O1']['data'][:data_points_to_show])
        legends.append('O1')

    # plot the profile for O3:
    if 'data' in configs_dict['configs_O3'].keys():
        lines.append(configs_dict['configs_O3']['data'][:data_points_to_show])
        legends.append('O3')

    # plot the profile for 405 laser when the channel is operating
    if 'data' in configs_dict['configs_405_laser'].keys():
        lines.append(numpy.asarray(configs_dict['configs_405_laser']['data'][:data_points_to_show])+0.1)
        legends.append('405 laser, offset + 0.1 on plot')

    # plot the profile for 488 laser when the channel is operating
    if 'data' in configs_dict['configs_488_laser'].keys():
        lines.append(numpy.asarray(configs_dict['configs_488_laser']['data'][:data_points_to_show])+0.15)
        legends.append('488 laser, offset + 0.15 on plot')

    # plot the profile for 561 laser when the channel is operating
    if 'data' in configs_dict['configs_561_laser'].keys():
        lines.append(numpy.asarray(configs_dict['configs_561_laser']['data'][:data_points_to_show])+0.2)
        legends.append('561 laser, offset + 0.2 on plot')

    # plot the profile for 639 laser when the channel is operating
    if 'data' in configs_dict['configs_639_laser'].keys():
        lines.append(numpy.asarray(configs_dict['configs_639_laser']['data'][:data_points_to_show])+0.25)
        legends.append('639 laser, offset + 0.25 on plot')

    # plot the profile for bright field LED when the channel is operating
    if 'data' in configs_dict['configs_bright_field'].keys():
        lines.append(numpy.asarray(configs_dict['configs_bright_field']['data'][:data_points_to_show])+0.3)
        legends.append('bright field LED, offset + 0.3 on plot')

    colors_list = Category20[20][:len(legends)]
    p = figure(width=1500, height=700)
    legend_it = []
    # configure the line plots
    for (colr, leg, line_data) in zip(colors_list, legends, lines):
        # c = p.line(numpy.arange(len(line_data)), line_data, color=colr, legend_label=leg, line_width=2)
        c = p.line(numpy.arange(len(line_data)), line_data, line_width=2, color=colr, alpha=0.9,
                   muted_color=colr, muted_alpha=0.01)
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
