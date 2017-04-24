"""Settings for feedforward Network.

These settings are for a network of FF excitation only. No interneurons.

Parameters for plasticity were drawn from Charlie's data (4/2017)

"""

from equations import neuron_eqs, synapse_eqs, onspike_eqs, sinusoid_rate


settings = {
    "neurons": {
        "MED_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.020,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.044,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "LAT_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.015,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.048,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "HVA_PV": {
            "N": 3,  # set to 100 for full model
            "eqs": neuron_eqs,
            "tau_m": 0.010,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.042,
            "V_rest": -0.070,
            "refract": 0.005
        },
        "HVA_SOM": {
            "N": 1,  # set to 100 for full model
            "eqs": neuron_eqs,
            "tau_m": 0.025,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.044,
            "V_rest": -0.065,
            "refract": 0.010
        },
    },

    "afferents": {
        "N": 10000,
        "use_poisson": True,
        "modulation_rate": 0,  # [0, 0.5, 1, 2, 4, 8, 16, 32]
        "peak_rate": 20,
        "eqs": sinusoid_rate,
        "spikes_per_second": None,
        "sim_time": 3
    },

    "synapses": {
        ("afferents", "MED_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.1,
            "d1": 0.749467099783301,
            "d2": 0.700437181519722,
            "f1": 1.13807720160064,
            "f2": 0.0483709364290671,
            "tau_D1": 0.365734211868718,
            "tau_D2": 0.0400001490139746,
            "tau_F1": 0.112433824472314,
            "tau_F2": 4.99813893799875,
            "w_e": 0,
            "w_i": 0,
            "delay": 0.002
        },

        ("afferents", "LAT_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.10,
            "d1": 0.713289167753535,
            "d2": 0.61815647916645,
            "f1": 0.0625555392792278,
            "f2": 1.08228513737162,
            "tau_D1": 0.312011074654424,
            "tau_D2": 0.0400023180322909,
            "tau_F1": 0.887175955605229,
            "tau_F2": 0.0904394937105904,
            "w_e": 0,
            "w_i": 0,
            "delay": 0.002
        },

        ("afferents", "HVA_PV"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.20,
            "d1": 0.473617339960491,
            "d2": 0.696307735155633,
            "f1": 0.919868184041437,
            "f2": 0.688201290212496,
            "tau_D1": 0.138803522289082,
            "tau_D2": 0.570740671744164,
            "tau_F1": 0.072675501828418,
            "tau_F2": 0.31581325424265,
            "w_e": [0.006, 0.007, 0.008, 0.009, 0.010, 0.011],
            "w_i": 0,
            "delay": 0.002
        },

        ("afferents", "HVA_SOM"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.20,
            "d1": 1,
            "d2": 0.835599557217797,
            "f1": 1.27821374452506,
            "f2": 0.278540399084653,
            "tau_D1": 2.42301768011074,
            "tau_D2": 0.0784851537484495,
            "tau_F1": 1.27821374452506,
            "tau_F2": 0.278540399084653,
            "w_e": 0,
            "w_i": 0,
            "delay": 0.002
        },

        ("HVA_PV", "LAT_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,  # set to 40% for real model
            "d1": 0.473617339960491,
            "d2": 0.696307735155633,
            "f1": 0.919868184041437,
            "f2": 0.688201290212496,
            "tau_D1": 0.138803522289082,
            "tau_D2": 0.570740671744164,
            "tau_F1": 0.072675501828418,
            "tau_F2": 0.31581325424265,
            "w_e": 0,
            "w_i": 0.025,
            "delay": 0.002
        },

        ("HVA_PV", "MED_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,  # set to 40% for real model
            "d1": 0.473617339960491,
            "d2": 0.696307735155633,
            "f1": 0.919868184041437,
            "f2": 0.688201290212496,
            "tau_D1": 0.138803522289082,
            "tau_D2": 0.570740671744164,
            "tau_F1": 0.072675501828418,
            "tau_F2": 0.31581325424265,
            "w_e": 0,
            "w_i": 0.025,
            "delay": 0.002
        },
    },

    "monitors": {
        "MED_PY": 'V Ge_total Gi_total spikes',
        "LAT_PY": 'V Ge_total Gi_total spikes',
        "HVA_PV": 'V Ge_total spikes',
        "HVA_SOM": 'V Ge_total spikes',
        "afferents": 'spikes'
    }
}


# add connections b/w INs and PY cells. Make Pconnect higher for som->med
# to reflect the higher number of SOM cells. Possibly make the
# SOM->PYmed weights stronger than the SOM->PVlat weights to reflect
# the lower number of INs in medial areas to begin with.
#
# also update the synaptic params to reflect AM vs. LM
