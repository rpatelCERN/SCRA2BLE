from __future__ import print_function
import os
import errno
from ROOT import TFile, TH1D, Math, gStyle, THStack, TLegend, TCanvas, TPad, gPad, TLatex, TLine
from bg_est import BGEst
from data_obs import DataObs
from data_mc_ratio import DataMCRatio
import CMS_lumi


plot_dir = "output/"
#plot_title = "results-plot-prefit-12_9-log"

def make_160_bin_plot(plot_title, lostlep, hadtau, znn, qcd, data_obs, doPull=False):

    TH1D.SetDefaultSumw2(True)
    import tdrstyle
    tdrstyle.setTDRStyle()
    gStyle.SetPadLeftMargin(0.12)
    gStyle.SetPadRightMargin(0.08)
    gStyle.SetPadTopMargin(0.08)
    gStyle.SetPalette(1)

    hdata_obs = data_obs.hist
    gdata_obs = data_obs.graph # note that this also sets the style

    ## load BG predictions -- also sets histogram styles
    sumBG = BGEst.sumBG(lostlep, hadtau, znn, qcd) # this will set the style of the hatched error bands

    ## build the stacked BG histogram    
    hqcd = qcd.hCV
    hznn = znn.hCV
    hlostlep = lostlep.hCV
    hhadtau = hadtau.hCV  
    hs = THStack("hs", "")
    hs.Add(hqcd)
    hs.Add(hhadtau)
    hs.Add(hlostlep)
    hs.Add(hznn)

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
    hbg_pred.GetYaxis().SetLabelSize(0.035*1.18)
    hbg_pred.GetYaxis().SetTitleSize(0.045*1.18)
    hbg_pred.GetYaxis().SetTitleOffset(0.75)
    hbg_pred.GetYaxis().SetTitleFont(42)
    hbg_pred.GetXaxis().SetLabelSize(0)
    hbg_pred.Add(hlostlep)
    hbg_pred.Add(hhadtau)
    hbg_pred.Add(hqcd)
    hbg_pred.Add(hznn)
    ymax = hbg_pred.GetMaximum()
    if hdata_obs.GetMaximum()>ymax:
         ymax=hdata_obs.GetMaximum()
    hbg_pred.SetMaximum(500*ymax)
    hbg_pred.SetMinimum(0.09)
    
    ratio = DataMCRatio(DataObs(hdata_obs), sumBG) # note that this also sets the style
    ratio_markers = ratio.markers
    ratio_bands = ratio.bands
    pull = ratio.pull
    pull.GetXaxis().SetTitle("Search region bin number")
    pull.SetMaximum(3.2)
    pull.SetMinimum(-3.2)
    hratdummy = ratio.dummy_hist
    hratdummy.GetXaxis().SetTitle("Search region bin number")
    hratdummy.SetMaximum(2.3)
    hratdummy.SetMinimum(-2.3)


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
    pad1.SetTopMargin(0.12)
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
    pad2.SetRightMargin(0.025)
    pad2.Draw()
    pad1.cd()

    ## draw graphs on top pad
    hbg_pred.Draw()
    hs.Draw("hist, same")
    sumBG.gFull.Draw("2, same")
    gdata_obs.Draw("p, same")

    ## legends
    leg1 = TLegend(0.6, 0.45, 0.845, 0.77)
    leg1.SetTextSize(0.035)
    leg1.SetFillStyle(0)
    leg1.AddEntry(gdata_obs.GetName(), "Data", "pes")
    leg1.AddEntry(hznn, "Z#rightarrow#nu#bar{#nu}", "f")
    leg1.AddEntry(hlostlep, "#splitline{Lost}{lepton}", "f")
    leg2 = TLegend(0.775, 0.45, 1.02, 0.77)
    leg2.SetTextSize(0.035)
    leg2.SetFillStyle(0)
    leg2.AddEntry(hbg_pred, "", "f")
    leg2.AddEntry(hhadtau, "#splitline{Hadronic}{#tau lepton}", "f")
    leg2.AddEntry(hqcd, "QCD", "f")

    leg1.Draw()
    leg2.Draw()

    ymax_top = hbg_pred.GetMaximum()
    ymin_top = 0.09

    ymax2_top = 1000.
    ymax3_top = 200.
    ymax4_top = 30.
    ymax5_top = 5.

    ymax_bottom = 1.99
    ymin_bottom = 0.01

    ymax2_bottom = 2.15
    ymax3_bottom = 2.15
    ymax4_bottom = 2.15

    ## labels and lines
    tl_njet = TLine()
    tl_njet.SetLineStyle(2)
    tl_njet.DrawLine(41.-0.5,ymin_top,41.-0.5,ymax_top) 
    tl_njet.DrawLine(81.-0.5,ymin_top,81.-0.5,ymax_top) 
    tl_njet.DrawLine(121.-0.5,ymin_top,121.-0.5,ymax_top) 

    ## Njet labels
    ttext_njet = TLatex()
    ttext_njet.SetTextFont(42)
    ttext_njet.SetTextSize(0.04)
    ttext_njet.SetTextAlign(22)
    ttext_njet.DrawLatex(20.-0.5 , ymax_top/4. , "3 #leq N_{#scale[0.2]{ }jet} #leq 4")
    ttext_njet.DrawLatex(60.-0.5 , ymax_top/4. , "5 #leq N_{#scale[0.2]{ }jet} #leq 6")
    ttext_njet.DrawLatex(100.-0.5 , ymax_top/4. , "7 #leq N_{#scale[0.2]{ }jet} #leq 8")
    ttext_njet.DrawLatex(140.-0.5 , ymax_top/4. , "N_{#scale[0.2]{ }jet} #geq 9")

    ## Nb separation lines
    tl_nb = TLine()
    tl_nb.SetLineStyle(3)
    tl_nb.DrawLine(11.-0.5,ymin_top,11.-0.5,ymax2_top) 
    tl_nb.DrawLine(21.-0.5,ymin_top,21.-0.5,ymax2_top) 
    tl_nb.DrawLine(31.-0.5,ymin_top,31.-0.5,ymax2_top)
    tl_nb.DrawLine(41.-0.5,ymin_top,41.-0.5,ymax2_top)
    tl_nb.DrawLine(51.-0.5,ymin_top,51.-0.5,ymax3_top) 
    tl_nb.DrawLine(61.-0.5,ymin_top,61.-0.5,ymax3_top) 
    tl_nb.DrawLine(71.-0.5,ymin_top,71.-0.5,ymax3_top) 
    tl_nb.DrawLine(81.-0.5,ymin_top,81.-0.5,ymax3_top) 
    tl_nb.DrawLine(91.-0.5,ymin_top,91.-0.5,ymax4_top) 
    tl_nb.DrawLine(101.-0.5,ymin_top,101.-0.5,ymax4_top) 
    tl_nb.DrawLine(111.-0.5,ymin_top,111.-0.5,ymax4_top)
    tl_nb.DrawLine(121.-0.5,ymin_top,121.-0.5,ymax4_top)
    tl_nb.DrawLine(131.-0.5,ymin_top,131.-0.5,ymax5_top)
    tl_nb.DrawLine(141.-0.5,ymin_top,141.-0.5,ymax5_top)
    tl_nb.DrawLine(151.-0.5,ymin_top,151.-0.5,ymax5_top)
    
    ## Nb labels
    ttext_nb = TLatex()
    ttext_nb.SetTextFont(42)
    ttext_nb.SetTextSize(0.04)
    ttext_nb.SetTextAlign(22)
    
    ttext_nb.DrawLatex(9.-0.5 , ymax_top/12. , "N_{#scale[0.2]{ }b-jet}")
    ttext_nb.DrawLatex(6.-0.5 , ymax_top/40. , "0")
    ttext_nb.DrawLatex(16.-0.5 , ymax_top/40. , "1")
    ttext_nb.DrawLatex(26.-0.5 , ymax_top/40. , "2")
    ttext_nb.DrawLatex(36.-0.5 , ymax_top/40. , "#geq 3")

    pad2.cd()
    if doPull:
        pull.Draw("hist")
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
    else:
        hratdummy.Draw("axis")
        ratio_bands.Draw("e2, same")
        ratio_markers.Draw("p, same")
    ratiomid = TLine(hbg_pred.GetBinLowEdge(1), 0., hbg_pred.GetBinLowEdge(hbg_pred.GetNbinsX()+1), 0.)
    ratiomid.SetLineStyle(2)
    ratiomid.Draw()
        
    ## lines again
    ratio_max = 2.3
    if doPull:
        ratio_max = 3.2
    tl_njet.DrawLine(41.-0.5, 0.-ratio_max, 41.-0.5,ratio_max) 
    tl_njet.DrawLine(81.-0.5, 0.-ratio_max, 81.-0.5,ratio_max)
    tl_njet.DrawLine(121.-0.5, 0.-ratio_max,121.-0.5,ratio_max)
    tl_nb.DrawLine(11.-0.5, 0.-ratio_max,11.-0.5,ratio_max) 
    tl_nb.DrawLine(21.-0.5, 0.-ratio_max,21.-0.5,ratio_max) 
    tl_nb.DrawLine(31.-0.5, 0.-ratio_max,31.-0.5,ratio_max)
    tl_nb.DrawLine(51.-0.5, 0.-ratio_max,51.-0.5,ratio_max) 
    tl_nb.DrawLine(61.-0.5, 0.-ratio_max,61.-0.5,ratio_max) 
    tl_nb.DrawLine(71.-0.5, 0.-ratio_max,71.-0.5,ratio_max) 
    tl_nb.DrawLine(91.-0.5, 0.-ratio_max,91.-0.5,ratio_max) 
    tl_nb.DrawLine(101.-0.5, 0.-ratio_max,101.-0.5,ratio_max) 
    tl_nb.DrawLine(111.-0.5, 0.-ratio_max,111.-0.5,ratio_max)
    tl_nb.DrawLine(131.-0.5, 0.-ratio_max,131.-0.5,ratio_max)
    tl_nb.DrawLine(141.-0.5, 0.-ratio_max,141.-0.5,ratio_max)
    tl_nb.DrawLine(151.-0.5, 0.-ratio_max,151.-0.5,ratio_max)

    ratioleg = TLegend(0.72, 0.88, 0.94, 0.96)
    ratioleg.SetTextSize(0.07)
    ratioleg.AddEntry(ratio_bands.GetName(), "Pred. uncert. (stat#oplussyst)", "f")

    ## refresh everything, to be safe
    pad1.cd()
    gPad.RedrawAxis()
    gPad.Modified()
    gPad.Update()
    pad2.cd()
    gPad.RedrawAxis()
    gPad.Modified()
    gPad.Update()

    ## now wite CMS headers
    canv.cd()
    lumi = 12.902808
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText = "       Preliminary"
    CMS_lumi.lumi_13TeV="%8.1f fb^{-1}" % lumi
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
    gPad.Print(plot_dir+plot_title+".png")
    
    gPad.Close()
        
