from __future__ import print_function
import os
import errno
from ROOT import TFile, TH1D, Math, gStyle, THStack, TLegend, TCanvas, TPad, gPad, TLatex, TLine, TF1
from bg_est import BGEst
from data_obs import DataObs
from obs_exp_ratio import ObsExpRatio
from agg_bins import AddHistsInQuadrature
import CMS_lumi

plot_dir = "output/"

def make_1d_pull_dist(plot_title,  lostlept, znn, qcd, data_obs,lumi=35.9):

    TH1D.SetDefaultSumw2(True)
    import tdrstyle
    tdrstyle.setTDRStyle()

    hdata_obs = data_obs.hist
    sumBG = BGEst.sumBG( lostlept, znn, qcd)
    hbg_pred = sumBG.hCV
    hbg_err_up = AddHistsInQuadrature('err_up', [sumBG.hStatUp, sumBG.hSystUp])
    hbg_err_down = AddHistsInQuadrature('err_down', [sumBG.hStatDown, sumBG.hSystDown])
    ratio = ObsExpRatio(DataObs(hdata_obs), sumBG)
    pull = ratio.pull

    hpull = TH1D("hPull", ";Pull = [N_{Obs.}-N_{Pred.}] / #sqrt{N_{Pred.}+(#deltaN_{Pred.})^{2}};N_{bins}", 25, -3.25, 3.25)
    hpull.GetXaxis().SetLabelSize(0.035)
    hpull.GetXaxis().SetTitleSize(0.035)
    hpull.GetXaxis().SetTitleOffset(1.3)
    hpull.GetXaxis().SetTitleFont(42)
    hpull.GetYaxis().SetLabelSize(0.04)
    hpull.GetYaxis().SetTitleSize(0.04)
    hpull.GetYaxis().SetTitleOffset(1.15)
    hpull.GetYaxis().SetTitleFont(42)
    hpull.GetYaxis().SetNdivisions(505)
    hpull.GetYaxis().SetTickLength(0.015)
    hpull.GetXaxis().SetTickLength(0.08)
    hpull.SetFillColor(2029)
    hpull.SetLineColor(1)
    hpull.SetLineWidth(2)
    ZerobBin=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 111, 112, 113, 114, 115, 116, 117, 118, 143, 144, 145, 146, 147, 148, 149, 150]
    OnebBin=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 119, 120, 121, 122, 123, 124, 125, 126, 151, 152, 153, 154, 155, 156, 157, 158]
    TwobBin=[21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174]
    ZeroCount=0;
    for ibin in range(pull.GetNbinsX()):
	#if hbg_pred.GetBinContent(ibin+1)<=5:
	#if ibin in TwobBin or ibin in OnebBin:
	if(hdata_obs.GetBinContent(ibin+1)>0): 
    		hpull.Fill(pull.GetBinContent(ibin+1))
	else: ZeroCount=ZeroCount+1
        if abs(pull.GetBinContent(ibin+1))>1.5:
        #if abs(hbg_pred.GetBinContent(ibin+1))<=5:
           	 print("Bin %d: Obs: %d, Pred: %3.3f, Err: %3.3f - %3.3f, Pull: %3.2f" % (ibin+1, hdata_obs.GetBinContent(ibin+1), hbg_pred.GetBinContent(ibin+1),\
                                                                                       hbg_err_up.GetBinContent(ibin+1), hbg_err_down.GetBinContent(ibin+1),\
                                                                                       pull.GetBinContent(ibin+1)) )
    print(ZeroCount)
    for ibin in range(hpull.GetNbinsX()):
        if hpull.GetBinContent(ibin+1)>0.:
            hpull.SetBinError(ibin+1,0.0001)

    if hpull.GetBinContent(hpull.GetNbinsX()+1)>0.: #and hbg_pred.GetBinContent(hpull.GetNbinsX()+1)>5:
        hpull.SetBinContent(hpull.GetNbinsX(), hpull.GetBinContent(hpull.GetNbinsX())+hpull.GetBinContent(hpull.GetNbinsX()+1))
	print(hpull.GetNbinsX()+1)
    fit = hpull.Fit("gaus")
    gStyle.SetOptFit(0)

    W = 800
    H = 800
    T = 0.08*H
    B = 0.15*H
    L = 0.12*W
    R = 0.04*W
    canv = TCanvas("pullcanv","pullcanv", 50, 50, W, H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetLeftMargin( L/W )
    canv.SetRightMargin( R/W )
    canv.SetTopMargin( T/H )
    canv.SetBottomMargin( B/H )
    canv.SetTickx(0)
    canv.SetTicky(0)
    canv.SetFrameFillColor(0)
    canv.SetFillColor(0)
    canv.SetTopMargin(0.12)
    canv.SetLeftMargin(0.1)

    hpull.Draw("hist");

    #lumi = 137.421
    #lumi =61.9
    #lumi =10.0
    #lumi =16
    #lumi =8.2
    #lumi = 7.8
    #lumi = 35.9
    #lumi = 41.529
    CMS_lumi.writeExtraText = False
    CMS_lumi.extraText = "  Preliminary"
    CMS_lumi.lumi_13TeV="%8.1f fb^{-1}" % lumi
    CMS_lumi.lumi_sqrtS = CMS_lumi.lumi_13TeV+ " (13 TeV)"
    CMS_lumi.relPosX = 0.1
    CMS_lumi.relPosY = 0.05
    CMS_lumi.cmsTextSize = 0.5
    iPos=0.75
    CMS_lumi.CMS_lumi(canv, 0, iPos)

    canv.Print(plot_dir+plot_title+".pdf")
