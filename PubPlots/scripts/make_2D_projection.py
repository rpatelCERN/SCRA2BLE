## makes 1D projections of background, signal, and observed data
## see make_all_1D_projections.py for examples of how to call this function

from __future__ import print_function
import os
import errno
from ROOT import TFile, TH1D, Math, gStyle, THStack, TLegend, TCanvas, TPad, gPad, TLatex, TLine, gROOT, TGaxis
from bg_est import BGEst
from data_obs import DataObs
from obs_exp_ratio import ObsExpRatio
from utils import GetPred
from math import floor
import CMS_lumi


plot_dir = "output/"
lumi = 35.862345

latex_templates = {'N_{jet} (p_{T} > 30 GeV)': 'njets',\
                   'N_{b-jet} (p_{T} > 30 GeV)': 'nbjets',\
                   'H_{T}^{miss} [GeV]': 'mht',\
                   'H_{T} [GeV]': 'ht'}

n_divisions = {'N_{jet} (p_{T} > 30 GeV)': 10, 'N_{b-jet} (p_{T} > 30 GeV)': 4}

signal_to_latex = {'T1tttt': '#tilde{g}#rightarrowt#bar{t} #tilde{#chi}_{1}^{0}',\
                   'T1bbbb': '#tilde{g}#rightarrowb#bar{b} #tilde{#chi}_{1}^{0}',\
                   'T1qqqq': '#tilde{g}#rightarrowq#bar{q} #tilde{#chi}_{1}^{0}',\
                   'T2tt': '#tilde{t}#rightarrowt #tilde{#chi}_{1}^{0}',\
                   'T2bb': '#tilde{b}#rightarrowb #tilde{#chi}_{1}^{0}',\
                   'T2qq': '#tilde{q}#rightarrowq #tilde{#chi}_{1}^{0}'}

signal_to_mass = {'T1tttt': 'm_{#tilde{g}}','T1bbbb':'m_{#tilde{g}}', 'T1qqqq': 'm_{#tilde{g}}',\
                  'T2tt': 'm_{#tilde{t}}','T2bb':'m_{#tilde{b}}', 'T2qq': 'm_{#tilde{q}}'}
               

def open_if_necessary(filename):
    # if we've already opened the file, just return the pointer already in memory, else create it, then return the pointer
    if gROOT.GetListOfFiles().FindObject(filename) == None:
        return TFile.Open(filename)
    else:
        return gROOT.GetListOfFiles().FindObject(filename)

