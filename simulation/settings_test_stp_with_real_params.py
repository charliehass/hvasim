"""Settings to test STP dynamics.

1) Enforces all the HVA neurons to be identical (all clones
   of the default PY cells)

2) Recovery of D,F is infinite so that we can see:
    * Geometric decay for Depression
    * Linear increase for facilitation

3) Feedforward weights of the V1 afferents onto the HVA neurons
   3 different values so that we can ensure the weights are correct
     * the P1 amplitude should be equal to this weight.

4) Dynamics of STP are different across the HVA neurons to check to make
   sure things are correct.

5) Decay of synaptic conductance is instantaneous so that there is no summation
   and the only dynamics of the EPSCs is due to STP (D,F, d,f)

"""

from equations import neuron_eqs, synapse_eqs, onspike_eqs, sinusoid_rate


settings = {
    "neurons": {
        "MED_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "LAT_PY": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "FS": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "SOM": {
            "N": 1,
            "eqs": neuron_eqs,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        }
    },

    "afferents": {
        "N": 1,
        "use_poisson": False,
        "modulation_rate": None,
        "peak_rate": None,
        "spikes_per_second": [1, 10, 50, 100],  # pulse train frequencies
        "eqs": sinusoid_rate,
        "sim_time": 5
    },

    "synapses": {
        ("afferents", "MED_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.677779435896493,
            "d2": 0.955948527539736,
            "f1": 0.148664758049794,
            "f2": 0.832543707486315,
            "tau_D1": 0.351337559465874,
            "tau_D2": 4.9999853200625,
            "tau_F1": 2.73381117965421,
            "tau_F2": 0.141095029186461,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "LAT_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.742699612358215,
            "d2": 0.380550934611453,
            "f1": 0.185905243622942,
            "f2": 1.99385635699509,
            "tau_D1": 0.390633486546194,
            "tau_D2": 0.0761030284059299,
            "tau_F1": 0.524076918189163,
            "tau_F2": 0.0613934939446212,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "FS"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.432578461135955,
            "d2": 0.780335983676696,
            "f1": 0.353000433498374,
            "f2": 1.40831789911982,
            "tau_D1": 0.206258773398254,
            "tau_D2": 0.903356348050939,
            "tau_F1": 0.710594220581384,
            "tau_F2": 0.0952281600157747,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "SOM"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.99999988547475,
            "d2": 0.999999885044096,
            "f1": 0.95088768316992,
            "f2": 0.113095357180333,
            "tau_D1": 2.23652758743532,
            "tau_D2": 2.19678699022476,
            "tau_F1": 0.111601436492032,
            "tau_F2": 2.94599944507649,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        }
    },

    "monitors": {
        "MED_PY": 'V Ge_total',
        "LAT_PY": 'V Ge_total',
        "FS": 'V Ge_total',
        "SOM": 'V Ge_total',
        "afferents": 'spikes'
    }
}
