#!/bin/bash
# keep in mind that these are demos for command line interface, so the demo codes are implemented in the form of shell
# scripts. Here we are using bash. But since we need to make daxi path universal...

# first, make sure you are in the daxi path. (change the daxi path to your actual daxi folder path)
pdaxi="/Users/xiyu.yi/Desktop/Research/Projects/P-daxi-protocol/daxi-controller/daxi"
# define the path for the template file for acquisition process for testing purposes  (keep in mind this test shall
# always be contained inside this folder.. may need to write a test for this) # todo - write a test to ensure this one.

# goto daxi path
cd $pdaxi

# specify the template process configuration file path

# run the command line to execute the specified process
python cli/firstcli.py -c ./globals_configs_constants_general_tools_needbettername/configuration_templates/process_templates/template_acquisition_mode1-dev.yaml
