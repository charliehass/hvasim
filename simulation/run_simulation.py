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
import settings_test_stp as sim_settings


######################################
# USER-DEFINE: ENTER A  DESCRIPTION  #
######################################
description = """
Test: relationship b/w peak firing rates and TF filtering
* peak rate set to 50 Hz
* passive props and W_e identical for HVA neurons
* STP dynamic variable as fit from CH's data (6/12/2017)
"""

########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path_mac = "/Users/charliehass/Dropbox/Duke on Dropbox/hva_sim_data"
dat_path_linux = "/home/charlie/Desktop/hva_sim_data"
dat_path_nuke = "C:\\Users\charlie\\Desktop\\hva_sim_data"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path_nuke)
