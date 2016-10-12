#!/usr/bin/python
## get the two ratio TGraphs :
## 1 -- the markers with statistical uncertainties from data
## 2 -- the bands around ratio = 1 with BG estimation uncertainty
## this will set the style for both

from ROOT import TH1D, TGraphAsymmErrors, TStyle, Math
from array import array
from bg_est import BGEst
from data_tgraph import DataGraph


class DataMCRatio:

    def __init__(self, data_obs, bg_pred):
        self.set_vars(data_obs, bg_pred)
        
    def set_vars(cls, data_obs, bg_pred):
        cls.markers = cls.GetRatioMarkers(data_obs, bg_pred)
        cls.bands = cls.GetRatioBands(data_obs, bg_pred)
        cls.dummy_hist = cls.GetDummyHist(data_obs)
        
    def GetRatioMarkers(cls, data_obs, bg_pred):
        x = []
        y = []
        ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        nbins = data_obs.hist.GetNbinsX()
        for ibin in range(nbins):
            if bg_pred.hCV.GetBinContent(ibin+1)>0 and data_obs.hist.GetBinContent(ibin+1)>0:
                x.append(data_obs.hist.GetBinCenter(ibin+1))
                ex_l.append(0.0001)
                ex_h.append(0.0001)
                y.append( (data_obs.hist.GetBinContent(ibin+1)-bg_pred.hCV.GetBinContent(ibin+1))/bg_pred.hCV.GetBinContent(ibin+1) )
                ey_l.append(data_obs.graph.GetErrorYlow(ibin)/bg_pred.hCV.GetBinContent(ibin+1))
                ey_h.append(data_obs.graph.GetErrorYhigh(ibin)/bg_pred.hCV.GetBinContent(ibin+1))
            else: # 0 estimated
                y.append(-999.)
                ey_l.append(0.0001)
                ey_h.append(0.0001)
                                    

        gMarkers = TGraphAsymmErrors(nbins, array('d', x), array('d', y), array('d', ex_l), array('d', ex_h), array('d', ey_l), array('d', ey_h))
        gMarkers.SetName("gMarkers")
        gMarkers.SetMarkerSize(1)
        gMarkers.SetLineWidth(1)
        gMarkers.SetMarkerStyle(20)
        gMarkers.SetLineColor(1)
        return gMarkers

    def GetRatioBands(cls, data_obs, bg_pred):
        x = []
        y = []
        ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        nbins = data_obs.hist.GetNbinsX()
        for ibin in range(nbins):
            if bg_pred.hCV.GetBinContent(ibin+1)>0:
                x.append(data_obs.hist.GetBinCenter(ibin+1))
                ex_l.append(bg_pred.hCV.GetBinWidth(ibin+1)/2.)
                ex_h.append(bg_pred.hCV.GetBinWidth(ibin+1)/2.)
                y.append(0.)
                ey_l.append(bg_pred.gFull.GetErrorYlow(ibin)/bg_pred.hCV.GetBinContent(ibin+1))
                ey_h.append(bg_pred.gFull.GetErrorYhigh(ibin)/bg_pred.hCV.GetBinContent(ibin+1))
            else: # 0 estimated
                y.append(0.)
                ey_l.append(0.)
                ey_h.append(5.)
                                    

        gBands = TGraphAsymmErrors(nbins, array('d', x), array('d', y), array('d', ex_l), array('d', ex_h), array('d', ey_l), array('d', ey_h))
        gBands.SetFillColor(14)
        gBands.SetMarkerSize(0)
        gBands.SetLineWidth(0)
        gBands.SetLineColor(0)
        gBands.SetFillStyle(3445)
        return gBands

    def GetDummyHist(cls, data_obs): ## for drawing axes
        hratdummy = data_obs.hist.Clone("hratdummy")
        hratdummy.Reset()
        hratdummy.SetStats(0)
        hratdummy.SetFillColor(0)
        hratdummy.SetFillStyle(0)
        hratdummy.GetYaxis().SetTitle("#frac{(Obs.-Exp.)}{Exp.}")
        hratdummy.GetXaxis().SetLabelSize(0.15)
        hratdummy.GetXaxis().SetLabelOffset(0.03)
        hratdummy.GetXaxis().SetTitleSize(0.14)
        hratdummy.GetXaxis().SetTitleOffset(1.1)
        hratdummy.GetYaxis().SetLabelSize(0.13)
        hratdummy.GetYaxis().SetTitleSize(0.13)
        hratdummy.GetYaxis().SetTitleOffset(0.32)
        hratdummy.GetYaxis().SetNdivisions(505)
        hratdummy.GetYaxis().SetTickLength(0.015)
        hratdummy.GetXaxis().SetTickLength(0.08)
        return hratdummy

    
