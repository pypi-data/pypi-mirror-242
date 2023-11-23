# v. 7.2.0 231117

import logging

from config_util import get_origplot_params, get_sigfilt_params, get_envelope_params
from plot_util import common_axes_personalization, handle_subplot_err

def addplot_orig_sign(config, opdesc, orig_xlabel, channelsetname, orig_ylabel, plot_title, targetAxes, time, signal, sig_time_window, sig_ampl_limits, incl_envelope, signal_peaks, include_sig_filtered, signal_filtered):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_orig_sign_raw(config, opdesc, orig_xlabel, channelsetname, orig_ylabel, plot_title, targetAxes, time, signal, sig_time_window, sig_ampl_limits, incl_envelope, signal_peaks, include_sig_filtered, signal_filtered)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_orig_sign_raw(config, opdesc, orig_xlabel, channelsetname, orig_ylabel, plot_title, target_ax, time, signal, sig_time_window, sig_ampl_limits, incl_envelope, signal_peaks, include_sig_filtered, signal_filtered):
    logger = logging.getLogger(__name__)
    orig_bgcolor, orig_yscale, orig_grid, orig_color, orig_lwidth, orig_label = get_origplot_params(config)
    target_ax.plot(time, signal, color=orig_color, linewidth=orig_lwidth, label=orig_label)
    #plot_title = plot_title + post_dssampl_subplot_title
    #print ('\n\n ' + orig_xlabel + ' \n\n')
    csadjustment = '(' + channelsetname + ') ' if (channelsetname and (len(channelsetname) > 0)) else ''
    common_axes_personalization(target_ax, plot_title, orig_xlabel, csadjustment + orig_ylabel, orig_grid, orig_yscale, sig_time_window, sig_ampl_limits, orig_bgcolor)
    incl_envel_in_tooltip = incl_envelope
    incl_filtsig_in_tooltip = include_sig_filtered
    if (incl_envelope):
        env_color, env_label, env_lwidth = get_envelope_params(config) # 'red', 'envelope', 1
        # Calculate the envelope using peaks
        #signal_peaks, _ = find_peaks(signal)
        # add peaks
        try:
            target_ax.scatter(time[signal_peaks], signal[signal_peaks], color=env_color, label=env_label, linewidth=env_lwidth)
        except Exception as e1:
            logger.error('Envelope rendering error: ' + str(e1))
            incl_envel_in_tooltip = False

    if (include_sig_filtered):
        sig_filtered_color, sig_filtered_linestyle, sig_filtered_linewidth, sig_filt_label = get_sigfilt_params(config) # 'gray', 'dashed', 1, 'filtered'
        try:
            target_ax.plot(time, signal_filtered, linestyle=sig_filtered_linestyle, color=sig_filtered_color, linewidth=sig_filtered_linewidth, label=sig_filt_label)
        except Exception as e2:
            logger.error('Filtered signal rendering error: ' + str(e2))
            incl_filtsig_in_tooltip = False

        #target_ax.legend(loc='upper right', bbox_to_anchor=(1, 0.5), framealpha=0.2)
        #target_ax.legend(loc='upper right')
    add_origplot_tooltip(config, target_ax, incl_filtsig_in_tooltip, incl_envel_in_tooltip)
    logger.debug('Subplot created (' + opdesc + ')')

def add_origplot_tooltip(config, ax, incl_sig_filtered, incl_env):
    #lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = get_origplot_tooltip_params(config)
    lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = True, 8, 'round', 'top', 'yellow', 0.3, 0, 1
    if ((incl_sig_filtered or incl_env) and lg_enabled):
        textstr = ''
        notes_count = 0
        if (incl_sig_filtered):
            textstr = textstr + '+filtered'
            notes_count = notes_count + 1
        if (incl_env):
            if (notes_count > 0):
                textstr = textstr + '\n'
            textstr = textstr + '+envel'
        leg_props = dict(boxstyle=lg_boxstyle, facecolor=lg_bgcolor, alpha=float(lg_transp))
        ax.text(float(lg_xpos), float(lg_ypos), textstr, transform=ax.transAxes, fontsize=int(lg_fontsz), verticalalignment=lg_vertalign, bbox=leg_props)
