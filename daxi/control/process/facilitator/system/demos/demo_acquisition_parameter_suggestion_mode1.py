from daxi.control.process.facilitator.system.tools.acquisition_parameter_suggestion import AcqParamMode1
import pprint

# Prints the nicely formatted dictionary
m = AcqParamMode1(dx=0.4,
                  length=1000,
                  t_exposure=90,
                  t_readout=10,
                  t_stage_retraction=23,
                  scanning_galvo_range_limit=0.8,
                  number_of_colors_per_slice=1,
                  colors=['488', '561'],
                  slice_color_list=None,
                  positions=None,
                  views=['1', '2'],
                  positions_views_list=None,
                  )

m.adapt()

m.find_parameter_combinations_ls3scan()

m.display_parameter_options()

m.get_parameter_combination(magnification_factor=5)
print("")
print("----------------------------------------------------------")
print("the selected parameter combination is shown below:")
pprint.pprint(m.selected_parameters)
