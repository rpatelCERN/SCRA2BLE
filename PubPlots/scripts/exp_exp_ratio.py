#!/usr/bin/python
## get the two ratio TGraphs :
## 1 -- the markers with statistical uncertainties from data
## 2 -- the bands around ratio = 1 with BG estimation uncertainty
## this will set the style for both

from ROOT import TH1D, TGraphAsymmErrors, TStyle, Math, TColor
from array import array
from math import sqrt
from bg_est import BGEst
from data_obs import DataObs


class ExpExpRatio:

    def __init__(self,bkg_pred1, bkg_pred2):
        self.set_vars(bkg_pred1, bkg_pred2)
        
    def set_vars(self, bkg_pred1, bkg_pred2):
        self.bkg_pred1 =bkg_pred1
        self.bkg_pred2 =bkg_pred2
        #self.markers = self.GetRatioMarkers()
        self.bands = self.GetRatioBands()
        self.pull = self.GetPullDist()
        self.dummy_hist = self.GetDummyHist()
    '''
    def GetRatioMarkers(self):
        x = []
        y = []
       ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        nbins = self.bkg_pred1.hCV.GetNbinsX()
        for ibin in range(nbins):
            x.append(self.bkg_pred1.hCV.GetBinCenter(ibin+1))
            ex_l.append(0.0001)
            ex_h.append(0.0001)
            if self.bkg_pred2.hCV.GetBinContent(ibin+1)>0 and self.bkg_pred1.hCV.GetBinContent(ibin+1)>0:                
                y.append( (self.bkg_pred1.hCV.GetBinContent(ibin+1)-self.bkg_pred2.hCV.GetBinContent(ibin+1))/self.bkg_pred2.hCV.GetBinContent(ibin+1) )
                ey_l.append(self.bkg_pred1.graph.GetErrorYlow(ibin)/self.bkg_pred2.hCV.GetBinContent(ibin+1))
                ey_h.append(self.bkg_pred1.graph.GetErrorYhigh(ibin)/self.bkg_pred2.hCV.GetBinContent(ibin+1))
                # if y[-1]> 3.45 or y[-1]<-1: print ibin+1, y[-1], "+", ey_h[-1], "-", ey_l[-1]
                ## print("Bin %d -- Obs: %3.0f, Exp: %3.2f, Rat: %3.2f" % (ibin+1, self.data_obs.hCV.GetBinContent(ibin+1), self.bkg_pred2.hCV.GetBinContent(ibin+1), y[ibin]))
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
    '''
    def GetRatioBands(self):
        x = []
        y = []
        ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        nbins = self.bkg_pred1.hCV.GetNbinsX()
        for ibin in range(nbins):
            if self.bkg_pred2.hCV.GetBinContent(ibin+1)>0:
                x.append(self.bkg_pred1.hCV.GetBinCenter(ibin+1))
                ex_l.append(self.bkg_pred2.hCV.GetBinWidth(ibin+1)/2.)
                ex_h.append(self.bkg_pred2.hCV.GetBinWidth(ibin+1)/2.)
                y.append(0.)
                ey_l.append(self.bkg_pred2.gFull.GetErrorYlow(ibin)/self.bkg_pred2.hCV.GetBinContent(ibin+1))
                ey_h.append(self.bkg_pred2.gFull.GetErrorYhigh(ibin)/self.bkg_pred2.hCV.GetBinContent(ibin+1))
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

    def GetDummyHist(self): ## for drawing axes
        hratdummy = self.bkg_pred1.hCV.Clone("hratdummy")
        hratdummy.Reset()
        hratdummy.SetStats(0)
        hratdummy.SetFillColor(0)
        hratdummy.SetFillStyle(0)
        hratdummy.GetYaxis().SetTitle("#frac{Obs.-Exp.}{Exp.}")
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
        hratdummy.GetXaxis().SetTitle(self.bkg_pred2.hCV.GetXaxis().GetTitle())
        return hratdummy

    def GetPullDist(self): # this will just be a TH1 of markers with no error bars
        hpull = self.bkg_pred1.hCV.Clone("hpull")
        hpull.Reset()
        hpull.SetStats(0)
        hpull.GetYaxis().SetTitle("Pull   ")
        hpull.GetXaxis().SetLabelSize(0.15)
        hpull.GetXaxis().SetLabelOffset(0.03)
        hpull.GetXaxis().SetTitleSize(0.14)
        hpull.GetXaxis().SetTitleOffset(1.1)
        hpull.GetYaxis().SetLabelSize(0.13)
        hpull.GetYaxis().SetTitleSize(0.13)
        hpull.GetYaxis().SetTitleOffset(0.32)
        hpull.GetYaxis().SetNdivisions(505)
        hpull.GetYaxis().SetTickLength(0.015)
        hpull.GetXaxis().SetTickLength(0.08)
        hpull.SetMarkerSize(1)
        hpull.SetLineWidth(1)
        hpull.SetMarkerStyle(20)
        hpull.SetLineColor(1)
        #hpull.SetFillColor(880-4)
        hpull.SetFillColor(14)
        hpull.GetXaxis().SetTitle(self.bkg_pred2.hCV.GetXaxis().GetTitle())
        for ibin in range(hpull.GetNbinsX()):
            pull = 0.
            if self.bkg_pred2.hCV.GetBinContent(ibin+1) < self.bkg_pred1.hCV.GetBinContent(ibin+1): # obs high
                pull = (self.bkg_pred1.hCV.GetBinContent(ibin+1)-self.bkg_pred2.hCV.GetBinContent(ibin+1))/sqrt(self.bkg_pred2.gFull.GetErrorYhigh(ibin)**2 + self.bkg_pred2.hCV.GetBinContent(ibin+1))
            elif self.bkg_pred2.hCV.GetBinContent(ibin+1) > self.bkg_pred1.hCV.GetBinContent(ibin+1): # obs low
                pull = (self.bkg_pred1.hCV.GetBinContent(ibin+1)-self.bkg_pred2.hCV.GetBinContent(ibin+1))/sqrt(self.bkg_pred2.gFull.GetErrorYlow(ibin)**2 + self.bkg_pred2.hCV.GetBinContent(ibin+1))
	    print "Pull %g" %pull
            hpull.SetBinContent(ibin+1, pull)
            hpull.SetBinError(ibin+1, 0.)
        return hpull
        
