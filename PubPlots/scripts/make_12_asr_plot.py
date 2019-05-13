## makes supplementary figures 2-a/b in SUS-16-014, the prefit background predictions and observed data in each of the 12 aggregate search regions
from __future__ import print_function
import os
import errno
from ROOT import TFile, TH1D, Math, gStyle, THStack, TLegend, TCanvas, TPad, gPad, TLatex, TLine, TGaxis
from bg_est import BGEst
from data_obs import DataObs
from obs_exp_ratio import ObsExpRatio
import CMS_lumi


plot_dir = "output/"

def make_12_asr_plot(plot_title,  lostlept, znn, qcd, data_obs, doPull=False,lumi=137):

    TH1D.SetDefaultSumw2(True)
    import tdrstyle
    tdrstyle.setTDRStyle()
    gStyle.SetPadLeftMargin(0.12)
    gStyle.SetPadRightMargin(0.08)
    gStyle.SetPadTopMargin(0.08)
    gStyle.SetPalette(1)

    ## load observed data
    hdata_obs = data_obs.hist
    gdata_obs = data_obs.graph # note that this also sets the style

    ## load BG predictions -- also sets histogram styles
    hqcd = qcd.hCV
    hznn = znn.hCV
    hlostlept = lostlept.hCV
    ## build the stacked BG histogram
    hs = THStack("hs", "")
    hs.Add(hqcd)
    hs.Add(hlostlept)
    hs.Add(hznn)
    sumBG = BGEst.sumBG( lostlept, znn, qcd) # this will set the style of the hatched error bands

    ## setup dummy BG histogram for ratio, axes
    hbg_pred = hqcd.Clone("hbg_pred")
    hbg_pred.Reset()
    hbg_pred.SetTitle("")
    hbg_pred.GetYaxis().SetTitle("Events")
    hbg_pred.SetMarkerSize(0)
    hbg_pred.SetMarkerColor(0)
    hbg_pred.SetLineWidth(0)
    hbg_pred.SetLineColor(0)
    hbg_pred.SetFillColor(0)
    hbg_pred.GetYaxis().SetLabelSize(0.048*1.24)
    hbg_pred.GetYaxis().SetTitleSize(0.05625*1.3)
    hbg_pred.GetYaxis().SetTitleOffset(0.7)
    hbg_pred.GetYaxis().SetTitleFont(42)
    hbg_pred.GetXaxis().SetLabelSize(0)
    hbg_pred.Add(hlostlept)
    hbg_pred.Add(hqcd)
    hbg_pred.Add(hznn)
    ymax = hbg_pred.GetMaximum()
    if hdata_obs.GetMaximum()>ymax:
         ymax=hdata_obs.GetMaximum()
    hbg_pred.SetMaximum(100*ymax)
    hbg_pred.SetMinimum(0.09)

    ratio = ObsExpRatio(DataObs(hdata_obs), sumBG) # note that this also sets the style
    ratio_markers = ratio.markers
    ratio_bands = ratio.bands
    pull = ratio.pull
    pull.GetXaxis().SetTitle("Aggregate search region bin number")
    pull.SetMaximum(3.2)
    pull.SetMinimum(-3.2)
    pull.GetXaxis().SetLabelSize(0.12*1.2)
    pull.GetXaxis().SetTitleSize(0.14*1.19)
    pull.GetYaxis().SetLabelSize(0.1*1.25)
    pull.GetYaxis().SetTitleSize(0.115*1.25)
    pull.GetXaxis().SetTitleOffset(0.9)
    pull.GetXaxis().SetLabelOffset(0.01)
    pull.GetYaxis().SetTitleOffset(0.275)

    hratdummy = ratio.dummy_hist
    hratdummy.GetXaxis().SetTitle("Aggregate search region bin number")
    hratdummy.SetMaximum(1.8)
    hratdummy.SetMinimum(-1.8)

    hratdummy.GetXaxis().SetLabelSize(0.12*1.4)
    hratdummy.GetXaxis().SetTitleSize(0.15*1.35)
    hratdummy.GetYaxis().SetLabelSize(0.1*1.25)
    hratdummy.GetYaxis().SetTitleSize(0.115*1.25)
    hratdummy.GetXaxis().SetTitleOffset(0.8)
    hratdummy.GetXaxis().SetLabelOffset(0.01)
    hratdummy.GetYaxis().SetTitleOffset(0.275)


    ## setup canvas and pads
    W = 800
    H = 600
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W
    canv = TCanvas("canvName","canvName", 50, 50, W, H)
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

    up_height     = 0.8  ## please tune so that the upper figures size will meet your requirement
    dw_correction = 1.30 ## please tune so that the smaller canvas size will work in your environment
    font_size_dw  = 0.1  ## please tune the font size parameter for bottom figure
    dw_height     = (1. - up_height) * dw_correction
    dw_height_offset = 0.02 ## KH, added to put the bottom one closer to the top panel

    pad1 = TPad("pad1", "top pad" , 0.0, 0.3, 1.0, 1.0)
    pad2 = TPad("pad2", "bottom pad", 0.0, 0.0, 1.0, 0.3)
    pad1.SetTickx(0)
    pad1.SetTicky(0)
    pad1.SetPad(0., 1 - up_height,    1., 1.00)
    pad1.SetFrameFillColor(0)
    pad1.SetFillColor(0)
    pad1.SetTopMargin(0.1)
    pad1.SetLeftMargin(0.1)
    pad1.SetRightMargin(0.02)
    pad1.SetLogy()
    pad1.Draw()

    pad2.SetPad(0., 0., 1., dw_height+dw_height_offset)
    pad2.SetFillColor(0)
    pad2.SetFrameFillColor(0)
    pad2.SetBottomMargin(0.35)
    pad2.SetTopMargin(0)
    pad2.SetLeftMargin(0.1)
    pad2.SetRightMargin(0.02)
    pad2.Draw()
    pad1.cd()

    ## draw graphs on top pad
    hbg_pred.Draw()
    hbg_pred.GetXaxis().SetNdivisions(12,0,0)
    hs.Draw("hist, same")
    sumBG.gFull.Draw("2, 0, same")
    gdata_obs.Draw("p, 0, same")

    ## legends
    legdata = TLegend(0.25-0.1, 0.73, 0.45-0.14, 0.85);
    legdata.SetTextSize(0.035)
    legdata.SetFillStyle(0)
    leg1 = TLegend(0.27, 0.726, 0.56, 0.86);
    leg1.SetTextSize(0.035)
    leg1.SetFillStyle(0)
    leg2 = TLegend(0.44, 0.726, 0.73, 0.86);
    leg2.SetTextSize(0.035)
    leg2.SetFillStyle(0)
    leg3 = TLegend(0.6, 0.726, 0.89, 0.86);
    leg3.SetTextSize(0.035)
    leg3.SetFillStyle(0)


    legdata.AddEntry(gdata_obs.GetName(), "Data", "pes")
    leg1.AddEntry(hznn, "Z#rightarrow#nu#bar{#nu}", "f")
    leg2.AddEntry(hlostlept, "#splitline{Lost}{lepton}", "f")
    leg3.AddEntry(hqcd, "QCD", "f")


    legdata.Draw()
    leg1.Draw()
    leg2.Draw()
    leg3.Draw()

    pad2.cd()
    if doPull:
        pull.Draw("hist")
        pull.GetXaxis().SetNdivisions(12,0,0)
        p1 = TLine(pull.GetBinLowEdge(1), 1., pull.GetBinLowEdge(pull.GetNbinsX()+1), 1.)
        p2 = TLine(pull.GetBinLowEdge(1), 2., pull.GetBinLowEdge(pull.GetNbinsX()+1), 2.)
        m1 = TLine(pull.GetBinLowEdge(1), -1., pull.GetBinLowEdge(pull.GetNbinsX()+1), -1.)
        m2 = TLine(pull.GetBinLowEdge(1), -2., pull.GetBinLowEdge(pull.GetNbinsX()+1), -2.)
        ## p1.SetLineStyle(2)
        ## p2.SetLineStyle(2)
        ## m1.SetLineStyle(2)
        ## m2.SetLineStyle(2)
        p1.Draw()
        p2.Draw()
        m1.Draw()
        m2.Draw()
        pull.Draw("hist,same")
    else:
        hratdummy.Draw("axis")
        hratdummy.GetXaxis().SetNdivisions(12,0,0)
        ratio_bands.Draw("e2, same")
        ratio_markers.Draw("p, same")
    ratiomid = TLine(hbg_pred.GetBinLowEdge(1), 0., hbg_pred.GetBinLowEdge(hbg_pred.GetNbinsX()+1), 0.)
    ratiomid.SetLineStyle(2)
    ratiomid.Draw()

    ## lines again
    ratio_max = 1.25
    if doPull:
        ratio_max = 3.2


    ## refresh everything, to be safe
    pad1.cd()
    gPad.RedrawAxis()
    rightaxis = TGaxis(12.5, 0.09, 12.5, 100*ymax, 0.09, 100*ymax, 510, "+L")
    rightaxis.SetLabelSize(0)
    rightaxis.SetNdivisions(0)
    rightaxis.Draw()
    gPad.Modified()
    gPad.Update()
    pad2.cd()
    gPad.RedrawAxis()
    gPad.Modified()
    gPad.Update()

    ## now wite CMS headers
    canv.cd()
    #lumi = 35.862345
    CMS_lumi.cmsTextSize = 0.85
    CMS_lumi.writeExtraText = False
    CMS_lumi.extraText = "   Preliminary"
    CMS_lumi.lumi_13TeV="%8.0f fb^{-1}" % lumi
    CMS_lumi.lumi_sqrtS = CMS_lumi.lumi_13TeV+ " (13 TeV)"
    iPos=0
    CMS_lumi.CMS_lumi(canv, 0, iPos)
    ## textCMS = TLatex(0.25,0.96, "  CMS ")
    ## textCMS.SetNDC()
    ## textCMS.SetTextAlign(13)
    ## textCMS.SetTextFont(52)
    ## textCMS.SetTextSize(0.038)
    ## textCMS.Draw()

    ## save plot to PDF and PNG
    try:
        os.makedirs(plot_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    gPad.Print(plot_dir+plot_title+".pdf")
    ##    gPad.Print(plot_dir+plot_title+".png")

    gPad.Close()


if __name__ == "__main__":
    import sys
    output_file = sys.argv[1]
    f_lostlept = TFile.Open(sys.argv[3])
    lostlept = BGEst(f_lostlept.Get("ASR/hCV"), f_lostlept.Get("ASR/hStatUp"), f_lostlept.Get("ASR/hStatDown"), f_lostlept.Get("ASR/hSystUp"), f_lostlept.Get("ASR/hSystDown"), 2006)
    f_znn = TFile.Open(sys.argv[4])
    znn = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"), 2002)
    f_qcd = TFile.Open(sys.argv[5])
    qcd = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"), 2001)
    f_data_obs = TFile.Open(sys.argv[6])
    data_obs = DataObs(f_data_obs.Get("ASR/hCV"))
    make_12_asr_plot(output_file,  lostlept, znn, qcd, data_obs)
