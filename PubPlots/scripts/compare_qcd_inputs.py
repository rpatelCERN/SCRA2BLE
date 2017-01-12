from __future__ import print_function
import os
import errno
from ROOT import TFile, TH1D, Math, gStyle, THStack, TLegend, TCanvas, TPad, gPad, TLatex, TLine, gROOT
from bg_est import BGEst
from utils import GetPred

def make_174_bin_qcd_tables(title='qcd-prefit-tables-174', qcdldp, qcdrs):

def compare_qcd_inputs(ldpfile='qcd_hists.root', rnsfile='qcdrs_hists.root'):
    f_rs = TFile.Open(rnsfile)
    f_ldp = TFile.Open(ldpfile)

    qcdrs = BGEst(f_rs.Get("hCV"), f_rs.Get("hStatUp"), f_rs.Get("hStatDown"), f_rs.Get("hSystUp"), f_rs.Get("hSystDown"), 2001)
    qcdldp = BGEst(f_ldp.Get("hCV"), f_ldp.Get("hStatUp"), f_ldp.Get("hStatDown"), f_ldp.Get("hSystUp"), f_ldp.Get("hSystDown"), 2001)

    make_174_bin_qcd_tables('qcd-prefit-tables-174', qcdldp, qcdrs)
