"""Analysis routines for the hva simulation.
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import dill as pickle
import brian2 as brian


def unpickle(pickle_file):
    """
    Unpickle a file and return its contents a mega-dictionary
    of all the monitored states during that run
    """
    with open(pickle_file, 'rb') as open_f:
        net = pickle.load(open_f)
    return net


def load_all_files(file_names, simulations_directory):
    """
    Plot a summary figure of the simmulation (all the files).
    But specify which monitor should be plotted.
    Vm, Ge, Gi can all be plotted
    """

    alldata = {}
    for fname in file_names:
        tmpdat = unpickle(simulations_directory + os.sep + fname)
        alldata[fname] = {"net": tmpdat["net"],
                          "settings": tmpdat["settings"],
                          "description": tmpdat["description"]
                          }
    return alldata


def extract_anlg_monitors(data_dict, mon_type="v"):
    # define key names for dynamic indexing
    if mon_type.lower() == "v":
        mon_suffix = "_V_mon"
        key_to_data = "V"
    elif mon_type.lower() == "ge_total":
        mon_suffix = "_Ge_total_mon"
        key_to_data = "Ge_total"
    elif mon_type.lower() == "gi_total":
        mon_suffix = "_Gi_total_mon"
        key_to_data = "Gi_total"
    else:
        raise Exception("plot type {} not recognized".format(mon_type))

    # store data in dictionary, one for each file
    monitors = {fname: {} for fname in data_dict.keys()}  # init empty dicts
    neuron_names = []
    for fname in data_dict.keys():
        neuron_groups = data_dict[fname]["settings"]["neurons"].keys()
        neuron_names.extend(list(neuron_groups))

        for neuron in neuron_groups:
            mon_name = neuron + mon_suffix
            net = data_dict[fname]["net"]
            if mon_name in net.keys():
                monitors[fname][neuron] = {"dat": net[mon_name][key_to_data],
                                           "time": net[mon_name]["t"],
                                           "mon": net[mon_name]
                                           }
            else:
                monitors[fname][neuron] = {"dat": np.array([]),
                                           "time": np.array([]),
                                           }

    return monitors, list(set(neuron_names))


def extract_spk_monitors(data_dict, binsize=0.025):

    # define key names for dynamic indexing
    mon_suffix = "_spike_mon"

    # store data in dictionary, one for each file
    monitors = {fname: {} for fname in data_dict.keys()}  # init empty dicts
    neuron_names = []
    for fname in data_dict.keys():
        neuron_groups = data_dict[fname]["settings"]["neurons"].keys()
        neuron_names.extend(list(neuron_groups))
        sim_time = data_dict[fname]['settings']['afferents']['sim_time']
        for neuron in neuron_groups:
            mon_name = neuron + mon_suffix
            net = data_dict[fname]["net"]
            if mon_name in net.keys():
                monitors[fname][neuron] = {"spk_t": net[mon_name]["t"],
                                           "unit_idx": net[mon_name]["i"],
                                           }
                psths = spk_mon_to_psth(monitors[fname][neuron],
                                        binsize,
                                        sim_time)
                monitors[fname][neuron]["psth"] = psths
            else:
                monitors[fname][neuron] = {"dat": np.array([]),
                                           "time": np.array([]),
                                           "psth": {}}

    return monitors, list(set(neuron_names))


def spk_mon_to_psth(spk_dict, binsize, total_time):

    # define the binedges
    edges = np.arange(0, total_time + binsize, binsize)

    # get the outputs ready
    out_psth = {'rates': [],
                'unit_idx': [],
                'edges': edges,
                'binsize': binsize}

    # compute the psths
    unit_idxs = set(spk_dict["unit_idx"])
    for idx in unit_idxs:
        l_idx = spk_dict["unit_idx"] == idx  # logical array
        spk_times = spk_dict["spk_t"][l_idx]
        counts_per_bin, _ = np.histogram(spk_times, edges)
        rate_per_bin = np.array(counts_per_bin) / binsize
        out_psth['rates'].append(rate_per_bin)
        out_psth['unit_idx'].append(idx)

    return out_psth


def plot_anlg_summary(monitors, neuron_names, plot_type="overlay"):
    """
    Plot a summary figure of the simmulation for the monitors supplied.
    """

    fnt_sz = 12
    N_sim_conds = len(monitors)
    N_neuron_groups = len(neuron_names)
    cm = plt.cm.get_cmap('Vega10')

    if plot_type.lower() == "overlay":
        fig, axs = plt.subplots(N_sim_conds, 1, figsize=(10, 25))
    elif plot_type.lower() == "grid":
        fig, axs = plt.subplots(N_sim_conds, N_neuron_groups, figsize=(25, 25))
    else:
        raise "Unknown plot_type"

    for row_idx, sim_type in enumerate(monitors.keys()):
        for col_idx, neuron_group in enumerate(monitors[sim_type].keys()):
            tt = monitors[sim_type][neuron_group]['time']
            yy = monitors[sim_type][neuron_group]['dat']
            y_units = brian.get_unit(yy)
            if y_units == brian.units.allunits.steradian3:
                y_units = "conductance"

            if plot_type.lower() == "overlay":
                ax = axs[row_idx]
            else:
                ax = axs[row_idx, col_idx]

            # plot
            ax.plot(tt, yy, c=cm.colors[col_idx], label=neuron_group)
            ax.set_ylabel("monitor ({})".format(y_units), fontsize=fnt_sz)
            ax.set_xlabel("time (sec)", fontsize=fnt_sz)

            # add y units
            if y_units == brian.volt:
                # ax.set_ylim(-0.077, -0.040)
                pass
            elif y_units == "conductance":
                pass

            # add title or legend
            if plot_type.lower() == "overlay":
                plt.legend()
            else:
                if row_idx == 0:
                    ax.set_title(neuron_group)

    plt.show()
    return


def plot_spk_summary(monitors, neuron_names, plot_type="overlay"):
    """
    Plot a summary figure of the simmulation for the monitors supplied.
    """

    fnt_sz = 12
    N_sim_conds = len(monitors)
    N_neuron_groups = len(neuron_names)
    cm = plt.cm.get_cmap('Vega10')

    if plot_type.lower() == "overlay":
        fig, axs = plt.subplots(N_sim_conds, 1, figsize=(10, 25))
    elif plot_type.lower() == "grid":
        fig, axs = plt.subplots(N_sim_conds, N_neuron_groups, figsize=(25, 25))
    else:
        raise "Unknown plot_type"

    for row_idx, sim_type in enumerate(monitors.keys()):
        for col_idx, neuron_group in enumerate(monitors[sim_type].keys()):
            tt = monitors[sim_type][neuron_group]['psth']['edges'][0:-1]
            yy = monitors[sim_type][neuron_group]['psth']['rates']

            if plot_type.lower() == "overlay":
                ax = axs[row_idx]
            else:
                ax = axs[row_idx, col_idx]

            # plot (if there are data)
            if len(yy) > 0:
                for yy_unit in yy:
                    ax.plot(tt,
                            yy_unit,
                            c=cm.colors[col_idx],
                            label=neuron_group
                            )

            # add x/y labels
            ax.set_ylabel("spk/sec", fontsize=fnt_sz)
            ax.set_xlabel("time (sec)", fontsize=fnt_sz)
            ax.set_ylim(0, 300)

            # add title or legend
            if plot_type.lower() == "overlay":
                plt.legend()
            else:
                if row_idx == 0:
                    ax.set_title(neuron_group)

    plt.show()
    return