if __name__ == "__main__":
    import sys
    output_file = sys.argv[1]
    f_lostlep = TFile.Open(sys.argv[2])
    lostlep = BGEst(f_lostlep.Get("hCV"), f_lostlep.Get("hStatUp"), f_lostlep.Get("hStatDown"), f_lostlep.Get("hSystUp"), f_lostlep.Get("hSystDown"), 2006)
    f_hadtau = TFile.Open(sys.argv[3])
    hadtau = BGEst(f_hadtau.Get("hCV"), f_hadtau.Get("hStatUp"), f_hadtau.Get("hStatDown"), f_hadtau.Get("hSystUp"), f_hadtau.Get("hSystDown"), 2007)
    f_znn = TFile.Open(sys.argv[4])
    znn = BGEst(f_znn.Get("hCV"), f_znn.Get("hStatUp"), f_znn.Get("hStatDown"), f_znn.Get("hSystUp"), f_znn.Get("hSystDown"), 2002)
    f_qcd = TFile.Open(sys.argv[5])
    qcd = BGEst(f_qcd.Get("hCV"), f_qcd.Get("hStatUp"), f_qcd.Get("hStatDown"), f_qcd.Get("hSystUp"), f_qcd.Get("hSystDown"), 2001)
    f_data_obs = TFile.Open(sys.argv[6])
    data_obs = DataObs(f_data_obs.Get("hCV"))
    make_160_bin_plot(output_file, lostlep, hadtau, znn, qcd, data_obs)  
