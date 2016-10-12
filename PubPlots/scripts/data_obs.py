#!/usr/bin/python
## stores a TGraphAsymmErrors of the observed data with proper poisson uncertainties, as well as the original histogram
## TH1::SetBinErrorOption(TH1::kPoisson) doesn't seem to work in some vrsions of root


from ROOT import TH1D, TGraphAsymmErrors, TStyle, Math
from array import array

alpha = 1 - 0.6827

class DataObs:

    def __init__(self, hdata_obs):
        self.set_vars(hdata_obs)
        
    def set_vars(cls, hdata_obs):
        cls.hist = hdata_obs
        cls.graph = cls.GetTGraph(hdata_obs)
        
    def GetTGraph(cls, hdata_obs):
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
        gData.SetName("gData")
        gData.SetMarkerSize(1)
        gData.SetLineWidth(1)
        gData.SetMarkerStyle(20)
        gData.SetLineColor(1)
        return gData

