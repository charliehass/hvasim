"""Settings for feedforward Network.

These settings are for a network of FF excitation only. No interneurons.

Parameters for plasticity were drawn from Charlie's data (4/2017)

"""

from equations import neuron_eqs, synapse_eqs, onspike_eqs, sinusoid_rate


settings = {
    "neurons": {
        "MED_HVA_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.044,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "LAT_HVA_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.025,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.040,
            "reset": -0.048,
            "V_rest": -0.075,
            "refract": 0.0015
        },
    },

    "afferents": {
        "N": 1000,
        "use_poisson": True,
        "modulation_rate": [0, 1, 25, 50],  # [0, 1, 3, 6, 12, 25, 50, 100]
        "peak_rate": 30,
        "eqs": sinusoid_rate,
        "spikes_per_second": None,
        "sim_time": 3
    },

    "synapses": {
        ("afferents", "MED_HVA_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.20,
            "d1": 0.51642,
            "d2": 0.71354,
            "f1": 0.34452,
            "f2": 1.5001,
            "tau_D1": 0.15051,
            "tau_D2": 0.35033,
            "tau_F1": 1.0608,
            "tau_F2": 0.10762,
            "w_e": 0.020,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "LAT_HVA_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 0.20,
            "d1": 0.40722,
            "d2": 0.70762,
            "f1": 0.46088,
            "f2": 1.6147,
            "tau_D1": 0.40722,
            "tau_D2": 0.70762,
            "tau_F1": 0.69453,
            "tau_F2": 0.09442,
            "w_e": 0.020,
            "w_i": 0,
            "delay": 0
        },
    },

    "monitors": {
        "MED_HVA_PY": 'V Ge_total',
        "LAT_HVA_PY": 'V Ge_total',
        "afferents": 'spikes'
    }
}
