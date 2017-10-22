"""Settings for feedforward Network.

These settings are for a network of FF excitation only.
* No interneurons.
* Parameters for plasticity were estimated from CH's experiments using the
  fit to the grand average raw data. 6/12/2017
* Passive props same for all postsynaptic cells

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
            "tau_m": 0.020,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.044,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "CONTROL_PY": {
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
    },

    "afferents": {
        "N": 200,
        "use_poisson": True,
        "modulation_rate": [0.01, 0.1, 0.2, 0.4, 1, 2, 4, 8, 16, 32, 64],  # [0, 0.5, 1, 2, 4, 8, 16, 32],
        "peak_rate": 50,
        "eqs": sinusoid_rate,
        "spikes_per_second": None,
        "sim_time": 5
    },

    "synapses": {
        ("afferents", "LAT_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.745776372204423,
            "d2": 0.384630322243764,
            "f1": 0.20171125824736,
            "f2": 1.99996992031001,
            "tau_D1": 0.408571779798192,
            "tau_D2": 0.0782562829011947,
            "tau_F1": 0.526480048225554,
            "tau_F2": 0.0611956230085695,
            "w_e": 0.0025,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "MED_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.57033797518005,
            "d2": 0.877343800497582,
            "f1": 0.24791793329521,
            "f2": 1.24055971861832,
            "tau_D1": 0.193759182770654,
            "tau_D2": 1.26678114645274,
            "tau_F1": 1.18578349080901,
            "tau_F2": 0.1027449281392,
            "w_e": 0.0025,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "CONTROL_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 1,
            "d2": 1,
            "f1": 0,
            "f2": 0,
            "tau_D1": 1,
            "tau_D2": 1,
            "tau_F1": 1,
            "tau_F2": 1,
            "w_e": 0.0025,
            "w_i": 0,
            "delay": 0
        },
    },

    "monitors": {
        "MED_PY": 'V Ge_total Gi_total spikes',
        "LAT_PY": 'V Ge_total Gi_total spikes',
        "CONTROL_PY": 'V Ge_total Gi_total spikes',
        "afferents": 'spikes'
    }
}


# add connections b/w INs and PY cells. Make Pconnect higher for som->med
# to reflect the higher number of SOM cells. Possibly make the
# SOM->PYmed weights stronger than the SOM->PVlat weights to reflect
# the lower number of INs in medial areas to begin with.
#
# also update the synaptic params to reflect AM vs. LM
