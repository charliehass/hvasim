"""Analysis routines for the hva simulation.
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import dill as pickle
import brian2 as brian
import dpath.util


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


def extract_afferent_monitors(data_dict, binsize=0.100):

    # store data in dictionary, one for each file
    monitors = {fname: {} for fname in data_dict.keys()}  # init empty dicts
    for fname in data_dict.keys():
        # initialize the dict for fname'th sim file
        monitors[fname]["afferents"] = {"unit_idx": np.array([]),
                                        "spk_t": np.array([]),
                                        "psth": {},
                                        "params": {}}

        mon_name = "afferents_spike_mon"
        net = data_dict[fname]["net"]
        if mon_name in net.keys():
            monitors[fname]["afferents"]['params'] = data_dict[fname]['settings']['afferents']
            monitors[fname]["afferents"]["spk_t"] = net[mon_name]["t"]
            monitors[fname]["afferents"]["unit_idx"] = net[mon_name]["i"]

            sim_time = data_dict[fname]['settings']['afferents']['sim_time']
            sim_time = np.int(np.round(np.max(monitors[fname]["afferents"]["spk_t"])))
            print("hack for sim_time: ", sim_time)
            psths = spk_mon_to_psth(monitors[fname]["afferents"],
                                    binsize,
                                    sim_time)
            monitors[fname]["afferents"]["psth"] = psths

    return monitors


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
    cm = plt.cm.get_cmap('Dark2')

    if plot_type.lower() == "overlay":
        fig, axs = plt.subplots(N_sim_conds, 1, figsize=(10, 25))
    elif plot_type.lower() == "grid":
        width = 25
        height = 5 * N_sim_conds
        fig, axs = plt.subplots(N_sim_conds,
                                N_neuron_groups,
                                figsize=(width, height)
                                )
    else:
        raise "Unknown plot_type"

    for row_idx, sim_type in enumerate(monitors.keys()):
        for col_idx, neuron_group in enumerate(neuron_names):
            tt = monitors[sim_type][neuron_group]['time']
            yy = monitors[sim_type][neuron_group]['dat']
            y_units = brian.get_unit(yy)
            yy * y_units  # backout the units

            if plot_type.lower() == "overlay":
                if N_sim_conds == 1:
                    ax = axs
                else:
                    ax = axs[row_idx]
            else:
                if N_sim_conds == 1:
                    ax = axs[col_idx]
                else:
                    ax = axs[row_idx, col_idx]

            # plot
            ax.plot(tt, yy, c=cm.colors[col_idx], label=neuron_group)
            ax.set_ylabel("monitor ({})".format(y_units), fontsize=fnt_sz)
            ax.set_xlabel("time (sec)", fontsize=fnt_sz)

            # add y units
            ax.set_ylabel(y_units)
            if y_units == brian.volt:
                #  ax.set_ylim(-0.070, -0.058)
                pass
            elif y_units == brian.siemens:
                pass

            # add title or legend
            if plot_type.lower() == "overlay":
                if row_idx == 0:
                    ax.legend()
            else:
                if row_idx == 0:
                    ax.set_title(neuron_group)

    return fig, axs


def plot_spk_summary(monitors, neuron_names, plot_type="overlay", average=True):
    """
    Plot a summary figure of the simmulation for the monitors supplied.
    """

    fnt_sz = 12
    N_sim_conds = len(monitors)
    N_neuron_groups = len(neuron_names)
    cm = plt.cm.get_cmap('Dark2')

    if plot_type.lower() == "overlay":
        fig, axs = plt.subplots(N_sim_conds, 1, figsize=(10, 25))
    elif plot_type.lower() == "grid":
        width = 25
        height = 5 * N_sim_conds
        fig, axs = plt.subplots(N_sim_conds,
                                N_neuron_groups,
                                figsize=(width, height)
                                )
    else:
        raise "Unknown plot_type"

    for row_idx, sim_type in enumerate(monitors.keys()):
        for col_idx, neuron_group in enumerate(neuron_names):
            tt = monitors[sim_type][neuron_group]['psth']['edges'][0:-1]
            yy = monitors[sim_type][neuron_group]['psth']['rates']

            if plot_type.lower() == "overlay":
                if N_sim_conds == 1:
                    ax = axs
                else:
                    ax = axs[row_idx]
            else:
                if N_sim_conds == 1:
                    ax = axs[col_idx]
                else:
                    ax = axs[row_idx, col_idx]

            # plot (if there are data)
            if len(yy) > 0:
                if average:
                    ax.plot(tt, np.mean(yy, axis=0), c=cm.colors[col_idx])
                else:
                    for yy_unit in yy:
                        ax.plot(tt,
                                yy_unit,
                                c=cm.colors[col_idx]
                                )

            # add x/y labels
            ax.set_ylabel("spk/sec", fontsize=fnt_sz)
            ax.set_xlabel("time (sec)", fontsize=fnt_sz)

            # add title or legend
            if plot_type.lower() == "overlay":
                # plt.legend()
                pass
            else:
                if row_idx == 0:
                    ax.set_title(neuron_group)

    return fig, axs


def plot_hva_rasters(monitors, neuron_names):
    """
    Plot a summary figure of the simmulation for the monitors supplied.
    """

    fnt_sz = 12
    N_sim_conds = len(monitors)
    N_neuron_groups = len(neuron_names)
    cm = plt.cm.get_cmap('Dark2')

    # set up the figure
    width = 25
    height = 5 * N_sim_conds
    fig, axs = plt.subplots(N_sim_conds,
                            N_neuron_groups,
                            figsize=(width, height)
                            )

    for row_idx, sim_type in enumerate(monitors.keys()):
        for col_idx, neuron_group in enumerate(neuron_names):
            tt = monitors[sim_type][neuron_group]['spk_t']
            yy = monitors[sim_type][neuron_group]['unit_idx']

            if N_sim_conds == 1:
                ax = axs[col_idx]
            else:
                ax = axs[row_idx, col_idx]

            # plot (if there are data)
            if len(yy) > 0:
                ax.plot(tt, yy, '|', c=cm.colors[col_idx])

            # add x/y labels
            ax.set_ylabel("unit number", fontsize=fnt_sz)
            ax.set_xlabel("time (sec)", fontsize=fnt_sz)

            # add title or legend
            if row_idx == 0:
                ax.set_title(neuron_group)

    return fig, axs


def plot_afferent_rasters(monitors):

    fnt_sz = 12
    N_sim_conds = len(monitors)

    fig, axs = plt.subplots(N_sim_conds, 1, figsize=(20, 40))

    for row_idx, fid in enumerate(monitors.keys()):
            tt = monitors[fid]["afferents"]['spk_t']
            yy = monitors[fid]["afferents"]['unit_idx']

            # plot (if there are data)
            if len(yy) > 0:
                axs[row_idx].plot(tt, yy, 'k|')

            # add x/y labels
            axs[row_idx].set_ylabel("afferent idx", fontsize=fnt_sz)
            axs[row_idx].set_xlabel("time (sec)", fontsize=fnt_sz)

    return fig, axs


def calculate_depth_of_mod(time_series, baseline=0, freq=0, samp_freq=1000):

    is_1d = time_series.ndim
    min_1d = np.min(time_series.shape) == 1
    assert is_1d or min_1d, "ERROR: incorrect dimensionality of time_series"

    # remove the first second of data
    # time_series = time_series[int(samp_freq):]
    n = time_series.size  # len returns 1 for row vec,  .size is more reliable

    # make the time_series a row vector
    time_series = time_series.reshape(1, n)

    # ditch the units
    time_series = time_series / brian.get_unit(time_series)

    # need to baseline subtract so that DOM is wrt pre-stim condition
    time_series = time_series - baseline

    if freq == 0:
        basis = np.ones((n, 1), dtype=float)
        dom = np.abs(np.dot(time_series, basis)) / n
        dom = dom[0]
    else:
        tt = np.arange(n) / samp_freq
        basis = np.exp(-2 * np.pi * np.sqrt(-1 + 0j) * freq * tt)
        basis.reshape(n, 1)  # column vector
        time_series_zero_mean = time_series - np.mean(time_series)
        dom = 2 * np.abs(np.dot(time_series_zero_mean, basis)) / n

    assert len(dom) == 1, "ERROR: output dims not correct"
    return dom[0]


def get_all_dat_dom(monitors, neuron_names, samp_freqs, tf_dict):
    out = {name: [] for name in neuron_names}  # empty dict for each neuron
    for i_tf, fid in enumerate(monitors.keys()):
        for neuron in neuron_names:
            yy = monitors[fid][neuron]['dat']
            baseline = yy[0] / brian.get_unit(yy[0])
            tf = tf_dict[fid]
            dom = calculate_depth_of_mod(yy,
                                         baseline=baseline,
                                         freq=tf,
                                         samp_freq=samp_freqs[i_tf]
                                         )
            out[neuron].append([tf, dom])

    return out


def get_looped_param_list(dat_dict, dict_addr):
    glob_prefix = '{}/settings/{}'
    globs = [glob_prefix.format(x, dict_addr) for x in dat_dict.keys()]
    params = [dpath.util.get(dat_dict, x) for x in globs]
    out_dict = {fid: val for fid, val in zip(dat_dict.keys(), params)}
    return out_dict


def plot_frequency_response(dom_dict, plot_type="overlay"):

    fnt_sz = 12
    N_neuron_groups = len(dom_dict)
    cm = plt.cm.get_cmap('Dark2')

    if plot_type.lower() == "overlay":
        fig, axs = plt.subplots(1, 1, figsize=(10, 10))
    elif plot_type.lower() == "grid":
        fig, axs = plt.subplots(1, N_neuron_groups, figsize=(25, 10))
    else:
        raise "Unknown plot_type"

    # calculate the depth of modulation for each neuron_type
    max_yy = 0
    for col_idx, neuron in enumerate(dom_dict.keys()):
        dat = np.array(dom_dict[neuron])
        inds = np.argsort(dat[:, 0], axis=0)
        ff = dat[inds, 0]
        amps = dat[inds, 1]

        # fix ff of zero b/c it won't apear on a log plot_type
        if 0 in ff:
            zero_idx = ff.tolist().index(0)
            ff[zero_idx] = ff[zero_idx + 1] / 4

        if plot_type.lower() == "overlay":
            ax = axs
        else:
            ax = axs[col_idx]

        # plot
        ax.plot(ff, amps, c=cm.colors[col_idx], label=neuron)
        ax.set_ylabel("depth of mod (V)")
        ax.set_xlabel("modulation frequency", fontsize=fnt_sz)
        ax.set_yscale("log")
        ax.set_xscale("log")
        max_yy = np.max([np.max(amps), max_yy])
        ax.set_ylim(0, max_yy * 1.05)

        # add title or legend
        if plot_type.lower() == "overlay":
            plt.legend()
        else:
            ax.set_title(neuron)

    return fig, ax
