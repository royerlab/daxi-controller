import platform

VERBOSE = True
debug_mode = True
devices_connected = True  # todo change this into the platform.system() string for windows machine later.
if platform.system() == 'Darwin':
    devices_connected = False

development_mode = True
sphinx_build = False
long_test = False
