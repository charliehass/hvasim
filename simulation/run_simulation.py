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
Testing out the HVA simulation.
* trying to find a model run that shows facil=low mod rates
* and depress=high mod rates
* making very long model runs to accomodate very slow mod_rates
* adding a control neuron group that has no plasticity
"""

########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path = "/Users/charliehass/Box Sync/Syncd Lab Stuff/hva_sim_data"
# dat_path = "/home/charlie/Desktop/hva_sim_data"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path)