# note: this time the inputs are just the paths to *_hists.root files
def make_2D_projection(plot_title, asr_name, lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       signal1, cut_labels, logy=True, doPull=False):

    TH1D.SetDefaultSumw2(True)
    import tdrstyle
    tdrstyle.setTDRStyle()
    gStyle.SetPadLeftMargin(0.12)
    gStyle.SetPadRightMargin(0.08)
    gStyle.SetPadTopMargin(0.08)
    gStyle.SetPalette(1)

    ## load observed data
    f_data_obs = open_if_necessary(data_file)
    data_obs_proj = DataObs(f_data_obs.Get(asr_name+"/hCV"))
    hdata_obs = data_obs_proj.hist
    gdata_obs = data_obs_proj.graph # note that this also sets the style
    gdata_obs.SetMarkerSize(1.3)

    ## load BG predictions -- also sets histogram styles

    f_lostlep = open_if_necessary(lostlep_file)
    f_hadtau = open_if_necessary(hadtau_file)
    f_qcd = open_if_necessary(qcd_file)
    f_znn = open_if_necessary(znn_file)
    qcd_proj = BGEst(f_qcd.Get(asr_name+"/hCV"), f_qcd.Get(asr_name+"/hStatUp"), f_qcd.Get(asr_name+"/hStatDown"), f_qcd.Get(asr_name+"/hSystUp"), f_qcd.Get(asr_name+"/hSystDown"), 2001)
    znn_proj = BGEst(f_znn.Get(asr_name+"/hCV"), f_znn.Get(asr_name+"/hStatUp"), f_znn.Get(asr_name+"/hStatDown"), f_znn.Get(asr_name+"/hSystUp"), f_znn.Get(asr_name+"/hSystDown"), 2002)
    lostlep_proj = BGEst(f_lostlep.Get(asr_name+"/hCV"), f_lostlep.Get(asr_name+"/hStatUp"), f_lostlep.Get(asr_name+"/hStatDown"), f_lostlep.Get(asr_name+"/hSystUp"), f_lostlep.Get(asr_name+"/hSystDown"), 2006)
    hadtau_proj = BGEst(f_hadtau.Get(asr_name+"/hCV"), f_hadtau.Get(asr_name+"/hStatUp"), f_hadtau.Get(asr_name+"/hStatDown"), f_hadtau.Get(asr_name+"/hSystUp"), f_hadtau.Get(asr_name+"/hSystDown"), 2007)

    
    hqcd = qcd_proj.hCV
    hznn = znn_proj.hCV
    hlostlep = lostlep_proj.hCV
    hhadtau = hadtau_proj.hCV
    ## build the stacked BG histogram    
    hs = THStack("hs", "")
    hs.Add(hqcd)
    hs.Add(hhadtau)
    hs.Add(hlostlep)
    hs.Add(hznn)

        ## load signal histograms
    f_signal = open_if_necessary(signal_file)
    # f_signal.ls()
    # print (asr_name, signal1, signal2)
    hsig1 = f_signal.Get("%s/RA2bin_%s_fast_nominal" % (asr_name, signal1))
    # scale to current luminosity
    if signal1.find("T2qq") >= 0:
        hsig1.Scale(lumi*1000*0.8)
    else:
        hsig1.Scale(lumi*1000)

    hs.Add(hsig1)
    hsig1.SetFillColor(2072)
    hsig1.SetLineStyle(7)
    hsig1.SetLineWidth(2)
    
        
    sumBG = BGEst.sumBG(lostlep_proj, hadtau_proj, znn_proj, qcd_proj) # this will set the style of the hatched error bands

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
    hbg_pred.GetYaxis().SetTitleFont(42)
    hbg_pred.GetXaxis().SetLabelSize(0)
    if logy:
        hbg_pred.GetYaxis().SetLabelSize(0.0455*1.18)
        hbg_pred.GetYaxis().SetTitleSize(0.075*1.18)
        hbg_pred.GetYaxis().SetTitleOffset(0.676)
    else:
        hbg_pred.GetYaxis().SetLabelSize(0.048*1.0)
        hbg_pred.GetYaxis().SetTitleSize(0.05625*1.15)
        hbg_pred.GetYaxis().SetTitleOffset(0.945)
    hbg_pred.Add(hlostlep)
    hbg_pred.Add(hhadtau)
    hbg_pred.Add(hqcd)
    hbg_pred.Add(hznn)
    ymax = hbg_pred.GetMaximum() + sumBG.hStatUp.GetMaximum()
    if hdata_obs.GetMaximum()>ymax:
         ymax=hdata_obs.GetMaximum()
    if logy:
        hbg_pred.SetMaximum(1500*ymax)
        hbg_pred.SetMinimum(0.09)
    else:
        hbg_pred.SetMaximum(1.625*ymax)
        if signal1.find('T1tttt')>=0:
            hbg_pred.SetMaximum(2.1*ymax)
        hbg_pred.SetMinimum(0.0)


        
    ratio = ObsExpRatio(DataObs(hdata_obs), sumBG) # note that this also sets the style
    ratio_markers = ratio.markers
    ratio.markers.SetMarkerSize(1.3)
    ratio_bands = ratio.bands
    pull = ratio.pull
    pull_max = 3.75
    pull_min = -3.75
    pull.SetMaximum(pull_max)
    pull.SetMinimum(-pull_max)
    pull.GetXaxis().SetLabelSize(0.14*1.2)
    pull.GetXaxis().SetTitleSize(0.12*1.19)
    pull.GetYaxis().SetLabelSize(0.14*1.075)
    pull.GetYaxis().SetTitleSize(0.155*1.12)
    pull.GetXaxis().SetTitleOffset(0.9)
    pull.GetXaxis().SetLabelOffset(0.01)
    pull.GetYaxis().SetTitleOffset(0.274)
    hratdummy = ratio.dummy_hist
    rat_max = 3.47
    rat_min = -rat_max*0.25
    hratdummy.SetMaximum(rat_max)
    hratdummy.SetMinimum(rat_min)
    hratdummy.GetXaxis().SetLabelSize(0.14*1.2)
    hratdummy.GetXaxis().SetTitleSize(0.12*1.19)
    hratdummy.GetYaxis().SetLabelSize(0.14*1.075)
    hratdummy.GetYaxis().SetTitleSize(0.155*1.12)
    hratdummy.GetXaxis().SetTitleOffset(1.05)
    hratdummy.GetXaxis().SetLabelOffset(0.01)
    hratdummy.GetYaxis().SetTitleOffset(0.274)



        
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

    pad1 = TPad("pad1", "top pad" , 0.0, 0.25, 1.0, 1.0)
    pad2 = TPad("pad2", "bottom pad", 0.0, 0.0, 1.0, 0.25)
    pad1.SetTickx(0)
    pad1.SetTicky(0)
    pad1.SetPad(0., 1 - up_height,    1., 1.00)
    pad1.SetFrameFillColor(0)
    pad1.SetFillColor(0)
    pad1.SetTopMargin(0.1)
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.02)
    pad1.SetLogy(logy)    
    pad1.Draw()

    pad2.SetPad(0., 0., 1., dw_height+dw_height_offset)
    pad2.SetFillColor(0)
    pad2.SetFrameFillColor(0)
    pad2.SetBottomMargin(0.35)
    pad2.SetTopMargin(0)
    pad2.SetLeftMargin(0.12)
    pad2.SetRightMargin(0.02)
    pad2.Draw()
    pad1.cd()

    ## draw graphs on top pad
    if hlostlep.GetXaxis().GetTitle() in n_divisions.keys():
        hbg_pred.GetXaxis().SetNdivisions(n_divisions[hlostlep.GetXaxis().GetTitle()],0,0)
    hbg_pred.Draw()
    hs.Draw("hist, same")
    #hsig1.Draw("hist,same")
    sumBG.gFull.Draw("2, same")
    gdata_obs.Draw("p, 0, same")

    ## legends
    legdata = TLegend(0.25-0.1, 0.756, 0.45-0.14, 0.9);
    legdata.SetTextSize(0.045)
    legdata.SetFillStyle(0)
    leg1 = TLegend(0.27, 0.756, 0.56, 0.88);
    leg1.SetTextSize(0.045)
    leg1.SetFillStyle(0)
    leg2 = TLegend(0.44, 0.756, 0.73, 0.88);
    leg2.SetTextSize(0.045)
    leg2.SetFillStyle(0)
    leg3 = TLegend(0.61, 0.756, 0.90, 0.88);
    leg3.SetTextSize(0.045)
    leg3.SetFillStyle(0)
    leg4 = TLegend(0.825, 0.756, 1.105, 0.88);
    leg4.SetTextSize(0.045)
    leg4.SetFillStyle(0)

    
    legdata.AddEntry(gdata_obs.GetName(), "Data", "pes")
    leg1.AddEntry(hznn, "Z#rightarrow#nu#bar{#nu}", "f")
    leg2.AddEntry(hlostlep, "#splitline{Lost}{lepton}", "f")
    leg3.AddEntry(hhadtau, "#splitline{Hadronic}{#tau lepton}", "f")
    leg4.AddEntry(hqcd, "QCD", "f")

    sig1_arr = signal1.split("_")
    legs1 = "%s (%s = %d GeV, m_{#tilde{#chi}_{1}^{0}} = %d GeV)" % (signal_to_latex[sig1_arr[0]], signal_to_mass[sig1_arr[0]], int(sig1_arr[1]), int(sig1_arr[2]))
    slength = len(legs1)
    legsig = TLegend(0.15, 0.62, 1.-slength/165.5+0.55, 0.75);
    legsig.SetTextSize(0.04)
    legsig.SetFillStyle(0)
    legsig.SetMargin(0.125)
    legsig.AddEntry(hsig1, legs1, "f")

    legdata.Draw()
    leg1.Draw()
    leg2.Draw()
    leg3.Draw()
    leg4.Draw()
    legsig.Draw()

    ymin_top=0.09
    ymax_top=1150

    ## labels and lines
    tl_njet = TLine()
    tl_njet.SetLineStyle(2)
    tl_njet.SetLineWidth(2)
    tl_njet.SetLineColor(1)
    tl_njet.DrawLine(3.5,ymin_top,3.5,ymax_top) 
    tl_njet.DrawLine(7.5,ymin_top,7.5,ymax_top) 
    tl_njet.DrawLine(11.5,ymin_top,11.5,ymax_top) 
    tl_njet.DrawLine(15.5,ymin_top,15.5,ymax_top)

    ## Njet labels
    ttext_njet = TLatex()
    ttext_njet.SetTextFont(42)
    ttext_njet.SetTextSize(0.04)
    ttext_njet.SetTextAlign(22)
    ttext_njet.DrawLatex(2 , ymax_top*0.75 , "N_{#scale[0.2]{ }jet} = 2")
    ttext_njet.DrawLatex(5.5 , ymax_top*0.75 , "3 #leq N_{#scale[0.2]{ }jet} #leq 4")
    ttext_njet.DrawLatex(9.5 , ymax_top*0.75, "5 #leq N_{#scale[0.2]{ }jet} #leq 6")
    ttext_njet.DrawLatex(13.5 , ymax_top*0.75, "7 #leq N_{#scale[0.2]{ }jet} #leq 8")
    ttext_njet.DrawLatex(17.5 , ymax_top*0.75, "N_{#scale[0.2]{ }jet} #geq 9")

    # cuts label
    latex = TLatex();
    latex.SetNDC();
    latex.SetTextAlign(12);
    latex.SetTextFont(62);
    latex.SetTextSize(0.038);
    latex.DrawLatex(1.-len(cut_labels)/125.5, 0.695, cut_labels);

    pad2.cd()
    ratiomid = TLine(hbg_pred.GetBinLowEdge(1), 0., hbg_pred.GetBinLowEdge(hbg_pred.GetNbinsX()+1), 0.)

    nb_labels = ['0','1','2']
    x_labels = ['0','1','2', '0','1','2','3+', '0','1','2','3+', '0','1','2','3+', '0','1','2', '3+']
    for xbin in range(hratdummy.GetNbinsX()):
        hratdummy.GetXaxis().SetBinLabel(xbin+1, x_labels[xbin])
        pull.GetXaxis().SetBinLabel(xbin+1, x_labels[xbin])
    
    if doPull:
        pull.Draw("hist")
        if hlostlep.GetXaxis().GetTitle() in n_divisions.keys():
            pull.GetXaxis().SetNdivisions(n_divisions[hlostlep.GetXaxis().GetTitle()],0,0)
        p1 = TLine(pull.GetBinLowEdge(1), 1., pull.GetBinLowEdge(pull.GetNbinsX()+1), 1.)
        p2 = TLine(pull.GetBinLowEdge(1), 2., pull.GetBinLowEdge(pull.GetNbinsX()+1), 2.)
        p3 = TLine(pull.GetBinLowEdge(1), 3., pull.GetBinLowEdge(pull.GetNbinsX()+1), 3.)
        m1 = TLine(pull.GetBinLowEdge(1), -1., pull.GetBinLowEdge(pull.GetNbinsX()+1), -1.)
        m2 = TLine(pull.GetBinLowEdge(1), -2., pull.GetBinLowEdge(pull.GetNbinsX()+1), -2.)
        m3 = TLine(pull.GetBinLowEdge(1), -3., pull.GetBinLowEdge(pull.GetNbinsX()+1), -3.)
        ratiomid.SetLineWidth(3)
        p1.SetLineStyle(2)
        p2.SetLineStyle(2)
        p3.SetLineStyle(2)
        m1.SetLineStyle(2)
        m2.SetLineStyle(2)
        m3.SetLineStyle(2)
        p1.Draw()
        p2.Draw()
        p3.Draw()
        m1.Draw()
        m2.Draw()
        m3.Draw()
        pull.Draw("hist,same")
    else:
        hratdummy.Draw("axis")
        if hlostlep.GetXaxis().GetTitle() in n_divisions.keys():
            hratdummy.GetXaxis().SetNdivisions(n_divisions[hlostlep.GetXaxis().GetTitle()],0,0)
        ratio_bands.Draw("e2, same")
        ratio_markers.Draw("p, 0, same")
        ratiomid.SetLineStyle(2)

    ratiomid.Draw()
        
    ## lines again
    if doPull:
        rat_max = pull_max
        rat_min = pull_min

    ymin_bottom = rat_min
    ymax_bottom = rat_max
    tl_njet.DrawLine(3.5,ymin_bottom,3.5,ymax_bottom) 
    tl_njet.DrawLine(7.5,ymin_bottom,7.5,ymax_bottom) 
    tl_njet.DrawLine(11.5,ymin_bottom,11.5,ymax_bottom) 
    tl_njet.DrawLine(15.5,ymin_bottom,15.5,ymax_bottom)


    ## refresh everything, to be safe
    pad1.cd()
    gPad.RedrawAxis()
    rightcoord = hbg_pred.GetBinLowEdge(sumBG.nbins)+hbg_pred.GetBinWidth(sumBG.nbins)
    rightaxis = TGaxis(rightcoord, 0., rightcoord, hbg_pred.GetMaximum(), 0., hbg_pred.GetMaximum(), 510, "+L")
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
    CMS_lumi.writeExtraText = True     
    CMS_lumi.extraText = "        Supplementary"
    CMS_lumi.lumi_13TeV="%8.1f fb^{-1}" % lumi
    CMS_lumi.lumi_sqrtS = CMS_lumi.lumi_13TeV+ " (13 TeV)"
    iPos=0
    CMS_lumi.CMS_lumi(canv, 0, iPos)

    latex = TLatex()
    latex.SetTextSize(0.0375)
    #latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextFont(42)
    latex.SetTextColor(4)
    latex.SetTextSize(0.032)
    latex.DrawLatex(0.48, 0.948, "arXiv:1704.07781")


    ## save plot to PDF and PNG
    try:
        os.makedirs(plot_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    gPad.Print(plot_dir+plot_title+".pdf")
    gPad.Print(plot_dir+plot_title+".png")

    if doPull:
        gPad.Close()
        return 

    gPad.Close()
    

        
## if __name__ == "__main__":
##     import sys
##     output_file = sys.argv[1]
##     asr_tag = sys.argv[2]
##     f_lostlep = TFile.Open(sys.argv[3])
##     lostlep = BGEst(f_lostlep.Get("ASR/hCV"), f_lostlep.Get("ASR/hStatUp"), f_lostlep.Get("ASR/hStatDown"), f_lostlep.Get("ASR/hSystUp"), f_lostlep.Get("ASR/hSystDown"), 2006)
##     f_hadtau = TFile.Open(sys.argv[4])
##     hadtau = BGEst(f_hadtau.Get("ASR/hCV"), f_hadtau.Get("ASR/hStatUp"), f_hadtau.Get("ASR/hStatDown"), f_hadtau.Get("ASR/hSystUp"), f_hadtau.Get("ASR/hSystDown"), 2007)
##     f_znn = TFile.Open(sys.argv[5])
##     znn = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"), 2002)
##     f_qcd = TFile.Open(sys.argv[6])
##     qcd = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"), 2001)
##     f_data_obs = TFile.Open(sys.argv[7])
##     data_obs = DataObs(f_data_obs.Get("ASR/hCV"))
##     make_12_asr_plot(output_file, lostlep, hadtau, znn, qcd, data_obs)  
