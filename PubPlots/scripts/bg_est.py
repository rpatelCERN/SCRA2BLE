from ROOT import TH1D, TGraphAsymmErrors
import math
from array import array
import tdrstyle

## two ways to build prediction:
        ## 1) Default: from a bunch of histograms (i.e. for a single background)
        ## 2) SumBG: from a bunch of predictions (i.e. for the total BG prediction)

class BGEst:
    def __init__(self, CV, statUp, statDown, systUp, systDown, hist_color = None):
        self.set_vars(CV, statUp, statDown, systUp, systDown, hist_color)
    
    def set_vars(cls, CV, statUp, statDown, systUp, systDown, hist_color):
        cls.nbins = CV.GetNbinsX()
        cls.hCV  = CV
        if hist_color != None:
            cls.hCV.SetFillColor(hist_color)
        cls.hCV.SetLineColor(1)
        cls.hCV.SetLineWidth(2)
        cls.hStatUp    = statUp
        cls.hStatDown    = statDown
        cls.hSystUp    = systUp
        cls.hSystDown     = systDown
        cls.gStat = cls.GetTGraph(CV, 'gStat', statUp, statDown)
        cls.gSyst = cls.GetTGraph(CV, 'gSyst', systUp, systDown)
        cls.gFull = cls.GetTGraph(CV, 'gFull', statUp, statDown, systUp, systDown)
        # set the full TGraph's style (hatched BG uncertainty bands)
        cls.gFull.SetFillColor(14)
        cls.gFull.SetMarkerSize(0)
        cls.gFull.SetLineWidth(0)
        cls.gFull.SetLineColor(0)
        cls.gFull.SetFillStyle(3445)

    def GetTGraph(cls, CV, gname, errUp, errDown, errUp2 = None, errDown2 = None):
        x = []
        y = []
        ex_l = []
        ex_h = []
        ey_l = []
        ey_h = []
        for ibin in range(cls.nbins):
            x.append(CV.GetBinCenter(ibin+1))
            ex_l.append(CV.GetBinWidth(ibin+1) / 2.)
            ex_h.append(CV.GetBinWidth(ibin+1) / 2.)
            y.append(CV.GetBinContent(ibin+1))
            if errDown2 != None:
                ey_l.append(math.sqrt(errDown.GetBinContent(ibin+1)**2 + errDown2.GetBinContent(ibin+1)**2))
            else:
               ey_l.append(errDown.GetBinContent(ibin+1))
            if errUp2 != None:
                ey_h.append(math.sqrt(errUp.GetBinContent(ibin+1)**2 + errUp2.GetBinContent(ibin+1)**2))
            else:
               ey_h.append(errUp.GetBinContent(ibin+1))
        gbg = TGraphAsymmErrors(cls.nbins, array('d', x), array('d', y), array('d', ex_l), array('d', ex_h), array('d', ey_l), array('d', ey_h))
        gbg.SetName(gname)
        return gbg
      
      
    @classmethod
    def sumBG(cls, lostlep, hadtau, znn, qcd): # in this case, sum the four BGs up accordingly
        xbins = lostlep.hCV.GetXaxis().GetXbins()
        if xbins.GetSum() == 0.0:
            hSumBGCV = TH1D("hSumBGCV", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), 0.5, int(lostlep.nbins)+0.5)
            hSumBGStatUp = TH1D("hSumBGStatUp", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), 0.5, int(lostlep.nbins)+0.5)
            hSumBGStatDown = TH1D("hSumBGStatDown", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), 0.5, int(lostlep.nbins)+0.5)
            hSumBGSystUp = TH1D("hSumBGSystUp", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), 0.5, int(lostlep.nbins)+0.5)
            hSumBGSystDown = TH1D("hSumBGSystDown", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), 0.5, int(lostlep.nbins)+0.5)
        else:
            hSumBGCV = TH1D("hSumBGCV", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), xbins.GetArray())
            hSumBGStatUp = TH1D("hSumBGStatUp", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), xbins.GetArray())
            hSumBGStatDown = TH1D("hSumBGStatDown", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), xbins.GetArray())
            hSumBGSystUp = TH1D("hSumBGSystUp", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), xbins.GetArray())
            hSumBGSystDown = TH1D("hSumBGSystDown", ";"+lostlep.hCV.GetXaxis().GetTitle(), int(lostlep.nbins), xbins.GetArray())
            
        for ibin in range(lostlep.nbins):
            cv = lostlep.hCV.GetBinContent(ibin+1)+hadtau.hCV.GetBinContent(ibin+1)+znn.hCV.GetBinContent(ibin+1)+qcd.hCV.GetBinContent(ibin+1)
            hSumBGCV.SetBinContent(ibin+1, cv)
            stat_up = lostlep.hStatUp.GetBinContent(ibin+1)+hadtau.hStatUp.GetBinContent(ibin+1) # treat as fully correlated, add these linearly
            stat_up = math.sqrt(stat_up**2 + znn.hStatUp.GetBinContent(ibin+1)**2 + qcd.hStatUp.GetBinContent(ibin+1)**2)
            hSumBGStatUp.SetBinContent(ibin+1, stat_up)
            stat_down = lostlep.hStatDown.GetBinContent(ibin+1)+hadtau.hStatDown.GetBinContent(ibin+1) # treat as fully correlated, add these linearly
            stat_down = math.sqrt(stat_down**2 + znn.hStatDown.GetBinContent(ibin+1)**2 + qcd.hStatDown.GetBinContent(ibin+1)**2)
            hSumBGStatDown.SetBinContent(ibin+1, stat_down)
            syst_up = math.sqrt(lostlep.hSystUp.GetBinContent(ibin+1)**2 + hadtau.hSystUp.GetBinContent(ibin+1)**2 + znn.hSystUp.GetBinContent(ibin+1)**2 + qcd.hSystUp.GetBinContent(ibin+1)**2)
            hSumBGSystUp.SetBinContent(ibin+1, syst_up)
            syst_down = math.sqrt(lostlep.hSystDown.GetBinContent(ibin+1)**2 + hadtau.hSystDown.GetBinContent(ibin+1)**2 + znn.hSystDown.GetBinContent(ibin+1)**2 + qcd.hSystDown.GetBinContent(ibin+1)**2)
            hSumBGSystDown.SetBinContent(ibin+1, syst_down)
        return cls(hSumBGCV, hSumBGStatUp, hSumBGStatDown, hSumBGSystUp, hSumBGSystDown)
