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
            "d1": 0.749791212284898,
            "d2": 0.781584143559302,
            "f1": 0.0590022328374986,
            "f2": 0.963202620601335,
            "tau_D1": 0.420903997287144,
            "tau_D2": 0.0400201594781335,
            "tau_F1": 4.99546381846439,
            "tau_F2": 0.129068776502273,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "LAT_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.699015990209628,
            "d2": 0.357083229942332,
            "f1": 1.99994759811683,
            "f2": 0.0221270322957057,
            "tau_D1": 0.184144229969057,
            "tau_D2": 0.0400044706622858,
            "tau_F1": 0.0571980386308833,
            "tau_F2": 4.99960469207174,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "FS"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.80192248039302,
            "d2": 0.653629376740116,
            "f1": 0.0465710525947677,
            "f2": 0.763481721014774,
            "tau_D1": 0.0400008972304614,
            "tau_D2": 0.541640231559288,
            "tau_F1": 4.99968792518823,
            "tau_F2": 0.167523752854107,
            "w_e": 1,
            "w_i": 0,
            "delay": 0
        },

        ("afferents", "SOM"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "p_connect": 1,
            "d1": 0.96402104078955,
            "d2": 0.999999245044985,
            "f1": 1.10266125277584,
            "f2": 0.126709362146515,
            "tau_D1": 0.077385530280161,
            "tau_D2": 2.47117271802827,
            "tau_F1": 0.0955007412337583,
            "tau_F2": 4.99903706972549,
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
