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

if __name__ == '__main__':

	names   = columnToList('dat.txt',0)
	l_obs   = columnToList('dat.txt',3)
	l_m2sig = columnToList('dat.txt',1)
	l_m1sig = columnToList('dat.txt',2)
	l_exp   = columnToList('dat.txt',3)
	l_p1sig = columnToList('dat.txt',4)
	l_p2sig = columnToList('dat.txt',5)

	print l_m2sig
	print l_p2sig

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

	a_2sig.append(2.29513096809)
	a2_xax.append(0.5)

	g_exp = ROOT.TGraph(len(a_xax), a_xax, a_exp)
	g_obs = ROOT.TGraph(len(a_xax), a_xax, a_obs)
	g_1sig = ROOT.TGraph(len(2*a_xax), a2_xax, a_1sig)
	g_2sig = ROOT.TGraph(len(2*a_xax)+1, a2_xax, a_2sig)

	print g_2sig;

	can = ROOT.TCanvas("can","can",1200,800);
	hrl = ROOT.TH1F("hrl","hrl",6,0,6);
	# hrl = can.DrawFrame(0,0,6,15);
	hrl.GetYaxis().SetTitle("#mu = #sigma_{95%CL}/#sigma_{SMS}");
	hrl.GetXaxis().SetTitle("FullSim model");
	hrl.GetXaxis().SetBinLabel(1,names[0])
	hrl.GetXaxis().SetBinLabel(2,names[1])
	hrl.GetXaxis().SetBinLabel(3,names[2])
	hrl.GetXaxis().SetBinLabel(4,names[3])
	hrl.GetXaxis().SetBinLabel(5,names[4])
	hrl.GetXaxis().SetBinLabel(6,names[5])
	hrl.SetMaximum(4.);
	hrl.Draw();

	can.SetGrid(); 

	txta = ROOT.TLatex(0.70,0.90,"CMS");
	txta.SetNDC();
	txtb = ROOT.TLatex(0.78,0.90,"Preliminary");
	txtb.SetNDC(); txtb.SetTextFont(52);
	txtc = ROOT.TLatex(0.81,0.96,"1.3 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.04);

	leg = ROOT.TLegend(0.20,0.73,0.4,0.90);
	leg.SetFillStyle(1001);
	leg.SetFillColor(0);    
	leg.SetBorderSize(1);  
	# leg.SetNColumns(2);
	leg.AddEntry(g_exp,"expected","l")
	# leg.AddEntry(g_obs,"observed","l")
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
	# g_obs.Draw('lsames');
	g_exp.Draw('lsames');
	oneLine.Draw("LSAMES");
	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	
	leg.Draw();

	can.SaveAs('test.pdf');


