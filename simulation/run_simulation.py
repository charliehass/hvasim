"""
Wrapper function for easy simulation setup.

1) Define the settings module
2) Enter a description
3) Specify the path to the directory where the data should be saved
4) Call "python3 run_simulation.py" from terminal

"""

###################################
# IMPORT THE NECESSARY MODULES    #
###################################
from hvasim import run_simulations


#######################################
# USER-DEFINE: THE SIMULATION SETTINGS
# import YYYYYY as sim_settings (YYYYY = sim_settings module name)
import settings_sim_for_allen as sim_settings


######################################
# USER-DEFINE: ENTER A  DESCRIPTION  #
######################################
description = """
Test: new passive props
* sinusoidal inputs (peak rate = 50Hz)
* using passive props for PY, FS, SOM cells
* using empirical tau_epsc
* using membrane eq that incorporates the Rin
* spiking output from FS and SOM cells with possibly realistic pA EPSCs
* adjusted the SOM scalefact down and the PV scalefact up (now 5x)
* using roughly empirical STP for SOM and PV+ cells
"""

########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path_mac = "/Users/charliehass/Box Sync/Syncd Lab Stuff/hva_sim_data"
dat_path_nuke = "C:\\Users\charlie\\Desktop\\hva_sim_data"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path_mac)
