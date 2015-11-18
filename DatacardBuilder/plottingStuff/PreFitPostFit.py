import ROOT as root
from ROOT import *
import ROOT
import time
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import math
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadTopMargin(0.08);
ROOT.gStyle.SetPalette(1);


#########################################################################################################
def getErrorFromCard(card,chan):

	lnNSystematics = [];

	fcard=open(card)
	column = -1;
	sysLine = False;
	for line in fcard:
		parse=line.split(' ')
		if parse[0]=='process' and parse[1]=='sig':
			for i in range(len(parse)):
				if parse[i] == chan: 
					column = i;

		if parse[0]=='lumi': sysLine = True; #it's time to collect
		if sysLine and parse[1] == "lnN": 
			parse = [x for x in parse if x != '']				
			print "blah,",parse[0],parse[column+1],column,parse				
			if parse[column+1] != "-": 
				if '/' in parse[column+1]: 
					syssplit = parse[column+1].split('/');
					lnNSystematics.append(float(syssplit[1])-1.0);
				else:
					lnNSystematics.append(float(parse[column+1])-1.0);

	print lnNSystematics
	return 0.5

if __name__ == '__main__':
	
	theDir = 'testCards-allBkgs-SMSbbbb1500-1.3-mu0.0'

	fin=TFile("../"+theDir+"/mlfit"+theDir+".root", "READ")
	BinProcesses=fin.Get("norm_prefit");
	mybins=[]
	searchbins=[]
	hsprefit = THStack();
	hspostfit = THStack();

	histqcd=TH1F("histqcd", "QCD pre-fit Yields"      , 72, 0.3, 72.3);
	histZ=TH1F("histZ", "Zinv pre-fit Yields"         , 72, 0.3, 72.3);
	histTau=TH1F("histTau", "Tau pre-fit Yields"      , 72, 0.3, 72.3);
	histLL=TH1F("histLL", "Lost Lepton pre-fit Yields", 72, 0.3, 72.3);

	# YieldsFile=TFile(theDir+"/yields.root", "READ")
	# histqcd=YieldsFile.Get("QCD")
	# histZ=YieldsFile.Get("Zvv")
	# histTau=YieldsFile.Get("tau")
	# histLL=YieldsFile.Get("LL")
	#Gymnastics for Pre-fit

	qcd_uscb_gold = TColor (2001, 255/255.,200/255.,47/255);
	znn_penn_red = TColor(2002, 255/255.,0/255.,43/255.);
	lost_lep_dusk_blue = TColor(2006, 105/255.,166/255., 202/255.);
	had_tau_grayed_jade = TColor(2007, 133/255.,189/255., 164/255.);

	histqcd.SetFillColor(2001);
	# histqcd.SetLineColor(kYellow);
	histZ.SetFillColor(2002);
	# histZ.SetLineColor(kCyan);
	histLL.SetFillColor(2006);
	# histLL.SetLineColor(kBlue);
	histTau.SetFillColor(2007);
	# histTau.SetLineColor(kGreen);

	for c in range(1,235):
		sig = BinProcesses.find("ch%d/sig" %c)
		Z   = BinProcesses.find("ch%d/zvv" %c)
		Q   = BinProcesses.find("ch%d/qcd" %c)
		T   = BinProcesses.find("ch%d/WTopHad" %c)
		L   = BinProcesses.find("ch%d/WTopSL" %c)
		
		if Q and Z:# only signal region bins have process QCD and Zinv 
			#print T.getVal(), L.getVal(),Z.getVal(), Q.getVal()
			mybins.append(c)
			#just need to find this once (mapping to search bins):
			for i in range(0,72):
				fcardname = "../"+theDir+"/card_signal%d.txt" %i;
				fcard=open(fcardname)
				fcard.seek(0)
				for line in fcard:
					parse=line.split(' ')
					if parse[0]=='rate':
						 eps=1e-4
						 if(abs(L.getVal()-float(parse[2]))<eps and abs(T.getVal()-float(parse[4]))<eps and abs(Z.getVal()-float(parse[6]))<eps and abs(Q.getVal()-float(parse[7]))<eps):
							searchbins.append(i)
							# Prefit errors, leave out for now
							# fcard.close();							
							# print "getErrorFromCard(fname,'zvv') = ", getErrorFromCard(fcardname,'zvv')
							histZ.SetBinContent(i+1, Z.getVal()) 	
							histqcd.SetBinContent(i+1, Q.getVal())
							histLL.SetBinContent(i+1, L.getVal())
							histTau.SetBinContent(i+1, T.getVal())
							# break;

	hsprefit.Add(histZ);
	hsprefit.Add(histqcd);
	hsprefit.Add(histLL);
	hsprefit.Add(histTau);
	hsprefit_tot = hsprefit.GetStack().Last();
	# hsprefit_tot.SetFillStyle(3004);
	# hsprefit_tot.SetFillColor(1);

	canPre = TCanvas("canPre","canPre",1600,800);
	hsprefit.Draw('hist');

	hsprefit.SetTitle('; bin; yield')
	canPre.SaveAs("plotstacks/prestack.pdf");
	gPad.SetLogy();
	canPre.SaveAs("plotstacks/prestack_log.pdf");

	histqcdpost=TH1F("histqcdpost", "QCD post-fit Yields", 72, 0.5, 72.5);
	histZpost=TH1F("histZpost", "Zinv post-fit Yields", 72, 0.5, 72.5);
	histTaupost=TH1F("histTaupost", "Tau post-fit Yields", 72, 0.5, 72.5);
	histLLpost=TH1F("histLLpost", "Lost Lepton post-fit Yields", 72, 0.5, 72.5);
	
	histqcdpost.SetFillColor(2001);
	# histqcdpost.SetLineColor(kYellow);
	histZpost.SetFillColor(2002);
	# histZpost.SetLineColor(kCyan);
	histLLpost.SetFillColor(2006);
	# histLLpost.SetLineColor(kBlue);
	histTaupost.SetFillColor(2007);
	# histTaupost.SetLineColor(kGreen);
	
	BinProcessesPostFit=fin.Get("norm_fit_b");

	print "len(mybins) = ", len(mybins);
	for c in range(len(mybins)):
		Z=BinProcessesPostFit.find("ch%d/zvv" %mybins[c])
		Q=BinProcessesPostFit.find("ch%d/qcd" %mybins[c])
		T=BinProcessesPostFit.find("ch%d/WTopHad" %mybins[c])
		L=BinProcessesPostFit.find("ch%d/WTopSL" %mybins[c])
		histZpost.SetBinContent(searchbins[c]+1, Z.getVal())
		histZpost.SetBinError(searchbins[c]+1, Z.getError())
		histqcdpost.SetBinContent(searchbins[c]+1, Q.getVal())
		histLLpost.SetBinContent(searchbins[c]+1, L.getVal())
		histLLpost.SetBinError(searchbins[c]+1, L.getError())
		histTaupost.SetBinContent(searchbins[c]+1, T.getVal())
		histTaupost.SetBinError(searchbins[c]+1, T.getError())

		qerr = Q.getError()
		if Q.getError()/Q.getVal() > 100 and Q.getError() > 1.0: 
			qerr = 0.0;
			print "Outlier Rejection!!"
		histqcdpost.SetBinError(searchbins[c]+1, qerr)

		print "XX content, bin {0:2}: {1:6.4f} +- {2:6.4f}, {3:6.4f} +- {4:6.4f}, {5:6.4f} +- {6:6.4f}, {7:6.4f} +- {8:6.4f}".format(c,Z.getVal(),Z.getError(),Q.getVal(),Q.getError(),L.getVal(),L.getError(),T.getVal(),T.getError());

	hspostfit.Add(histqcdpost)
	hspostfit.Add(histZpost)
	hspostfit.Add(histTaupost)
	hspostfit.Add(histLLpost)
	hspostfit_tot = hspostfit.GetStack().Last();

	hspostfit_tot_clone = hspostfit_tot.Clone();
	hspostfit_tot_clone.SetFillStyle(3001);
	hspostfit_tot_clone.SetFillColor(13);
	hspostfit_tot_clone.SetMarkerSize(0);

	# for i in range(hsprefit_tot.GetNbinsX()):
	# 	print "bin {0:2}: {1:6.2f} {2:6.2f}".format(i,hsprefit_tot.GetBinContent(i+1),hspostfit_tot.GetBinContent(i+1));

	DataIn = TFile("../inputHistograms/histograms_1.3fb/RA2bin_signalUnblind.root");
	DataHist = DataIn.Get("RA2bin_data");
	DataHist.SetBinErrorOption(ROOT.TH1F.kPoisson);
	DataHist.SetMarkerStyle(34);
	DataHist.SetMarkerSize(2);
	hsprefit_tot.SetMarkerStyle(24);
	hsprefit_tot.SetMarkerSize(2);
	hsprefit_tot.SetMarkerColor(2);
	hsprefit_tot.SetLineColor(2);

	dat_rat = TH1F('dat_rat',';bin;pull',72,0.5,72.5);
	dat_rat_nounc = TH1F('dat_rat_nounc',';bin;obs/pred',72,0.5,72.5);
	pre_rat = TH1F('pre_rat',';bin;pull',72,0.5,72.5);

	prepost_rat_Z = TH1F('prepost_rat_Z',';bin;(postfit_{i}-prefit_{i})/prefit_{i}',72,0.5,72.5);
	prepost_rat_Q = TH1F('prepost_rat_Q',';bin;fraction change',72,0.5,72.5);
	prepost_rat_L = TH1F('prepost_rat_L',';bin;fraction change',72,0.5,72.5);
	prepost_rat_T = TH1F('prepost_rat_T',';bin;fraction change',72,0.5,72.5);

	prepost_rat_Z_ovTot = TH1F('prepost_rat_Z_ ovTot',';bin;(postfit_{i}-prefit_{i})/prefit_{tot}',72,0.5,72.5);
	prepost_rat_Q_ovTot = TH1F('prepost_rat_Q_ ovTot',';bin;fraction change',72,0.5,72.5);
	prepost_rat_L_ovTot = TH1F('prepost_rat_L_ ovTot',';bin;fraction change',72,0.5,72.5);
	prepost_rat_T_ovTot = TH1F('prepost_rat_T_ ovTot',';bin;fraction change',72,0.5,72.5);


	tmptot = 0;
	tmptot2 = 0;
	DataHistNew = ROOT.TH1F("DataHistNew",";yield;bins",72,0.5,72.5);
	DataHistNew.SetBinErrorOption(ROOT.TH1.kPoisson);
	for i in range(dat_rat.GetNbinsX()):
		DataHistNew.SetBinContent(i+1,DataHist.GetBinContent(i+1));
		staterr_dat = max(DataHistNew.GetBinErrorUp(i+1),DataHistNew.GetBinErrorLow(i+1));
		staterr_post = sqrt(hspostfit_tot_clone.GetBinContent(i+1));
		# print DataHist.GetBinContent(i+1),TMP1.GetBinErrorUp(i+1),TMP1.GetBinErrorLow(i+1),hsprefit_tot.GetBinError(i+1)

		curerr_dat = math.sqrt(hspostfit_tot_clone.GetBinError(i+1)*hspostfit_tot_clone.GetBinError(i+1) + staterr_post*staterr_post);
		curerr_pre = math.sqrt(hspostfit_tot_clone.GetBinError(i+1)*hspostfit_tot_clone.GetBinError(i+1) + staterr_post*staterr_post);
		curdat = DataHist.GetBinContent(i+1);
		curpre = hsprefit_tot.GetBinContent(i+1);
		curpos = hspostfit_tot.GetBinContent(i+1);
		i_dat_rat = (curdat-curpos)/curerr_dat;
		i_pre_rat = (curpre-curpos)/curerr_pre;
		dat_rat.SetBinContent(i+1,i_dat_rat)
		dat_rat_nounc.SetBinContent(i+1,curdat/curpos)
		pre_rat.SetBinContent(i+1,i_pre_rat)

		prepost_rat_Z.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/histZ.GetBinContent(i+1));
		prepost_rat_Q.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1))/histqcd.GetBinContent(i+1));
		prepost_rat_L.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1))/histLL.GetBinContent(i+1));
		prepost_rat_T.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1))/histTau.GetBinContent(i+1));

		prepost_rat_Z_ovTot.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/curpre);
		prepost_rat_Q_ovTot.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1))/curpre);
		prepost_rat_L_ovTot.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1))/curpre);
		prepost_rat_T_ovTot.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1))/curpre);

		if i >= 60: tmptot += curpos;
		if i >= 60: tmptot2 += curpre;
		# print "bin{0:2}: {1:4} {2:6} +/- {7:6f} +/- {8:6f} ||| Z={3:4f} Q={4:4f} L={5:4f} T={6:4f}".format(i,curdat,curpos,histZpost.GetBinContent(i+1),histqcdpost.GetBinContent(i+1),histLLpost.GetBinContent(i+1),histTaupost.GetBinContent(i+1),hspostfit_tot_clone.GetBinError(i+1),staterr_post)
		print "bin{0:2}: {1:4.4} {2:4.4} +/- {3:4.4f} +/- {4:4.4f} | prefit = {5:4.4f}".format(i,curdat,curpos,hspostfit_tot_clone.GetBinError(i+1),staterr_post,curpre)
	print "tmptot = ", tmptot, tmptot2

	###################################################################################################
	## PLOTTING TIME!
	###################################################################################################

	dat_rat.SetMarkerStyle(34);
	dat_rat.SetMarkerSize(2);
	dat_rat_nounc.SetMarkerStyle(34);
	dat_rat_nounc.SetMarkerSize(2);	
	pre_rat.SetMarkerColor(2);
	pre_rat.SetMarkerStyle(24);
	pre_rat.SetMarkerSize(2);

	leg = TLegend(0.7,0.6,0.9,0.9);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.AddEntry(DataHist,"Data","pe")
	leg.AddEntry(hsprefit_tot,"PreFit","p")
	leg.AddEntry(histqcdpost,"QCD postfit","f")
	leg.AddEntry(histZpost,"Zinv postfit","f")
	leg.AddEntry(histTaupost,"Tau postfit","f")
	leg.AddEntry(histLLpost,"LL postfit","f")

	leg2 = TLegend(0.7,0.6,0.9,0.9);
	leg2.SetFillStyle(0);
	leg2.SetBorderSize(0);
	leg2.AddEntry(DataHist,"Data","pe")
	leg2.AddEntry(histqcdpost,"QCD postfit","f")
	leg2.AddEntry(histZpost,"Zinv postfit","f")
	leg2.AddEntry(histTaupost,"Tau postfit","f")
	leg2.AddEntry(histLLpost,"LL postfit","f")

	txta = TLatex(0.15,0.94,"CMS");
	txta.SetNDC(); txta.SetTextSize(0.035);
	txtb = TLatex(0.22,0.94,"Preliminary");
	txtb.SetNDC(); txtb.SetTextFont(52); txtb.SetTextSize(0.035);
	txtc = TLatex(0.70,0.94,"1.3 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.035);	

	canPost = TCanvas("canPost","canPost",1600,1200);
	p1 = TPad("p1","p1",0.0,0.3,1.0,0.97)
	p1.SetBottomMargin(0.05)
	p1.SetNumber(1)
	p2 = TPad("p2","p2",0.0,0.00,1.0,0.3)
	p2.SetNumber(2)
	p2.SetTopMargin(0.05)
	p2.SetBottomMargin(0.30)
	canPost.cd()
	p1.Draw(); p1.cd();	
	hspostfit.Draw('hist');
	hspostfit.GetYaxis().SetTitleOffset(0.7);
	hspostfit.SetTitle('; bin; yield')
	DataHistNew.Draw('pesames');
	hspostfit_tot_clone.Draw('e2sames');
	leg2.Draw();
	canPost.cd()
	p2.Draw(); p2.cd();
	dat_rat.SetMinimum(-3.);
	dat_rat.SetMaximum(3.);
	dat_rat.GetXaxis().SetTitleSize(0.15);
	dat_rat.GetYaxis().SetTitleSize(0.15);
	dat_rat.GetXaxis().SetTitleOffset(0.7);
	dat_rat.GetYaxis().SetTitleOffset(0.3);
	dat_rat.GetXaxis().SetLabelSize(0.1);
	dat_rat.GetYaxis().SetLabelSize(0.1);
	dat_rat.Draw('p');
	canPost.cd()
	txta.Draw();
	txtb.Draw();
	txtc.Draw();	
	canPost.SaveAs("plotstacks/poststack-pas.pdf");
	p1.SetLogy();
	hspostfit.SetMinimum(0.1);
	canPost.SaveAs("plotstacks/poststack_log-pas.pdf");
	
	canPostAN = TCanvas("canPostAN","canPostAN",1600,1200);
	p1AN = TPad("p1","p1",0.0,0.3,1.0,0.97)
	p1AN.SetBottomMargin(0.05)
	p1AN.SetNumber(1)
	p2AN = TPad("p2","p2",0.0,0.00,1.0,0.3)
	p2AN.SetNumber(2)
	p2AN.SetTopMargin(0.05)
	p2AN.SetBottomMargin(0.30)	
	canPostAN.cd()
	p1AN.Draw(); p1AN.cd();
	hspostfit.Draw('hist');
	hspostfit.GetYaxis().SetTitleOffset(0.7);
	hspostfit.SetTitle('; bin; yield')
	DataHistNew.Draw('pesames');
	hsprefit_tot.Draw('psames');
	hspostfit_tot_clone.Draw('e2sames');	
	leg.Draw();
	canPostAN.cd()	
	p2AN.Draw(); p2AN.cd();
	dat_rat.SetMinimum(-10.);
	dat_rat.SetMaximum(10.);	
	dat_rat.Draw('p');
	pre_rat.Draw('psames');
	canPostAN.cd()
	txta.Draw();
	txtb.Draw();
	txtc.Draw();		
	p1AN.SetLogy(0);
	canPostAN.SaveAs("plotstacks/poststack.pdf");
	p1AN.SetLogy(1);
	canPostAN.SaveAs("plotstacks/poststack_log.pdf");

	########################################################


	canPrePost = TCanvas("canPrePost","canPrePost",1200,800);
	prepost_rat_Z.SetMaximum(2.5);
	prepost_rat_Z.SetMinimum(-1.5);
	prepost_rat_Z.GetYaxis().SetTitleOffset(0.7);

	prepost_rat_Z.SetMarkerStyle(20);
	prepost_rat_Q.SetMarkerStyle(25);
	prepost_rat_L.SetMarkerStyle(30);
	prepost_rat_T.SetMarkerStyle(33);
	prepost_rat_Z.SetMarkerSize(2);
	prepost_rat_Q.SetMarkerSize(2);
	prepost_rat_L.SetMarkerSize(2);
	prepost_rat_T.SetMarkerSize(2);	
	prepost_rat_Z.SetMarkerColor(1);
	prepost_rat_Q.SetMarkerColor(2);
	prepost_rat_L.SetMarkerColor(4);
	prepost_rat_T.SetMarkerColor(6);		

	leg3 = TLegend(0.75,0.7,0.9,0.9);
	leg3.SetFillStyle(0);
	leg3.SetBorderSize(0);
	leg3.AddEntry(prepost_rat_Z,"Zinv","p")
	leg3.AddEntry(prepost_rat_Q,"QCD","p")
	leg3.AddEntry(prepost_rat_L,"lost lep","p")
	leg3.AddEntry(prepost_rat_T,"had #tau","p")

	prepost_rat_Z.Draw("p");
	prepost_rat_Q.Draw("psames");
	prepost_rat_L.Draw("psames");
	prepost_rat_T.Draw("psames");

	leg3.Draw();
	canPrePost.SaveAs("plotstacks/prepostcomp.pdf");

	####
	
	canPrePost_ovTot = TCanvas("canPrePost_ovTot","canPrePost_ovTot",1200,800);
	prepost_rat_Z_ovTot.SetMaximum(1.1 );
	prepost_rat_Z_ovTot.SetMinimum(-1.1);
	prepost_rat_Z_ovTot.GetYaxis().SetTitleOffset(0.7);

	prepost_rat_Z_ovTot.SetMarkerStyle(20);
	prepost_rat_Q_ovTot.SetMarkerStyle(25);
	prepost_rat_L_ovTot.SetMarkerStyle(30);
	prepost_rat_T_ovTot.SetMarkerStyle(33);
	prepost_rat_Z_ovTot.SetMarkerSize(2);
	prepost_rat_Q_ovTot.SetMarkerSize(2);
	prepost_rat_L_ovTot.SetMarkerSize(2);
	prepost_rat_T_ovTot.SetMarkerSize(2);	
	prepost_rat_Z_ovTot.SetMarkerColor(1);
	prepost_rat_Q_ovTot.SetMarkerColor(2);
	prepost_rat_L_ovTot.SetMarkerColor(4);
	prepost_rat_T_ovTot.SetMarkerColor(6);		

	leg3 = TLegend(0.75,0.7,0.9,0.9);
	leg3.SetFillStyle(0);
	leg3.SetBorderSize(0);
	leg3.AddEntry(prepost_rat_Z,"Zinv","p")
	leg3.AddEntry(prepost_rat_Q,"QCD","p")
	leg3.AddEntry(prepost_rat_L,"lost lep","p")
	leg3.AddEntry(prepost_rat_T,"had #tau","p")

	prepost_rat_Z_ovTot.Draw("p");
	prepost_rat_Q_ovTot.Draw("psames");
	prepost_rat_L_ovTot.Draw("psames");
	prepost_rat_T_ovTot.Draw("psames");

	leg3.Draw();
	canPrePost_ovTot.SaveAs("plotstacks/prepostcomp_ovTot.pdf");	

	
