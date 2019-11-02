#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: grc_cc1111_hackrf_receiver
# Author: Jerome Nokin
# Generated: Sat Nov  2 20:21:35 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cc1111
import math
import osmosdr
import time
import wx


class grc_cc1111_hackrf_receiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="grc_cc1111_hackrf_receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 80000
        self.samp_rate = samp_rate = 2e06
        self.firdes_transition_width = firdes_transition_width = 15000
        self.firdes_cuttoff = firdes_cuttoff = 21e3
        self.samp_per_sym = samp_per_sym = int(samp_rate / symbole_rate)
        self.rat_interop = rat_interop = 8
        self.rat_decim = rat_decim = 5
        self.myqueue_out = myqueue_out = gr.msg_queue(2)
        self.frequency_shift = frequency_shift = 520000
        self.frequency_center = frequency_center = 433.6e06
        self.firdes_filter = firdes_filter = firdes.low_pass(1,samp_rate/2, firdes_cuttoff, firdes_transition_width)
        self.firdes_decim = firdes_decim = 4
        self.access_code = access_code = '11010011100100011101001110010001'

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0_1 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency_center,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=5120,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Source",
        	win=window.rectangular,
        )
        self.Add(self.wxgui_waterfallsink2_0_1.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency_center,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=5120,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Filter",
        	win=window.rectangular,
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rat_interop,
                decimation=rat_decim,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "hackrf=1" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frequency_center-frequency_shift, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(2, (1, ), frequency_shift, samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(firdes_decim, (firdes_filter), 0, samp_rate/2)
        self.digital_correlate_access_code_bb_0_0 = digital.correlate_access_code_bb(access_code, 1)
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0_0_0 = digital.binary_slicer_fb()
        self.cc1111_cc1111_packet_decoder_0 = cc1111.cc1111_packet_decoder(myqueue_out,True, False, True, False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/home/bkbilly/Desktop/hello_out.txt", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))    
        self.connect((self.cc1111_cc1111_packet_decoder_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0_0_0, 0), (self.digital_correlate_access_code_bb_0_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.digital_binary_slicer_fb_0_0_0, 0))    
        self.connect((self.digital_correlate_access_code_bb_0_0, 0), (self.cc1111_cc1111_packet_decoder_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_waterfallsink2_0_1, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))    

    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1.set_sample_rate(self.samp_rate)

    def get_firdes_transition_width(self):
        return self.firdes_transition_width

    def set_firdes_transition_width(self, firdes_transition_width):
        self.firdes_transition_width = firdes_transition_width
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))

    def get_firdes_cuttoff(self):
        return self.firdes_cuttoff

    def set_firdes_cuttoff(self, firdes_cuttoff):
        self.firdes_cuttoff = firdes_cuttoff
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0_0.set_omega(self.samp_per_sym*(1+0.0))

    def get_rat_interop(self):
        return self.rat_interop

    def set_rat_interop(self, rat_interop):
        self.rat_interop = rat_interop

    def get_rat_decim(self):
        return self.rat_decim

    def set_rat_decim(self, rat_decim):
        self.rat_decim = rat_decim

    def get_myqueue_out(self):
        return self.myqueue_out

    def set_myqueue_out(self, myqueue_out):
        self.myqueue_out = myqueue_out

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.frequency_shift)
        self.osmosdr_source_0.set_center_freq(self.frequency_center-self.frequency_shift, 0)

    def get_frequency_center(self):
        return self.frequency_center

    def set_frequency_center(self, frequency_center):
        self.frequency_center = frequency_center
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.frequency_center)
        self.osmosdr_source_0.set_center_freq(self.frequency_center-self.frequency_shift, 0)
        self.wxgui_waterfallsink2_0_1.set_baseband_freq(self.frequency_center)

    def get_firdes_filter(self):
        return self.firdes_filter

    def set_firdes_filter(self, firdes_filter):
        self.firdes_filter = firdes_filter
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.firdes_filter))

    def get_firdes_decim(self):
        return self.firdes_decim

    def set_firdes_decim(self, firdes_decim):
        self.firdes_decim = firdes_decim

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code


def main(top_block_cls=grc_cc1111_hackrf_receiver, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
