#!/usr/bin/python
## stores a TGraphAsymmErrors of the observed data with proper poisson uncertainties, as well as the original histogram
## TH1::SetBinErrorOption(TH1::kPoisson) doesn't seem to work in some vrsions of root


from ROOT import TH1D, TGraphAsymmErrors, TStyle, Math
from array import array

alpha = 1 - 0.6827

class DataObs:

    def __init__(self, hdata_obs):
        self.set_vars(hdata_obs)
        
    def set_vars(self, hdata_obs):
        self.hist = hdata_obs.Clone("hCV")
        self.graph = self.GetTGraph(hdata_obs)
        
    def GetTGraph(self, hdata_obs):
        x = []
        y = []
        ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        nbins = hdata_obs.GetNbinsX()
        for ibin in range(nbins):
            nObs = hdata_obs.GetBinContent(ibin+1)
            x.append(hdata_obs.GetBinCenter(ibin+1))
            ex_l.append(0.0001)
            ex_h.append(0.0001)
            y.append(nObs)
            L = 0.
            if nObs > 0.:
                L = Math.gamma_quantile(alpha/2, nObs, 1.)
            U = Math.gamma_quantile_c(alpha/2, nObs+1., 1.)
            ey_l.append(nObs-L)
            ey_h.append(U-nObs)
        gData = TGraphAsymmErrors(nbins, array('d', x), array('d', y), array('d', ex_l), array('d', ex_h), array('d', ey_l), array('d', ey_h))
        gData.SetName("g_"+self.hist.GetName())
        gData.SetMarkerSize(1)
        gData.SetLineWidth(1)
        gData.SetMarkerStyle(20)
        gData.SetLineColor(1)
        return gData

    def AggregateBins(self, agg_bins, xaxis_title=None, xaxis_binning=None):
        ## can define the x-axis here if you want
        if xaxis_title != None and xaxis_binning!=None:
            hagg = TH1D(self.hist.GetName(), ";"+xaxis_title, len(xaxis_binning)-1, array('d', xaxis_binning))
        else:
            hagg = TH1D("hCV", "", len(agg_bins), 0.5, float(len(agg_bins))+0.5)
        for iasr in range(len(agg_bins)):
            asr_yield = 0.
            for isub in range(len(agg_bins[iasr])):
                asr_yield += self.hist.GetBinContent(agg_bins[iasr][isub]) # note: agg_bins[iasr][isub] index runs from 1 to nbins -- no need to add 1
            hagg.SetBinContent(iasr+1, asr_yield)
        return DataObs(hagg)
        
