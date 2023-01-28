from daxi.control.process.facilitator.system.tools.acquisition_parameter_suggestion import \
    AcqParamBase, AcqParamMode1, AcqParamMode2, \
    AcqParamMode3, AcqParamMode4, AcqParamMode5, AcqParamMode6


def test_acq_param_suggestion_init():
    m = AcqParamBase()
    assert hasattr(m, 'dx')
    assert hasattr(m, 'length')
    assert hasattr(m, 't_exposure')
    assert hasattr(m, 't_readout')
    assert hasattr(m, 't_stage_retraction')
    assert hasattr(m, 'ns')
    assert hasattr(m, 'ys_list')
    assert hasattr(m, 'vs_list')
    assert hasattr(m, 'n_slices_list')
    assert hasattr(m, 'stack_time_list')
    assert hasattr(m, 'length_updated_list')
    assert hasattr(m, 'selected_parameters')


def test_find_parameter_combinations():
    m = AcqParamBase(dx=0.4,
                     length=1000,
                     t_exposure=90,
                     t_readout=10,
                     number_of_colors_per_slice=1,
                     t_stage_retraction=0.01,
                     number_of_scans_per_timepoint=1,
                     scanning_galvo_range_limit=0.1)
    m.find_parameter_combinations_ls3scan()
    assert m.ns is not None
    assert m.ys_list is not None
    assert m.vs_list is not None
    assert m.n_slices_list is not None
    assert m.stack_time_list is not None
    assert m.length_updated_list is not None
    assert m.scanning_galvo_range_per_slice_list is not None
    assert m.scanning_galvo_range_limit is not None


def test_get_parameter_combination():
    m = AcqParamBase(dx=0.4,
                     length=1000,
                     t_exposure=90,
                     t_readout=10,
                     number_of_colors_per_slice=1,
                     t_stage_retraction=0.01,
                     number_of_scans_per_timepoint=1,
                     scanning_galvo_range_limit=0.1)

    m.get_parameter_combination(magnification_factor=5)
    assert "pixel size in xy (um)" in m.selected_parameters.keys()
    assert "mag-factor" in m.selected_parameters.keys()
    assert "slice distance (um)" in m.selected_parameters.keys()
    assert "n slices" in m.selected_parameters.keys()
    assert "time per stack per view (s)" in m.selected_parameters.keys()
    assert "time per time point (s)" in m.selected_parameters.keys()
    assert "scanning range (um)" in m.selected_parameters.keys()
    assert "galvo scanning speed (nm/ms)" in m.selected_parameters.keys()
    assert "stage scanning speed (nm/ms)" in m.selected_parameters.keys()
    assert "exposure time (ms)" in m.selected_parameters.keys()
    assert "camera read out time (ms)" in m.selected_parameters.keys()
    assert "stage retraction time (ms)" in m.selected_parameters.keys()
    assert "scanning galvo scan range per slice (um)" in m.selected_parameters.keys()
    assert "scanning galvo scan range limit (um)" in m.selected_parameters.keys()
    assert "name" in m.selected_parameters.keys()
    assert "type" in m.selected_parameters.keys()
    assert "looping order" in m.selected_parameters.keys()


def test_mode1to6_get_paramter_combination():
    # acquisition mode 1
    m1 = AcqParamMode1(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m1.adapt()
    m1.find_parameter_combinations_ls3scan()
    m1.get_parameter_combination(magnification_factor=5)
    assert abs(m1.selected_parameters['time per time point (s)'] - 141.692) < 0.001

    # acquisition mode 2
    m2 = AcqParamMode2(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m2.adapt()
    m2.find_parameter_combinations_ls3scan()
    m2.get_parameter_combination(magnification_factor=5)
    assert abs(m2.selected_parameters['time per time point (s)'] - 141.646) < 0.001

    # acquisition mode 3
    m3 = AcqParamMode3(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m3.adapt()
    m3.find_parameter_combinations_ls3scan()
    m3.get_parameter_combination(magnification_factor=5)
    assert abs(m3.selected_parameters['time per time point (s)'] - 70.846) < 0.001

    # acquisition mode 4
    m4 = AcqParamMode4(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m4.adapt()
    m4.find_parameter_combinations_ls3scan()
    m4.get_parameter_combination(magnification_factor=5)
    assert abs(m4.selected_parameters['time per time point (s)'] - 141.692) < 0.001

    # acquisition mode 5
    m5 = AcqParamMode5(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m5.adapt()
    m5.find_parameter_combinations_ls3scan()
    m5.get_parameter_combination(magnification_factor=5)
    assert abs(m5.selected_parameters['time per time point (s)'] - 141.646) < 0.001

    # acquisition mode 6
    m6 = AcqParamMode6(dx=0.4,
                       length=1000,
                       t_exposure=90,
                       t_readout=10,
                       t_stage_retraction=23,
                       scanning_galvo_range_limit=0.8,
                       number_of_colors_per_slice=1,
                       colors=['488', '561'],
                       number_of_scans_per_timepoint=1,
                       slice_color_list=None,
                       positions=None,
                       views=['1', '2'],
                       positions_views_list=None,
                       )
    m6.adapt()
    m6.find_parameter_combinations_ls3scan()
    m6.get_parameter_combination(magnification_factor=5)
    assert abs(m6.selected_parameters['time per time point (s)'] - 70.846) < 0.001
