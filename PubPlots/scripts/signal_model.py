#!/usr/bin/python
## Very simple class for accessing signal histograms given model name and mother and LPS masses

from ROOT import TFile, gROOT, TH1D
from array import array

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
        fname = "inputs/sig_hists/%s.root" % self.model
        # if we've already opened the file, just return the pointer already in memory, else create it
        if gROOT.GetListOfFiles().FindObject(fname) == None: 
            return TFile.Open(fname)
        else:
            return gROOT.GetListOfFiles().FindObject(fname)
        
    def GetInputHist(self): # returns histogram loaded from input file
        hname = "RA2bin_%s_%d_%d_fast" % (self.model, int(self.mMom), int(self.mLSP))        
        return self.infile.Get(hname)

    def AggregateBins(self, agg_bins, xaxis_title=None, xaxis_binning=None): # creates a histogram from aggregated bins -- this is used in fill_signal_hists.py
        ## can define the x-axis here if you want
        if xaxis_title != None and xaxis_binning!=None:
            hagg = TH1D(self.inhist.GetName(), ";"+xaxis_title, len(xaxis_binning)-1, array('d', xaxis_binning))
        else:
            hagg = TH1D(self.inhist.GetName(), "", len(agg_bins), 0.5, float(len(agg_bins))+0.5)
        for iasr in range(len(agg_bins)):
            asr_yield = 0.
            for isub in range(len(agg_bins[iasr])):
                asr_yield += self.inhist.GetBinContent(agg_bins[iasr][isub]) # note: agg_bins[iasr][isub] index runs from 1 to nbins -- no need to add 1
            hagg.SetBinContent(iasr+1, asr_yield)
        return hagg
    
    @classmethod
    def GetASRHist(cls, asr_name, model, mMom, mLSP, asr_file='signal_hists.root'): # returns ASR histogram that we made by running fill_signal_hists.py, specified by asr_file
        if gROOT.GetListOfFiles().FindObject(asr_file):
            f_asr = TFile.Open(asr_file)
        else:
            f_asr = gROOT.GetListOfFiles().FindObject(asr_file)
        hname = "%s/RA2bin_%s_%d_%d_fast" % (asr_name, model, int(mMom), int(mLSP))
        return cls(f_asr.Get(hname))

    
