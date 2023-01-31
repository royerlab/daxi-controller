from daxi.control.process.facilitator.system.tools.acquisition_parameter_suggestion \
    import AcqParamMode7
import pprint

def demo_acquisition_params_mode7():
    # Prints the nicely formatted dictionary
    m = AcqParamMode7(dx=0.4,
                      length=1000,
                      t_exposure=90,
                      t_readout=10,
                      t_stage_retraction=23,  # retraction time for the stage after a stack acquisition is done.
                      number_of_colors_per_slice=1,
                      colors=['488', '561'],
                      slice_color_list=None,
                      views=['1', '2'],
                      positions_views_list=None,
                      positions={'position name 1': {'x': 1, 'y': 10}, 'position name 2': {'x': 23, 'y': 12}},
                      number_of_time_points=2,
                      )

    m.adapt()

    m.find_parameter_combinations_o1scan()

    m.display_parameter_options()

    m.get_parameter_combination(magnification_factor=5)
    print("")
    print("----------------------------------------------------------")
    print("the selected parameter combination is shown below:")
    pprint.pprint(m.selected_parameters)
    return m


if __name__ == "__main__":
    demo_acquisition_params_mode7()

