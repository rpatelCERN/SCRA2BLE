#! /usr/bin/env python

import os
import glob
import math
import array
import sys
import time
import ROOT
from array import array


import tdrstyle
tdrstyle.setTDRStyle()
# ROOT.gROOT.ProcessLine(".L ~/tdrstyle.C");
# ROOT.setTDRStyle();
# ROOT.gStyle.SetPadLeftMargin(0.16);
# ROOT.gStyle.SetPadRightMargin(0.10);
# ROOT.gStyle.SetPadTopMargin(0.10);
# ROOT.gStyle.SetPalette(1);

## ===========================================================================================
## ===========================================================================================
## ===========================================================================================

def columnToList(fn,col):
	f = open(fn,'r');

	olist = [];
	for line in f: 
		linelist = line.strip().split()
		olist.append( linelist[col] );
	return olist

def ExtractFile(iname, tag):
	f = ROOT.TFile(iname);
	t = f.Get("results");
	t.GetEntry(0);
	lims = [];
	lims.append(tag);
	lims.append( t.limit_m2s )
	lims.append( t.limit_m1s );
	lims.append( t.limit_exp )
	lims.append( t.limit_p1s );
	lims.append( t.limit_p2s )
	lims.append( t.limit_obs );
	return lims;

if __name__ == '__main__':

	#idir = "/eos/uscms/store/user/ntran/SUSY/statInterp/scanOutput/Dec6";
	idir = ".";

	results = [];
	results.append( ExtractFile(idir+'/results_T5HH_1300_900_mu0.0.root','1300') );
	results.append( ExtractFile(idir+'/results_T5HH_1400_900_mu0.0.root','1400') );
	results.append( ExtractFile(idir+'//results_T5HH_1500_900_mu0.0.root','1500') );
	# results.append( ExtractFile(idir+'/results_T1tttt_1200_800.root','T1tttt1200') );
	results.append( ExtractFile(idir+'/results_T5HH_1600_900_mu0.0.root','1600') );
	results.append( ExtractFile(idir+'/results_T5HH_1700_900_mu0.0.root','1700') );

	# results.append( ExtractFile(idir+'/results_T1bbbb_1500_100.root','T1bbbb1500') );
	# results.append( ExtractFile(idir+'/results_T1bbbb_1000_100.root','T1bbbb1000') );
	# #results.append( ExtractFile(idir+'/results_T1tttt_1500_100.root','T1tttt1500') );
	# results.append( ExtractFile(idir+'/results_T1tttt_1500_800.root','T1tttt1200') );
	# results.append( ExtractFile(idir+'/results_T1tttt_1200_800.root','T1tttt1200') );
	# results.append( ExtractFile(idir+'/results_T1qqqq_1400_800.root','T1qqqq1400') );
	# results.append( ExtractFile(idir+'/results_T1qqqq_1000_800.root','T1qqqq1000') );

	Xsecs=[0.0460525, 0.0252977, 0.0141903, 0.00810078, 0.00470323]
	names   = [];
	l_obs   = [];
	l_m2sig = [];
	l_m1sig = [];
	l_exp   = [];
	l_p1sig = [];
	l_p2sig = [];
	count=0;
	for r in results:
		names.append(r[0]);
		l_m2sig.append(r[1]*Xsecs[count]);
		l_m1sig.append(r[2]*Xsecs[count]);
		l_exp.append(r[3]*Xsecs[count]);
		l_p1sig.append(r[4]*Xsecs[count]);
		l_p2sig.append(r[5]*Xsecs[count]);
		l_obs.append(r[6]*Xsecs[count]);
		count=count+1
	print "l_exp = ", l_exp
	print "l_obs = ", l_obs

	a_xax = array('d', []);
	a2_xax = array('d', []);
	a_exp = array('d', []);
	a_obs = array('d', []);
	a_1sig = array('d', []);
	a_2sig = array('d', []);

	for i in range(len(names)): a_xax.append( float(i)+0.5 );
	for i in range(len(names)): a2_xax.append( float(i)+0.5 );
	for i in range(len(names)-1,-1,-1): a2_xax.append( float(i)+0.5 );
	for i in range(len(l_obs)): a_obs.append( float(l_obs[i]) );
	for i in range(len(l_exp)): a_exp.append( float(l_exp[i]) );
	
	for i in range(len(l_m2sig)): a_2sig.append( float(l_m2sig[i]) );
	for i in range(len(l_p2sig)-1,-1,-1): a_2sig.append( float(l_p2sig[i]) );
	
	for i in range(len(l_m1sig)): a_1sig.append( float(l_m1sig[i]) );
	for i in range(len(l_p1sig)-1,-1,-1): a_1sig.append( float(l_p1sig[i]) );

	print a_2sig, len(a_2sig)
	print a2_xax, len(a2_xax)

	a_2sig.append(results[0][6])
	a2_xax.append(0.5)

	g_exp = ROOT.TGraph(len(a_xax), a_xax, a_exp)
	g_obs = ROOT.TGraph(len(a_xax), a_xax, a_obs)
	g_1sig = ROOT.TGraph(len(2*a_xax), a2_xax, a_1sig)
	g_2sig = ROOT.TGraph(len(2*a_xax)+1, a2_xax, a_2sig)

	print g_2sig;

	can = ROOT.TCanvas("can","can",1200,800);
	hrl = ROOT.TH1F("hrl","hrl",5,0,5);
	# hrl = can.DrawFrame(0,0,6,15);
	#hrl.GetYaxis().SetTitle("#mu = #sigma_{95%CL}/#sigma_{SMS}");
	hrl.GetYaxis().SetTitle("#sigma_{95%CL}");
	hrl.GetXaxis().SetTitle("FullSim model");
	hrl.GetXaxis().SetBinLabel(1,names[0])
	hrl.GetXaxis().SetBinLabel(2,names[1])
	hrl.GetXaxis().SetBinLabel(3,names[2])
	hrl.GetXaxis().SetBinLabel(4,names[3])
	hrl.GetXaxis().SetBinLabel(5,names[4])
	hrl.SetMaximum(0.1);
	hrl.Draw();

	can.SetGrid(); 

	txta = ROOT.TLatex(0.70,0.90,"CMS");
	txta.SetNDC();
	txtb = ROOT.TLatex(0.78,0.90,"Preliminary");
	txtb.SetNDC(); txtb.SetTextFont(52);
	txtc = ROOT.TLatex(0.81,0.96,"9.2 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.04);

	leg = ROOT.TLegend(0.20,0.73,0.4,0.90);
	leg.SetFillStyle(1001);
	leg.SetFillColor(0);    
	leg.SetBorderSize(1);  
	# leg.SetNColumns(2);
	leg.AddEntry(g_exp,"expected","l")
	leg.AddEntry(g_obs,"observed","l")
	leg.AddEntry(g_2sig,"expected 2#sigma","f")
	leg.AddEntry(g_1sig,"expected 1#sigma","f")
   
	oneLine = ROOT.TF1("oneLine","1",0,6);
	oneLine.SetLineColor(ROOT.kRed+2);
	oneLine.SetLineWidth(2);
	oneLine.SetLineStyle(1);
	
	g_1sig.SetFillColor(ROOT.kGreen);
	g_1sig.SetFillStyle(3244);
	g_2sig.SetFillColor(ROOT.kYellow);
	g_2sig.SetFillStyle(3244);
	g_exp.SetLineStyle(2);
	g_exp.SetLineWidth(2);
	g_2sig.Draw('f');
	g_1sig.Draw('fsames');
	g_obs.Draw('lsames');
	g_exp.Draw('lsames');
	oneLine.Draw("LSAMES");
	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	
	leg.Draw();

	can.SaveAs('brazilFullSim.pdf');


