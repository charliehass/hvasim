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
import settings_test_stp_with_real_params as sim_settings


######################################
# USER-DEFINE: ENTER A  DESCRIPTION  #
######################################
description = """
Testing out the HVA simulation.
* Re-testing the STP with params that came from the fit of the average
  data. Average across all cells.
"""

########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path = "/Users/charliehass/Dropbox/Duke on Dropbox/hva_sim_data"
# dat_path = "/home/charlie/Desktop/hva_sim_data"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path)
