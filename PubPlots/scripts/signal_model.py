#!/usr/bin/python
## Very simple class for accessing signal histograms given model name and mother and LPS masses

from ROOT import TFile, gROOT, TH1D
from array import array
from math import sqrt

alpha = 1 - 0.6827

class SignalModel:

    def __init__(self, model, mMom, mLSP):
        self.set_vars(model, mMom, mLSP)
        
    def set_vars(self, model, mMom, mLSP):
        self.model = model
        self.mMom = mMom
        self.mLSP = mLSP
        self.infile = self.GetInputFile()
        self.inhist = self.GetInputHist()

    def GetInputFile(self): # returns pointer to Kevin's file containing signal input
        #fname = "../DatacardBuilder/inputHistograms/fastsimSignal%s/RA2bin_proc_%s_%d_%d_fast.root" % (self.model, self.model, int(self.mMom), int(self.mLSP))
        #fname = "inputs/signal_hists/inputHistograms/fastsimSignal%s/RA2bin_proc_%s_%d_%d_fast.root" % (self.model, self.model, int(self.mMom), int(self.mLSP))
	fname="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV16_v6/RA2bin_proc_%s_%d_%d_MC2017_fast.root"% (self.model, int(self.mMom), int(self.mLSP))
        #fname = "inputs/signal_hists/inputHistograms/FullSIM/RA2bin_proc_%s_%d_%d_MC2017.root" % (self.model, int(self.mMom), int(self.mLSP))
        # if we've already opened the file, just return the pointer already in memory, else create it
        if gROOT.GetListOfFiles().FindObject(fname) == None: 
            return TFile.Open(fname)
        else:
            return gROOT.GetListOfFiles().FindObject(fname)
        
    def GetInputHist(self): # returns histogram loaded from input file
        hname = "RA2bin_%s_%d_%d_MC2017_fast_nominal" % (self.model, int(self.mMom), int(self.mLSP))
        return self.infile.Get(hname)

    def AggregateBins(self, agg_bins, xaxis_title=None, xaxis_binning=None): # creates a histogram from aggregated bins -- this is used in fill_signal_hists.py
        ## can define the x-axis here if you want
        if xaxis_title != None and xaxis_binning!=None:
            hagg = TH1D(self.inhist.GetName(), ";"+xaxis_title, len(xaxis_binning)-1, array('d', xaxis_binning))
        else:
            hagg = TH1D(self.inhist.GetName(), "", len(agg_bins), 0.5, float(len(agg_bins))+0.5)
        for iasr in range(len(agg_bins)):
            asr_yield = 0.
            asr_err = 0.
            for isub in range(len(agg_bins[iasr])):
                asr_yield += self.inhist.GetBinContent(agg_bins[iasr][isub]+1)
                asr_err += self.inhist.GetBinError(agg_bins[iasr][isub]+1)**2
            hagg.SetBinContent(iasr+1, asr_yield)
            hagg.SetBinError(iasr+1, sqrt(asr_err))
        return hagg
    
    @classmethod
    def GetASRHist(cls, asr_name, model, mMom, mLSP, asr_file='signal_hists.root'): # returns ASR histogram that we made by running fill_signal_hists.py, specified by asr_file
        if gROOT.GetListOfFiles().FindObject(asr_file):
            f_asr = TFile.Open(asr_file)
        else:
            f_asr = gROOT.GetListOfFiles().FindObject(asr_file)
        hname = "%s/RA2bin_%s_%d_%d_fast" % (asr_name, model, int(mMom), int(mLSP))
        return cls(f_asr.Get(hname))

    
