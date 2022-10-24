from daxi.ctr_processesfacilitator.system.tools.acquisition_parameter_suggestion import AcqParamToolsMode5
import pprint

# Prints the nicely formatted dictionary
m = AcqParamToolsMode5(dx=0.4,
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

m.adapt()

m.find_parameter_combinations()

m.display_parameter_options()

m.get_parameter_combination(magnification_factor=5)
print("")
print("----------------------------------------------------------")
print("the selected parameter combination is shown below:")
pprint.pprint(m.selected_parameters)

m.selected_parameters
