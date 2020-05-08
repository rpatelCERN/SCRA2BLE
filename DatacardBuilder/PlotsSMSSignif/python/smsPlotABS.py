import ROOT as rt
from array import *
from sms import *
from color import *
import CMS_lumi
class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # obsLimits is a list of opbserved limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, energy, lumi, preliminary)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary):
        # which SMS?
        self.model = sms(modelname)
        self.OBS = obsLimits
        self.EXP = expLimits
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        # create the reference empty histo
        self.emptyhisto = self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self):
        self.emptyHisto = rt.TH2D("emptyHisto", "", 1, self.model.Xmin, self.model.Xmax, 1, self.model.Ymin, self.model.Ymax)
        
    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)        

        #self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)

        self.c.SetRightMargin(0.19)
        self.c.SetTopMargin(0.08)
        self.c.SetLeftMargin(0.14)
        self.c.SetBottomMargin(0.14)

        # set x axis
        self.emptyHisto.GetXaxis().SetLabelFont(42)
        self.emptyHisto.GetXaxis().SetLabelSize(0.035)
        self.emptyHisto.GetXaxis().SetTitleFont(42)
        self.emptyHisto.GetXaxis().SetTitleSize(0.05)
        self.emptyHisto.GetXaxis().SetTitleOffset(1.2)
        self.emptyHisto.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)
	self.emptyHisto.GetXaxis().SetNdivisions(5,5,0)
        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.035)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        self.emptyHisto.GetYaxis().SetTitleOffset(1.35)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)
                
    def DrawText(self):
        #redraw axes
        self.c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.model.Xmin, self.model.Ymax)
        graphWhite.SetPoint(1,self.model.Xmax, self.model.Ymax)
        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.75)
        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.75)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
       	CMS_lumi.writeExtraText = 0
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.lumi_13TeV="137 fb^{-1}"

	CMS_lumi.lumi_sqrtS = "13 TeV"  
	iPos=0
	CMS_lumi.CMS_lumi(self.c,4, iPos)
        # CMS LABEL
	self.preliminary="Supplementary"
        textCMS = rt.TLatex(0.25,0.96,"  %s " %(self.preliminary))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(52)
        textCMS.SetTextSize(0.038)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # MODEL LABEL
        #textModelLabel= rt.TLatex(0.15,0.90,"%s Approx NNLO+NNLL exclusion" %self.model.label)
        textModelLabel= rt.TLatex(0.3,0.85,"%s " %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.045)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        # NLO NLL XSEC
        textNLONLL= rt.TLatex(0.35,0.9,"arXiv:1908.04722")
        textNLONLL.SetNDC()
        textNLONLL.SetTextAlign(13)
        textNLONLL.SetTextFont(52)
        textNLONLL.SetTextSize(0.035)
        textNLONLL.Draw()
	self.c.textNLONLL=textNLONLL
	#textChi= rt.TLatex(0.16,0.2,"m_{{#tilde{#chi}^{\pm}_1}/{#tilde{#chi}^{0}_2}}")
	textChi= rt.TLatex(0.16,0.70, "m_{#tilde{#chi}_{1}^{#pm}/#tilde{#chi}_{2}^{0}}=0.5 (m_{#tilde{#chi}_{1}^{0}}+ m_{#tilde{g}} )")
        textChi.SetNDC()
        textChi.SetTextAlign(13)
        textChi.SetTextFont(42)
        textChi.SetTextSize(0.035)
	#print "m_{{#tilde{#chi}^{\pm}_1}/{#tilde{#chi}^{0}_2}}"
	#textChi.Draw()
        #self.c.NLONLL = textChi

    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        
    def DrawLegend(self):
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LObs = rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(color(self.OBS['colorLine']))
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)

        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(color(self.OBS['colorLine']))
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10)

        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(color(self.OBS['colorLine']))
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10)

        textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)  
        LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10)

        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)  
        LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10)
        LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10)

        textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp

        LObs.Draw("LSAME")
        LObsM.Draw("LSAME")
        LObsP.Draw("LSAME")
        LExp.Draw("LSAME")
        LExpM.Draw("LSAME")
        LExpP.Draw("LSAME")
        
        self.c.LObs = LObs
        self.c.LObsM = LObsM
        self.c.LObsP = LObsP
        self.c.LExp = LExp
        self.c.LExpM = LExpM
        self.c.LExpP = LExpP

    def DrawDiagonal(self):
	diagonal=rt.TGraph(3)
        diagonal.SetName("diagonal")
	diagonal2=rt.TGraph(128)
        diagonal2.SetName("diagonal2")
	for i in range(0,152):
		x=float((i*12.5)+600)
		#x=float((i*12.5)+150)
		#y=float((i*12.5)+80)
		y=float((i*12.5)+475)
		#FOR T2tt
		#x=float((i*12.5)+150)
		#y=float((i*12.5)+75-10)
		y2=float((i*12.5)+400-170)
		diagonal.SetPoint(diagonal.GetN(), x,y)
		#diagonal2.SetPoint(diagonal2.GetN(),x,y2)
	#diagonal.SetPoint(diagonal.GetN(), 150,2000);
	#diagonal.SetPoint(diagonal.GetN(), 150,80);
	diagonal.SetPoint(diagonal.GetN(), 600,2000);
	diagonal.SetPoint(diagonal.GetN(), 600,475);
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        #diagonal2=rt.TGraph(4)
        x1 = self.model.Xmin ## = 150
        y1 = self.model.Ymin ## = 0

        ## lower right corner
        x2 = self.model.Xmin+50. ## = 200
        y2 = self.model.Ymin     ## = 0

        ## upper right corner
        x3 = self.model.Xmin+137.5 ## = 287.5
        y3 = self.model.Ymin+87.5  ## = 87.5

        ## upper left corner
        x4 = self.model.Xmin+112.5 ## = 262.5
        y4 = self.model.Ymin+112.5 ## = 112.5

        diagonal2 = rt.TGraph(4, array('d',[x1,x2,x3,x4]), array('d',[y1,y2,y3,y4]))
 
        #diagonal2.SetPoint(diagonal2.GetN(), 800, 0);
        #diagonal2.SetPoint(diagonal2.GetN(), 800,25);
        #diagonal2.SetPoint(diagonal2.GetN(), 2200, 25);
        #diagonal2.SetPoint(diagonal2.GetN(), 2200, 0);
        diagonal.Draw("FSAME")
        #diagonal.Draw("LSAME")
        diagonal2.SetLineColor(rt.kGray)
        diagonal2.SetLineStyle(2)
        diagonal2.SetFillColor(rt.kWhite)

        diagonal2.Draw("FSame")
        self.c.diagonal = diagonal
        #self.c.diagonal2=diagonal2
	self.c.Update

    def DrawLines(self):
        # observed
        self.OBS['nominal'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['nominal'].SetLineStyle(1)
        self.OBS['nominal'].SetLineWidth(4)
        # observed + 1sigma
        self.OBS['plus'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['plus'].SetLineStyle(1)
        self.OBS['plus'].SetLineWidth(2)        
        # observed - 1sigma
        self.OBS['minus'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['minus'].SetLineStyle(1)
        self.OBS['minus'].SetLineWidth(2)        
        # expected + 1sigma
        self.EXP['plus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['plus'].SetLineStyle(7)
        self.EXP['plus'].SetLineWidth(2)                
        # expected
        self.EXP['nominal'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['nominal'].SetLineStyle(7)
        self.EXP['nominal'].SetLineWidth(4)        
        # expected - 1sigma
        self.EXP['minus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['minus'].SetLineStyle(7)
        self.EXP['minus'].SetLineWidth(2)                        
        # DRAW LINES
        self.EXP['nominal'].Draw("LSAME")
        self.EXP['plus'].Draw("LSAME")
        self.EXP['minus'].Draw("LSAME")
        self.OBS['nominal'].Draw("LSAME")
        self.OBS['plus'].Draw("LSAME")
        self.OBS['minus'].Draw("LSAME")        

        
