# v. 7.2.0 231117

import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import FuncFormatter
#from scipy.signal import welch

from plot_window_wrap import PlotWindowWrapper
from config_util import get_freq_xgrain, get_rainbow_colors
from file_util import get_file_basename

from plot_util import common_axes_personalization, override_axis_boundaries, add_freqplots_tooltip #, eval_subplot_title
from plot_origsignal import addplot_orig_sign
from plot_ft import addplot_ft
from plot_ftphase import addplot_ftphase
from plot_psd import addplot_psd
from plot_histogram import addplot_histogram
from plot_spectrogram import addplot_spectrogram
from plot_3d_spectrogram import addplot_3d_spectrogram
from plot_wavelet import addplot_wavelet
from plot_wavelet import addplot_wavelet
from plot_qq import addplot_qq_sign

#import pywt

import logging

class PlotsBuilder:
    def __init__(self, is_multitab, config_hnd, channset_name, chann_xfield, chann_yfield, orig_xlbl, orig_ylbl, chann_name, origsubplot_type_label, incl_original, incl_four_transf, src_info, num_samples_pre, num_samples, num_freq_vals, samp_freq, remove_dc_offset, time_values, time_boundaries, signal_values, sign_peaks_vals, signal_filtered_values, frequencies_values, signal_fft_magn_vals, ft_magn_boundaries, plot_signal_ampl_window, plot_ft_freq_window, sig_ft_phase, psd_freq_window, psd_pow_boundaries, hist_val_window, hist_freq_window, ftphase_freq_window, ftphase_val_window, incl_spectrogr, incl_3dspectrogr, incl_hist, psd_x_axis_vals, psd_y_axis_vals, wavl_scales, wavl_transf_data, wv_type, include_qq):

        self.multi_tab = is_multitab

        self.incl_orig = incl_original
        self.orig_xlbl = orig_xlbl
        self.orig_ylbl = orig_ylbl
        self.incl_ft = incl_four_transf
        self.incl_qq = include_qq

        self.channelset_name = channset_name
        self.channel_xfield = chann_xfield
        self.channel_yfield = chann_yfield
        self.channel_name = chann_name
        self.orig_splot_type_lab = origsubplot_type_label

        self.source_info = get_file_basename(src_info) if (not (src_info is None)) else 'source: unknown'
        self.time = time_values

        self.num_time_samples_pre = num_samples_pre
        self.num_time_samples = num_samples
        self.downsampled = (not (num_samples_pre is None)) and (num_samples < num_samples_pre)
        #self.downsampled = num_samples > num_samples_pre

        self.num_freq_values = num_freq_vals
        self.signal = signal_values
        self.signal_peaks = sign_peaks_vals
        self.signal_filtered = signal_filtered_values
        self.frequencies = frequencies_values
        #self.signal_fft = signal_fft_values
        self.signal_fft_magnitude = signal_fft_magn_vals
        self.signal_ft_phase = sig_ft_phase
        self.config = config_hnd

        self.sig_time_window = time_boundaries
        self.sig_ampl_limits = plot_signal_ampl_window

        self.ft_freq_limits = plot_ft_freq_window
        self.ft_magn_limits = ft_magn_boundaries

        self.psd_x_vals = psd_x_axis_vals
        self.psd_y_vals = psd_y_axis_vals
        self.psd_freq_limits = psd_freq_window
        self.psd_pow_limits = psd_pow_boundaries

        self.hist_val_limits = hist_val_window
        self.hist_freq_limits = hist_freq_window

        self.ftphase_freq_limits = ftphase_freq_window
        self.ftphase_val_limits = ftphase_val_window

        self.wv_scales = wavl_scales
        self.wavelet_transform_data = wavl_transf_data
        self.wavelet_type = wv_type

        self.sampling_freq = samp_freq
        self.dc_offset_suppressed = remove_dc_offset
        self.include_spectrogram = incl_spectrogr
        self.include_3dspectrogram = incl_3dspectrogr
        #self.plt_hnd = None
        self.plotWindowWrap = None
        #self.incl_envelope = incl_envelope
        #self.incl_psd = incl_psd
        self.incl_hist = incl_hist
        #self.include_wavelet = incl_wavelet

    def createPlots(self):
        logger = logging.getLogger(__name__)

        num_subplots = 0;
        self.plt_hnd = None

        # init subplots dictionary
        subplots_dict = {} # ket: file suffix for split saving; value: subplot axes

        rainbow_string = get_rainbow_colors(self.config)
        rainbow_colors = rainbow_string.split(',')

        include_sig_filtered = not (self.signal_filtered is None)
        incl_envelope = not (self.signal_peaks is None)

        include_phasepl = not (self.signal_ft_phase is None)
        incl_psd = not ((self.psd_x_vals is None) or (self.psd_y_vals is None))
        include_wavelet = not ((self.wv_scales is None) or (self.wavelet_transform_data is None))

        if (self.incl_orig):
            num_subplots = num_subplots + 1;
        if (self.incl_ft):
            num_subplots = num_subplots + 1;
        if (include_wavelet):
            num_subplots = num_subplots + 1;
        if (self.include_3dspectrogram):
            num_subplots = num_subplots + 1;
        if (self.include_spectrogram):
            num_subplots = num_subplots + 1;
        if (incl_psd):
            num_subplots = num_subplots + 1;
        if (self.incl_hist):
            num_subplots = num_subplots + 1;
        if (include_phasepl):
            num_subplots = num_subplots + 1;
        if (self.incl_qq):
            num_subplots = num_subplots + 1;

        orig_xlabel, orig_ylabel = self.orig_xlbl, self.orig_ylbl
        #print ('\n\n ' + orig_xlabel + ' \n\n')
        #print ('\n\n ' + orig_ylabel + ' \n\n')

        if (num_subplots > 0):
            logger.info('Creating plots ...')

            #self.plotWindowWrap = PlotWindowWrapper(self.multi_tab, self.config, self.downsampled, self.num_time_samples_pre, self.num_time_samples, self.num_freq_values, num_subplots, self.source_info)
            self.plotWindowWrap = PlotWindowWrapper(self.multi_tab, self.config, num_subplots, self.source_info)
            #post_dssampl_subplot_title = '' if (not self.downsampled) else ' (downsampled, ' + str(self.num_time_samples_pre) + '-->' + str(self.num_time_samples) + ')'
            # Plot the Original Signal

            #self.downsampled, self.num_time_samples_pre, self.num_time_samples
            if (self.incl_orig):
                tab_title = 'Signal (orig.)'
                opdesc = tab_title
                plot_title = self.channel_name + ' (' + self.orig_splot_type_lab + ')'
                #plot_title = #eval_subplot_title(self.channelset_name, self.channel_xfield, self.channel_yfield, self.channel_name, self.orig_splot_type_lab)
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                # first opdesc (in logs), then plot_title (in subplot_title); typically, it's fine to have them identical
                #addplot_orig_sign addplot_qq_sign
                o_xlabel = orig_xlabel + ' (downsampled: ' + str(self.num_time_samples_pre) + ' ->' + str(self.num_time_samples) + ')' if (self.downsampled) else orig_xlabel
                addplot_orig_sign(self.config, opdesc, o_xlabel, self.channelset_name, orig_ylabel, plot_title, targetAxes, self.time, self.signal, self.sig_time_window, self.sig_ampl_limits,
                                  incl_envelope, self.signal_peaks, include_sig_filtered, self.signal_filtered)
                subplots_dict['orig'] = targetAxes

            #### applies to ALL plots having frequency in the x-axis, except the wavelet transform
            frequency_grain = get_freq_xgrain(self.config)
            logger.debug('frequency grain set: ' + str(frequency_grain))

            # Plot the Fourier transform
            if (self.incl_ft):
                tab_title = 'Fourier tr.'
                opdesc = 'Fourier transform'
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_ft(self.config, opdesc, targetAxes, self.frequencies, self.signal_fft_magnitude, frequency_grain, self.ft_freq_limits, self.ft_magn_limits, self.dc_offset_suppressed)
                subplots_dict['ft'] = targetAxes

            # Plot the QQ Plot
            if (self.incl_qq):
                tab_title = 'Q-Q Plot'
                opdesc = tab_title
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_qq_sign(self.config, opdesc, orig_ylabel, targetAxes, self.signal)
                subplots_dict['qq'] = targetAxes

            # Plot the PSD
            if (incl_psd):
                tab_title = 'PSD'
                opdesc = tab_title
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_psd(self.config, opdesc, targetAxes, self.psd_x_vals, self.psd_y_vals, frequency_grain, self.psd_freq_limits, self.psd_pow_limits, self.dc_offset_suppressed)
                subplots_dict['psd'] = targetAxes

            # Plot the values histogram
            if (self.incl_hist):
                tab_title = 'Histogram'
                opdesc = 'Values histogram'
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_histogram(self.config, opdesc, targetAxes, self.signal, self.hist_val_limits, self.hist_freq_limits, rainbow_colors)
                subplots_dict['hist'] = targetAxes

            # Plot the phase plot
            if (include_phasepl):
                tab_title = 'Fourier tr. (ph.)'
                opdesc = 'Fourier transform phase'
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_ftphase(self.config, opdesc, targetAxes, self.frequencies, self.signal_ft_phase, frequency_grain, self.ftphase_freq_limits, self.ftphase_val_limits)
                subplots_dict['ft-phase'] = targetAxes

            # Plot the wavelet transform plot
            if (include_wavelet):
                tab_title = 'Wavelet tr.'
                opdesc = 'Wavelet transform'
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_wavelet(self.config, opdesc, targetAxes, orig_xlabel, self.time, self.wv_scales, self.wavelet_transform_data, self.wavelet_type)
                subplots_dict['wvlet'] = targetAxes

            # Plot the 3d spectrogram plot
            if (self.include_3dspectrogram):
                tab_title = '3D Spectrogram'
                opdesc = tab_title
                is3D = True
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, is3D)
                addplot_3d_spectrogram(self.config, opdesc, targetAxes, orig_xlabel, self.sampling_freq, self.time, self.signal)
                subplots_dict['3dspctg'] = targetAxes

            # Plot the spectrogram plot
            if (self.include_spectrogram):
                tab_title = 'Spectrogram'
                opdesc = tab_title
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title)
                addplot_spectrogram(self.config, opdesc, targetAxes, orig_xlabel, self.sampling_freq, self.time, self.signal)
                subplots_dict['spctg'] = targetAxes

            self.plotWindowWrap.prepareForDisplay()

            logger.debug('Subplot dictionary entries: ' + str(len(subplots_dict)) + ', keys: ' + ', '.join(subplots_dict.keys()))
        else:
            logger.info('No plots created (per user request)')

        return subplots_dict

    def showPlots(self):
        logger = logging.getLogger(__name__)
        if (self.plotWindowWrap):
            self.plotWindowWrap.showPlots()
