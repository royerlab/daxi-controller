from daxi.ctr_processesfacilitator.system.tools.acquisition_parameter_suggestion import AcqParamToolsBase
import pprint

# Prints the nicely formatted dictionary
m = AcqParamToolsBase(dx=0.4,
                      length=1000,
                      t_exposure=90,
                      t_readout=10)

m.find_parameter_combinations()

m.display_parameter_options()

m.get_parameter_combination(magnification_factor=5)
print("")
print("----------------------------------------------------------")
print("the selected parameter combination is shown below:")
pprint.pprint(m.selected_parameters)
