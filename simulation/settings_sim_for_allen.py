"""Settings for feedforward Network.

These settings are for a network of FF excitation only.
* With interneurons.
* Parameters for plasticity of INs from my data set
* Passive props fit (by eye) from my data set for all neurons
* PY cells have no plasticity

"""

from equations import synapse_eqs
from equations import onspike_eqs
from equations import sinusoid_rate
from equations import neuron_eqs_with_Rin
import brian2 as brian

# need to solve for synaptic conductances,
# which will be a function of the number of neurons
N_afferents_total = 400
p_afferent_connect = 0.25
N_afferents = N_afferents_total * p_afferent_connect
total_EPSC_on_PY = 1000 * brian.pamp
scale_fact_FS = 5
scale_fact_SOM = 0.15
driving_force = 70 * brian.mvolt

#  EPSC tau onto PY cells is about 3.5ms. Onto PV is about 2.5 ms
tau_epsc = 0.003

# solve for the weights, make them unitless (but represent pS)
we_v1_onto_py = (total_EPSC_on_PY / driving_force) / N_afferents / brian.psiemens
we_v1_onto_fs = ((total_EPSC_on_PY * scale_fact_FS) / driving_force) / N_afferents / brian.psiemens
we_v1_onto_som = ((total_EPSC_on_PY * scale_fact_SOM) / driving_force) / N_afferents / brian.psiemens


settings = {
    "neurons": {
        "HVA_FS": {
            "N": 20,
            "eqs": neuron_eqs_with_Rin,
            "tau_m": 0.004,
            "R_in": 85,  # MOhm
            "tau_e": tau_epsc,
            "tau_i": 0.010,  # not constrained by data
            "thresh": -0.040,
            "reset": -0.060,
            "V_rest": -0.065,
            "refract": 0.0023
        },
        "HVA_SOM": {
            "N": 20,
            "eqs": neuron_eqs_with_Rin,
            "tau_m": 0.0182,
            "R_in": 240,  # MOhm
            "tau_e": tau_epsc,
            "tau_i": 0.010,  # not constrained by data
            "thresh": -0.040,
            "reset": -0.055,
            "V_rest": -0.062,
            "refract": 0.008
        },
        "HVA_PY": {
            "N": 20,
            "eqs": neuron_eqs_with_Rin,
            "tau_m": 0.020,
            "R_in": 87,  # MOhm, but set later
            "tau_e": tau_epsc,
            "tau_i": 0.010,  # not constrained by data
            "thresh": -0.035,
            "reset": -0.050,
            "V_rest": -0.065,
            "refract": 0.020
        },
    },

    "afferents": {
        "N": N_afferents_total,
        "use_poisson": True,
        "modulation_rate": [0.1, 0.5, 1, 4],  # [0.01, 0.1, 0.2, 0.4, 1, 2, 4, 8, 16, 32, 64],
        "peak_rate": 50,
        "eqs": sinusoid_rate,
        "spikes_per_second": 1,
        "sim_time": 5  # change to 5 for sinusoids
    },

    "synapses": {
        ("afferents", "HVA_FS"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": p_afferent_connect,
            "d1": 0.8966,
            "d2": 0.92244,
            "f1": 0,
            "f2": 0,
            "tau_D1": 0.0504,
            "tau_D2": 0.10431,
            "tau_F1": 0.0001,
            "tau_F2": 0.0001,
            "w_e": we_v1_onto_fs,
            "w_i": 0,
            "delay": 0.002
        },

        ("afferents", "HVA_SOM"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": p_afferent_connect,
            "d1": 0.87488,
            "d2": 0.94607,
            "f1": 1.6817,
            "f2": 0.27817,
            "tau_D1": 0.10472,
            "tau_D2": 0.084781,
            "tau_F1": 0.050023,
            "tau_F2": 0.57205,
            "w_e": we_v1_onto_som,
            "w_i": 0,
            "delay": 0.002
        },

        ("afferents", "HVA_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": p_afferent_connect,
            "d1": 1,
            "d2": 1,
            "f1": 0,
            "f2": 0,
            "tau_D1": 0.0001,
            "tau_D2": 0.0001,
            "tau_F1": 0.0001,
            "tau_F2": 0.0001,
            "w_e": we_v1_onto_py,
            "w_i": 0,
            "delay": 0.002
        },
    },

    "monitors": {
        "HVA_FS": 'V spikes',  # Ge_total Gi_total
        "HVA_SOM": 'V spikes',
        "HVA_PY": 'V spikes',
        "afferents": 'spikes'
    }
}


# add connections b/w INs and PY cells. Make Pconnect higher for som->med
# to reflect the higher number of SOM cells. Possibly make the
# SOM->PYmed weights stronger than the SOM->PVlat weights to reflect
# the lower number of INs in medial areas to begin with.
#
# also update the synaptic params to reflect AM vs. LM
