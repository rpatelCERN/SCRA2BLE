import ROOT as root
from ROOT import *
import ROOT
import time
from array import array
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import math
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadTopMargin(0.08);
ROOT.gStyle.SetPalette(1);


#########################################################################################################
def GetPrefitErrorsFromJack(fn):
	f = open(fn,'r');

	errup = [];
	errdn = [];
	for line in f:
		linelist = line.strip().split();
		#print linelist;
		errup.append(float(linelist[1]))
		errdn.append(float(linelist[2]))
		#print errup, errdn
		#errup.append( math.sqrt( float(linelist[4])*float(linelist[4]) + float(linelist[6])*float(linelist[6]) ) );
		#errdn.append( math.sqrt( float(linelist[8])*float(linelist[8]) + float(linelist[10])*float(linelist[10]) ) );

	return (errup,errdn);

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
	
	#theDir = 'testCards-allBkgs-SMSbbbb1500-2.1-mu0.0'
	# theDir = 'testCards-allBkgswithPho-SMSbbbb1500-2.1-mu0.0'
	#theDir = 'testCards-allBkgsTestingFit-SMSbbbb1500-2.1-mu0.0';
	theDir='/fdata/hepx/store/user/rish/CombineCards/Unblinding/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/testCards-allBkgs-T1tttt_1500_100-36.3-mu0.0/'
	fin=TFile("/fdata/hepx/store/user/rish/CombineCards/Unblinding/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder"+"/mlfittestCards-allBkgs-T1tttt_1500_100-36.3-mu0.0.root", "READ")
	#fin=TFile("/fdata/hepx/store/user/rish/CombineCards//CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/"+"/mlfittestCards-allBkgs-T1tttt_1200_800-24.5-mu0.0.root", "READ")
	BinProcesses=fin.Get("norm_fit_b");
	mybins=[]
	searchbins=[]
	hsprefit = THStack();
	hspostfit = THStack();


	YieldsFile=TFile(theDir+"/yields.root", "READ")
	histqcd=YieldsFile.Get("QCD")
	histZ=YieldsFile.Get("Zvv")
	histTau=YieldsFile.Get("tau")
	histLL=YieldsFile.Get("LL")
	DataHist=YieldsFile.Get("data")
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
	for c in range(1,176):
		#sig = BinProcesses.find("ch%d/sig" %c)
		Z   = BinProcesses.find("ch%d/zvv" %c)
		Q   = BinProcesses.find("ch%d/qcd" %c)
		T   = BinProcesses.find("ch%d/WTopHad" %c)
		L   = BinProcesses.find("ch%d/WTopSL" %c)
	        C   = BinProcesses.find("ch%d/contam" %c)
			
		mybins.append(c)
			#just need to find this once (mapping to search bins):
		'''
		for i in range(0,174):
			fcardname = theDir+"/card_signal%d.txt" %i;
			fcard=open(fcardname)
			fcard.seek(0)
			for line in fcard:
				parse=line.split(' ')
				if parse[0]=='rate':
					eps=1e-3
					if(abs(L.getVal()-float(parse[2]))<eps and abs(T.getVal()-float(parse[4]))<eps and abs(Z.getVal()-float(parse[6]))<eps and abs(Q.getVal()-float(parse[7]))<eps):
		'''
		searchbins.append(c-1)
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

	histqcdpost=TH1F("histqcdpost", "QCD post-fit Yields", 174, 0.5, 174.5);
	histZpost=TH1F("histZpost", "Zinv post-fit Yields", 174, 0.5, 174.5);
	histTaupost=TH1F("histTaupost", "Tau post-fit Yields", 174, 0.5, 174.5);
	histLLpost=TH1F("histLLpost", "Lost Lepton post-fit Yields", 174, 0.5, 174.5);
	
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
	for c in range(1,175):
		Z=BinProcessesPostFit.find("ch%d/zvv" %c)
		Q=BinProcessesPostFit.find("ch%d/qcd" %c)
		T=BinProcessesPostFit.find("ch%d/WTopHad" %c)
		L=BinProcessesPostFit.find("ch%d/WTopSL" %c)

		TZ   = BinProcessesPostFit.find("ch%d/WTopSLHighW" %c)
		LZ   = BinProcessesPostFit.find("ch%d/WTopHadHighW" %c)
		#print (c+1),"TZ,LZ = ", TZ.getVal(), LZ.getVal()
		histZpost.SetBinContent(c, Z.getVal())
		histZpost.SetBinError(c, Z.getError())
		histqcdpost.SetBinContent(c, Q.getVal())
		histLLpost.SetBinContent(c, L.getVal()+LZ.getVal())
		histLLpost.SetBinError(c, math.sqrt((L.getError()*L.getError())+(LZ.getError()*LZ.getError())))
		histTaupost.SetBinContent(c, T.getVal()+TZ.getVal())
		histTaupost.SetBinError(c, math.sqrt((T.getError()*T.getError())+(TZ.getError()*TZ.getError())))

		qerr = Q.getError()
		if Q.getError()/Q.getVal() > 100 and Q.getError() > 1.0: 
			qerr = 0.0;
			# print "Outlier Rejection!!"
		histqcdpost.SetBinError(searchbins[c]+1, qerr)

		# print "XX content, bin {0:2}: {1:6.4f} +- {2:6.4f}, {3:6.4f} +- {4:6.4f}, {5:6.4f} +- {6:6.4f}, {7:6.4f} +- {8:6.4f}".format(c,Z.getVal(),Z.getError(),Q.getVal(),Q.getError(),L.getVal(),L.getError(),T.getVal(),T.getError());
		#print "{0:2} & {1:6.2f} \pm {2:6.2f} & {3:6.2f} \pm {4:6.2f} & {5:6.2f} \pm {6:6.2f} & {7:6.2f} \pm {8:6.2f} \\\\".format(c,Z.getVal(),Z.getError(),Q.getVal(),Q.getError(),L.getVal(),L.getError(),T.getVal(),T.getError());		

	hspostfit.Add(histqcdpost)
	hspostfit.Add(histZpost)
	hspostfit.Add(histTaupost)
	hspostfit.Add(histLLpost)
	hspostfit_tot = hspostfit.GetStack().Last();

	hspostfit_tot_clone = hspostfit_tot.Clone();
	hspostfit_tot_clone.SetFillStyle(3013);
	hspostfit_tot_clone.SetFillColor(13);
	hspostfit_tot_clone.SetMarkerSize(0);

	# for i in range(hsprefit_tot.GetNbinsX()):
	# 	print "bin {0:2}: {1:6.2f} {2:6.2f}".format(i,hsprefit_tot.GetBinContent(i+1),hspostfit_tot.GetBinContent(i+1));

	#DataIn = TFile("../inputHistograms/histograms_2.1fb/RA2bin_signalUnblind.root");
	#DataHist = DataIn.Get("RA2bin_data");
	DataHist.SetBinErrorOption(ROOT.TH1F.kPoisson);
	DataHist.SetMarkerStyle(34);
	DataHist.SetMarkerSize(2);
	hsprefit_tot.SetMarkerStyle(24);
	hsprefit_tot.SetMarkerSize(2);
	hsprefit_tot.SetMarkerColor(2);
	hsprefit_tot.SetLineColor(2);

	dat_rat = TH1F('dat_rat',';bin;pull',174,0.5,174.5);
	dat_rat_nounc = TH1F('dat_rat_nounc',';bin;obs/pred',174,0.5,174.5);
	pre_rat = TH1F('pre_rat','Pull=;bin;pull',174,0.5,174.5);
	pre_rathisto=TH1F('pre_rat_histo', ';(N_{post}-N_{pre})/#sigma_{pre};Freq per bin;',30,-3,3)
	post_rathisto=TH1F('post_rat_histo', ';(N_{obs}-N_{post})/#sigma_{post};Freq per bin;',30,-3,3)
	
	prepost_rat_Z = TH1F('prepost_rat_Z',';bin;(postfit_{i}-prefit_{i})/prefit_{i}',174,0.5,174.5);
	prepost_rat_Q = TH1F('prepost_rat_Q',';bin;fraction change',174,0.5,174.5);
	prepost_rat_L = TH1F('prepost_rat_L',';bin;fraction change',174,0.5,174.5);
	prepost_rat_T = TH1F('prepost_rat_T',';bin;fraction change',174,0.5,174.5);

	prepost_rat_Z_ovTot = TH1F('prepost_rat_Z_ ovTot',';bin;(postfit_{i}-prefit_{i})/#sigma_{prefit}',174,0.5,174.5);
	prepost_rat_Q_ovTot = TH1F('prepost_rat_Q_ ovTot',';bin;fraction change',174,0.5,174.5);
	prepost_rat_L_ovTot = TH1F('prepost_rat_L_ ovTot',';bin;fraction change',174,0.5,174.5);
	prepost_rat_T_ovTot = TH1F('prepost_rat_T_ ovTot',';bin;fraction change',174,0.5,174.5);


	tmptot = 0;
	tmptot2 = 0;
	DataHistNew = ROOT.TH1F("DataHistNew",";yield;bins",174,0.5,174.5);
	DataHistNew.SetBinErrorOption(ROOT.TH1.kPoisson);
	
	PostFitErrorsNew = ROOT.TH1F("PostFitErrorsNew",";yield;bins",174,0.5,174.5);
	PostFitErrorsNew.SetBinErrorOption(ROOT.TH1.kPoisson);
	PostFitErrorsNew.SetFillStyle(3013);
	PostFitErrorsNew.SetFillColor(13);
	PostFitErrorsNew.SetMarkerSize(0);

	a_jets = array('d', [2,3,4,6,8,20]);	
	a_btags = array('d', [0,1,2,3,20]);	
	a_MHT= array('d', [300,350,500,750,2100]);	
	a_HT= array('d', [300,500,1000,2100]);	
	NJetsData=TH1F('NJetsData', ";NJets;Yields", 5,a_jets)
	NJetsData.Sumw2(kFALSE)
	NJetsData.SetBinErrorOption(ROOT.TH1.kPoisson);
	NBtagsData=TH1F('NBtagsData', ";NBtags;Yields", 4,a_btags)
	MHTData=TH1F('MHTData', ";MHT;Yields", 4,a_MHT)
	HTData=TH1F('HTData', ";HT;Yields", 3,a_HT)

	NJetsPreFit=TH1F('NJetsPreFit', ";NJets;Yields", 5,a_jets)
	NBtagsPreFit=TH1F('NBtagsPreFit', ";NBtags;Yields", 4,a_btags)
	MHTPreFit=TH1F('MHTPreFit', ";MHT;Yields", 4,a_MHT)
	HTPreFit=TH1F('HTPreFit', ";HT;Yields", 3,a_HT)
	
	NJetsHTauPostFit=TH1F('NJetsHTauPostFit', ";NJets;Yields", 5,a_jets)
	NBtagsHTauPostFit=TH1F('NBtagsHTauPostFit', ";NBtags;Yields", 4,a_btags)
	MHTHTauPostFit=TH1F('MHTHTauPostFit', ";MHT;Yields", 4,a_MHT)
	HTHTauPostFit=TH1F('HTHTauPostFit', ";HT;Yields", 3,a_HT)
	NJetsLostLPostFit=TH1F('NJetsLostLPostFit', ";NJets;Yields", 5,a_jets)
	NBtagsLostLPostFit=TH1F('NBtagsLostLPostFit', ";NBtags;Yields", 4,a_btags)
	MHTLostLPostFit=TH1F('MHTLostLPostFit', ";MHT;Yields", 4,a_MHT)
	HTLostLPostFit=TH1F('HTLostLPostFit', ";HT;Yields", 3,a_HT)
	NJetsQCDPostFit=TH1F('NJetsQCDPostFit', ";NJets;Yields", 5,a_jets)
	NBtagsQCDPostFit=TH1F('NBtagsQCDPostFit', ";NBtags;Yields", 4,a_btags)
	MHTQCDPostFit=TH1F('MHTQCDPostFit', ";MHT;Yields", 4,a_MHT)
	HTQCDPostFit=TH1F('HTQCDPostFit', ";HT;Yields", 3,a_HT)
	
	NJetsZPostFit=TH1F('NJetsZPostFit', ";NJets;Yields", 5,a_jets)
	NBtagsZPostFit=TH1F('NBtagsZPostFit', ";NBtags;Yields", 4,a_btags)
	MHTZPostFit=TH1F('MHTZPostFit', ";MHT;Yields", 4,a_MHT)
	HTZPostFit=TH1F('HTZPostFit', ";HT;Yields", 3,a_HT)
		
	NJetsZPostFit.SetFillColor(2002);
	NJetsQCDPostFit.SetFillColor(2001);
	NJetsHTauPostFit.SetFillColor(2007);
	NJetsLostLPostFit.SetFillColor(2006);
	NBtagsZPostFit.SetFillColor(2002);
	NBtagsQCDPostFit.SetFillColor(2001);
	NBtagsHTauPostFit.SetFillColor(2007);
	NBtagsLostLPostFit.SetFillColor(2006);
	HTZPostFit.SetFillColor(2002);
	HTQCDPostFit.SetFillColor(2001);
	HTHTauPostFit.SetFillColor(2007);
	HTLostLPostFit.SetFillColor(2006);
	MHTZPostFit.SetFillColor(2002);
	MHTQCDPostFit.SetFillColor(2001);
	MHTHTauPostFit.SetFillColor(2007);
	MHTLostLPostFit.SetFillColor(2006);
	
	flabels=TFile("../inputHistograms/fastsimSignalT1tttt/RA2bin_signal.root","READ")
	labels=flabels.Get("RA2bin_T1tttt_1500_100_fast")
	for i in range(1,175):
		binlabel=labels.GetXaxis().GetBinLabel(i)	
		if "NJets0" in binlabel:
			NJetsPreFit.Fill(2.5,hsprefit_tot.GetBinContent(i)); 
			NJetsData.Fill(2.5,DataHist.GetBinContent(i)); 
			NJetsQCDPostFit.Fill(2.5,histqcdpost.GetBinContent(i))
			NJetsZPostFit.Fill(2.5,histZpost.GetBinContent(i))
			NJetsHTauPostFit.Fill(2.5,histTaupost.GetBinContent(i))
			NJetsLostLPostFit.Fill(2.5,histLLpost.GetBinContent(i))
		if "NJets1" in binlabel:
			NJetsPreFit.Fill(3.5,hsprefit_tot.GetBinContent(i)); 
			NJetsData.Fill(3.5,DataHist.GetBinContent(i)); 
			NJetsQCDPostFit.Fill(3.5,histqcdpost.GetBinContent(i))
			NJetsZPostFit.Fill(3.5,histZpost.GetBinContent(i))
			NJetsHTauPostFit.Fill(3.5,histTaupost.GetBinContent(i))
			NJetsLostLPostFit.Fill(3.5,histLLpost.GetBinContent(i))

		if "NJets2" in binlabel:
			NJetsPreFit.Fill(5,hsprefit_tot.GetBinContent(i));
			NJetsData.Fill(5,DataHist.GetBinContent(i));
			NJetsQCDPostFit.Fill(5,histqcdpost.GetBinContent(i))
			NJetsZPostFit.Fill(5,histZpost.GetBinContent(i))
			NJetsHTauPostFit.Fill(5,histTaupost.GetBinContent(i))
			NJetsLostLPostFit.Fill(5,histLLpost.GetBinContent(i))
	 
		if "NJets3" in binlabel:
			NJetsPreFit.Fill(7,hsprefit_tot.GetBinContent(i));
			NJetsData.Fill(7,DataHist.GetBinContent(i));
			NJetsQCDPostFit.Fill(7,histqcdpost.GetBinContent(i))
			NJetsZPostFit.Fill(7,histZpost.GetBinContent(i))
			NJetsHTauPostFit.Fill(7,histTaupost.GetBinContent(i))
			NJetsLostLPostFit.Fill(7,histLLpost.GetBinContent(i))
		if "NJets4" in binlabel:
			NJetsPreFit.Fill(9,hsprefit_tot.GetBinContent(i)); 
			NJetsData.Fill(9,DataHist.GetBinContent(i)); 
			NJetsQCDPostFit.Fill(9,histqcdpost.GetBinContent(i))
			NJetsZPostFit.Fill(9,histZpost.GetBinContent(i))
			NJetsHTauPostFit.Fill(9,histTaupost.GetBinContent(i))
			NJetsLostLPostFit.Fill(9,histLLpost.GetBinContent(i))
			print "Post-fit at High NJ %g %g " %(histqcdpost.GetBinContent(i),histZpost.GetBinContent(i)) 
		if "BTags0" in binlabel:
			NBtagsPreFit.Fill(0.1,hsprefit_tot.GetBinContent(i)); 
			NBtagsData.Fill(0.1,DataHist.GetBinContent(i)); 
			NBtagsQCDPostFit.Fill(0.5,histqcdpost.GetBinContent(i))
			NBtagsZPostFit.Fill(0.5,histZpost.GetBinContent(i))
			NBtagsHTauPostFit.Fill(0.5,histTaupost.GetBinContent(i))
			NBtagsLostLPostFit.Fill(0.5,histLLpost.GetBinContent(i))

		if "BTags1" in binlabel:
			NBtagsPreFit.Fill(1.5,hsprefit_tot.GetBinContent(i)); 
			NBtagsQCDPostFit.Fill(1.5,histqcdpost.GetBinContent(i))
			NBtagsZPostFit.Fill(1.5,histZpost.GetBinContent(i))
			NBtagsHTauPostFit.Fill(1.5,histTaupost.GetBinContent(i))
			NBtagsLostLPostFit.Fill(1.5,histLLpost.GetBinContent(i))
			NBtagsData.Fill(1.5,DataHist.GetBinContent(i)); 
		if "BTags2" in binlabel:
		        NBtagsPreFit.Fill(2.5,hsprefit_tot.GetBinContent(i));	
			NBtagsData.Fill(2.5,DataHist.GetBinContent(i)); 
			NBtagsQCDPostFit.Fill(2.5,histqcdpost.GetBinContent(i))
			NBtagsZPostFit.Fill(2.5,histZpost.GetBinContent(i))
			NBtagsHTauPostFit.Fill(2.5,histTaupost.GetBinContent(i))
			NBtagsLostLPostFit.Fill(2.5,histLLpost.GetBinContent(i))
		if "BTags3" in binlabel:
			NBtagsPreFit.Fill(4,hsprefit_tot.GetBinContent(i)); 
			NBtagsData.Fill(4,DataHist.GetBinContent(i)); 
			NBtagsQCDPostFit.Fill(4,histqcdpost.GetBinContent(i))
			NBtagsZPostFit.Fill(4,histZpost.GetBinContent(i))
			NBtagsHTauPostFit.Fill(4,histTaupost.GetBinContent(i))
			NBtagsLostLPostFit.Fill(4,histLLpost.GetBinContent(i))
		if "MHT0" in binlabel:
			MHTPreFit.Fill(325, hsprefit_tot.GetBinContent(i))
			MHTData.Fill(325, DataHist.GetBinContent(i))
			MHTQCDPostFit.Fill(325,histqcdpost.GetBinContent(i))
			MHTZPostFit.Fill(325,histZpost.GetBinContent(i))
			MHTHTauPostFit.Fill(325,histTaupost.GetBinContent(i))
			MHTLostLPostFit.Fill(325,histLLpost.GetBinContent(i))

		if "MHT1" in binlabel:
			MHTPreFit.Fill(375, hsprefit_tot.GetBinContent(i))
			MHTData.Fill(375, DataHist.GetBinContent(i))
			MHTQCDPostFit.Fill(375,histqcdpost.GetBinContent(i))
			MHTZPostFit.Fill(375,histZpost.GetBinContent(i))
			MHTHTauPostFit.Fill(375,histTaupost.GetBinContent(i))
			MHTLostLPostFit.Fill(375,histLLpost.GetBinContent(i))
		if "MHT2" in binlabel:
			MHTPreFit.Fill(525, hsprefit_tot.GetBinContent(i))
			MHTData.Fill(525, DataHist.GetBinContent(i))
			MHTQCDPostFit.Fill(525,histqcdpost.GetBinContent(i))
			MHTZPostFit.Fill(525,histZpost.GetBinContent(i))
			MHTHTauPostFit.Fill(525,histTaupost.GetBinContent(i))
			MHTLostLPostFit.Fill(525,histLLpost.GetBinContent(i))

		if "MHT3" in binlabel:
			MHTPreFit.Fill(900, hsprefit_tot.GetBinContent(i))
			MHTData.Fill(900, DataHist.GetBinContent(i))
			MHTQCDPostFit.Fill(900,histqcdpost.GetBinContent(i))
			MHTZPostFit.Fill(900,histZpost.GetBinContent(i))
			MHTHTauPostFit.Fill(900,histTaupost.GetBinContent(i))
			MHTLostLPostFit.Fill(900,histLLpost.GetBinContent(i))
		if "HT0" in binlabel or "HT3" in binlabel:
			HTPreFit.Fill(325, hsprefit_tot.GetBinContent(i))			
			HTQCDPostFit.Fill(325,histqcdpost.GetBinContent(i))
			HTZPostFit.Fill(325,histZpost.GetBinContent(i))
			HTHTauPostFit.Fill(325,histTaupost.GetBinContent(i))
			HTLostLPostFit.Fill(325,histLLpost.GetBinContent(i))
			HTData.Fill(325, DataHist.GetBinContent(i))			
		if "HT1" in binlabel or "HT4" in binlabel or "HT6" in binlabel or "HT8" in binlabel:
			HTPreFit.Fill(600, hsprefit_tot.GetBinContent(i))			
			HTData.Fill(600, DataHist.GetBinContent(i))			
			HTQCDPostFit.Fill(600,histqcdpost.GetBinContent(i))
			HTZPostFit.Fill(600,histZpost.GetBinContent(i))
			HTHTauPostFit.Fill(600,histTaupost.GetBinContent(i))
			HTLostLPostFit.Fill(600,histLLpost.GetBinContent(i))
		if "HT2" in binlabel or "HT5" in binlabel or "HT7" in binlabel or "HT9" in binlabel:
			HTPreFit.Fill(1100, hsprefit_tot.GetBinContent(i))			
			HTData.Fill(1100, DataHist.GetBinContent(i))			
			HTQCDPostFit.Fill(1100,histqcdpost.GetBinContent(i))
			HTZPostFit.Fill(1100,histZpost.GetBinContent(i))
			HTHTauPostFit.Fill(1100,histTaupost.GetBinContent(i))
			HTLostLPostFit.Fill(1100,histLLpost.GetBinContent(i))
		
	hpostfitNJets = THStack();
	hpostfitNJets.Add(NJetsQCDPostFit)
	hpostfitNJets.Add(NJetsZPostFit)
	hpostfitNJets.Add(NJetsHTauPostFit)
	hpostfitNJets.Add(NJetsLostLPostFit)

	hpostfitNBtags = THStack();
	hpostfitNBtags.Add(NBtagsQCDPostFit)
	hpostfitNBtags.Add(NBtagsZPostFit)
	hpostfitNBtags.Add(NBtagsHTauPostFit)
	hpostfitNBtags.Add(NBtagsLostLPostFit)

	hpostfitMHT = THStack();
	hpostfitMHT.Add(MHTQCDPostFit)
	hpostfitMHT.Add(MHTZPostFit)
	hpostfitMHT.Add(MHTHTauPostFit)
	hpostfitMHT.Add(MHTLostLPostFit)
	hpostfitHT = THStack();
	hpostfitHT.Add(HTQCDPostFit)
	hpostfitHT.Add(HTZPostFit)
	hpostfitHT.Add(HTHTauPostFit)
	hpostfitHT.Add(HTLostLPostFit)

	TMP1 = ROOT.TH1F("TMP1","TMP1",1,0,1);
	errorsPrefitFromJack_Up,errorsPrefitFromJack_Dn  = GetPrefitErrorsFromJack("ParsedInputPrefit.txt");
	for i in range(dat_rat.GetNbinsX()):
		Z=BinProcessesPostFit.find("ch%d/zvv" %mybins[i])
		Q=BinProcessesPostFit.find("ch%d/qcd" %mybins[i])
		T=BinProcessesPostFit.find("ch%d/WTopHad" %mybins[i])
		L=BinProcessesPostFit.find("ch%d/WTopSL" %mybins[i])
		TZ   = BinProcessesPostFit.find("ch%d/WTopSLHighW" %mybins[i])
		LZ   = BinProcessesPostFit.find("ch%d/WTopHadHighW" %mybins[i])

		DataHistNew.SetBinContent(i+1,DataHist.GetBinContent(i+1));
		staterr_dat = max(DataHistNew.GetBinErrorUp(i+1),DataHistNew.GetBinErrorLow(i+1));

		PostFitErrorsNew.SetBinContent(i+1,hspostfit_tot.GetBinContent(i+1));
		staterr_post = max(PostFitErrorsNew.GetBinErrorUp(i+1),PostFitErrorsNew.GetBinErrorLow(i+1));
		#print i+1, DataHist.GetBinContent(i+1)
		#print DataHistNew.GetBinErrorUp(i+1),DataHistNew.GetBinErrorLow(i+1)
		# print DataHist.GetBinContent(i+1),TMP1.GetBinErrorUp(i+1),TMP1.GetBinErrorLow(i+1),hsprefit_tot.GetBinError(i+1)

		curerr_dat = math.sqrt(hspostfit_tot_clone.GetBinError(i+1)*hspostfit_tot_clone.GetBinError(i+1) + staterr_post*staterr_post);
		curerr_pre = math.sqrt(hspostfit_tot_clone.GetBinError(i+1)*hspostfit_tot_clone.GetBinError(i+1) + staterr_post*staterr_post);
		curdat = DataHist.GetBinContent(i+1);
		curpre = hsprefit_tot.GetBinContent(i+1);
		curpos = hspostfit_tot.GetBinContent(i+1);
		i_dat_rat = (curdat-curpos)/curerr_dat;
		
		#print errorsPrefitFromJack_Up[i],errorsPrefitFromJack_Dn[i],curpre,curpos
		#i_pre_rat = (curpre-curpos)/errorsPrefitFromJack_Up[i];
		i_pre_rat = (curpos-curpre)/curerr_dat;
		if curpos-curpre > 0 and errorsPrefitFromJack_Up[i]>0: i_pre_rat = (curpos-curpre)/errorsPrefitFromJack_Up[i]
		if curpos-curpre < 0 and errorsPrefitFromJack_Dn[i]>0: i_pre_rat = (curpos-curpre)/errorsPrefitFromJack_Dn[i]
		pre_rathisto.Fill(i_pre_rat);
		hsprefit_tot.SetBinError(i+1,max(errorsPrefitFromJack_Dn[i],errorsPrefitFromJack_Up[i]))

		dat_rat.SetBinContent(i+1,i_dat_rat)
		post_rathisto.Fill(i_dat_rat)
		dat_rat_nounc.SetBinContent(i+1,curdat/curpos)
		pre_rat.SetBinContent(i+1,i_pre_rat)
		
		if histZ.GetBinContent(i+1)>0.0:
			prepost_rat_Z.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/histZ.GetBinContent(i+1));
			#print "Znunu bin %d %g %g " %(i+1, histZpost.GetBinContent(i+1), histZ.GetBinContent(i+1))
		else:prepost_rat_Z.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1)))

		if histqcd.GetBinContent(i+1)>0.0: prepost_rat_Q.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1))/histqcd.GetBinContent(i+1));
		else: prepost_rat_Q.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1)))
		if histLL.GetBinContent(i+1)>0.0:prepost_rat_L.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1))/histLL.GetBinContent(i+1));
		else: prepost_rat_L.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1)))
		if histTau.GetBinContent(i+1)>0.0:prepost_rat_T.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1))/histTau.GetBinContent(i+1));
		else: prepost_rat_T.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1)))
		#print "Bin %d %g %g %g %g" %(i+1, histTaupost.GetBinContent(i+1), histTau.GetBinContent(i+1), (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1)), prepost_rat_T.GetBinContent(i+1))
		if curpre-curpos <0:
			prepost_rat_Z_ovTot.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/errorsPrefitFromJack_Up[i]);
			#print i+1,histZpost.GetBinContent(i+1),histZ.GetBinContent(i+1), errorsPrefitFromJack_Up[i],(histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/errorsPrefitFromJack_Up[i]
			prepost_rat_Q_ovTot.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1))/errorsPrefitFromJack_Up[i]);
			prepost_rat_L_ovTot.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1))/errorsPrefitFromJack_Up[i]);
			prepost_rat_T_ovTot.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1))/errorsPrefitFromJack_Up[i]);
		if errorsPrefitFromJack_Dn[i]>0.0 and curpre-curpos>=0:
			prepost_rat_Z_ovTot.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1))/errorsPrefitFromJack_Dn[i]);
                        prepost_rat_Q_ovTot.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1))/errorsPrefitFromJack_Dn[i]);
                        prepost_rat_L_ovTot.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1))/errorsPrefitFromJack_Dn[i]);
                        prepost_rat_T_ovTot.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1))/errorsPrefitFromJack_Dn[i]);
		if errorsPrefitFromJack_Dn[i]==0.0:
			prepost_rat_Z_ovTot.SetBinContent(i+1, (histZpost.GetBinContent(i+1)-histZ.GetBinContent(i+1)));
                        prepost_rat_Q_ovTot.SetBinContent(i+1, (histqcdpost.GetBinContent(i+1)-histqcd.GetBinContent(i+1)));
                        prepost_rat_L_ovTot.SetBinContent(i+1, (histLLpost.GetBinContent(i+1)-histLL.GetBinContent(i+1)));
                        prepost_rat_T_ovTot.SetBinContent(i+1, (histTaupost.GetBinContent(i+1)-histTau.GetBinContent(i+1)));

		if i >= 60: tmptot += curpos;
		if i >= 60: tmptot2 += curpre;
		# print "bin{0:2}: {1:4} {2:6} +/- {7:6f} +/- {8:6f} ||| Z={3:4f} Q={4:4f} L={5:4f} T={6:4f}".format(i,curdat,curpos,histZpost.GetBinContent(i+1),histqcdpost.GetBinContent(i+1),histLLpost.GetBinContent(i+1),histTaupost.GetBinContent(i+1),hspostfit_tot_clone.GetBinError(i+1),staterr_post)
		#print "bin{0:2}: {1:4.4} {2:4.4} +/- {3:4.4f} +/- {4:4.4f} | prefit = {5:4.4f}".format(i,curdat,curpos,hspostfit_tot_clone.GetBinError(i+1),staterr_post,curpre)
		print "{0:2} & ${1:6.2f} \pm {2:6.2f}$ & ${3:6.2f} \pm {4:6.2f}$ & ${5:6.2f} \pm {6:6.2f}$ & ${7:6.2f} \pm {8:6.2f}$ & ${9:6.2f} \pm {10:6.2f}$ & ${11:1}$ \\\\ \hline".format(i+1,histLLpost.GetBinContent(i+1),histLLpost.GetBinError(i+1),histTaupost.GetBinContent(i+1),histTaupost.GetBinError(i+1),histZpost.GetBinContent(i+1),histZpost.GetBinError(i+1),histqcdpost.GetBinContent(i+1),histqcdpost.GetBinError(i+1),curpos,hspostfit_tot.GetBinError(i+1),int(curdat));		
		#print " %d &  %g & %g & %g & %g " %(i+1, histLL.GetBinContent(i+1),histTau.GetBinContent(i+1),histZ.GetBinContent(i+1), histqcd.GetBinContent(i+1))
		#print "%d & %g %g %g" %(i+1, histZ.GetBinContent(i+1),histZ.GetBinContent(i+1) , prepost_rat_Z.GetBinContent(i+1))
		#print "bin{0:2}: {1:4} {2:4.2f} {5:4.2f}".format(i+1,curdat,curpos,hspostfit_tot_clone.GetBinError(i+1),staterr_post,curpre)
	#	print "bin{0:2}: & ${1:6.2f} \pm {2:6.2f}$ \\\\ \hline".format(i+1,Q.getVal(),Q.getError())
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

	leg = TLegend(0.55,0.6,0.9,0.87);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(0.04);	
	leg.AddEntry(DataHist,"Data","pe")
	leg.AddEntry(hsprefit_tot,"Pre-fit total background","p")
	leg.AddEntry(None,"Post-fit backgrounds:","")
	leg.AddEntry(histqcdpost,"QCD","f")
	leg.AddEntry(histZpost,"Z#rightarrow#nu#bar{#nu}","f")
	leg.AddEntry(histTaupost,"Hadronic #tau lepton","f")
	leg.AddEntry(histLLpost,"Lost lepton","f")

	leg2 = TLegend(0.55,0.55,0.9,0.87);
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
	txtc = TLatex(0.70,0.94,"36.3 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.035);	

	txt1 = TLatex(0.25,0.25,"pull_{data} = (N_{obs}-N_{post})/#sigma_{post}");
	txt1.SetNDC(); txt1.SetTextFont(42); txt1.SetTextSize(0.030);
	txt2 = TLatex(0.55,0.25,"pull_{prefit} = (N_{post}-N_{pre})/#sigma_{pre}");
	txt2.SetNDC(); txt2.SetTextFont(42); txt2.SetTextSize(0.030);

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
	#hspostfit_tot_clone.Draw('e2sames');
	PostFitErrorsNew.Draw('e2sames');
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
	hsprefit_tot.Draw('pesames');
	PostFitErrorsNew.Draw('e3sames');
	leg.Draw();
	canPostAN.cd()	
	p2AN.Draw(); p2AN.cd();
	dat_rat.SetMinimum(-4.);
	dat_rat.SetMaximum(4.);	
	dat_rat.Draw('p');
	pre_rat.Draw('psames');
	canPostAN.cd()
	txta.Draw();
	txtb.Draw();
	txtc.Draw();		
	txt1.Draw();
	txt2.Draw();	
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
	canPostPull=TCanvas("canPostPull","canPostPull",1200,800);
	pre_rathisto.GetYaxis().SetTitleOffset(0.7);
	post_rathisto.GetYaxis().SetTitleOffset(0.7);
	canPostPull.Divide(2,1)

	canPostPull.cd(1);
	txtc.Draw()	
	pre_rathisto.Draw()
	canPostPull.cd(2)
	txtc.Draw()
	post_rathisto.Draw()
	canPostPull.SaveAs("plotstacks/pre_rathisto.pdf")
	canPost1DProj=TCanvas("canPost1DProj","canPostPull",1600,1200);
	#canPost1DProj.Divide(2,2)
	#canPost1DProj.cd(1)
	canPost1DProj.SetLogy()
	hpostfitNJets.Draw("hist")
	hpostfitNJets.SetTitle('NJets: Post-Fit Backgrounds; N_{Jets}; yield')
	hpostfitNJets.GetYaxis().SetTitleOffset(0.7);
	hpostfitNJets.SetMinimum(10);
	hpostfitNBtags.Draw("hist")
	hpostfitNBtags.SetTitle('NBtags: Post-Fit Backgrounds; N_{BTags}; yield')
	hpostfitNBtags.GetYaxis().SetTitleOffset(0.7);
	hpostfitNBtags.SetMinimum(10);
	hpostfitMHT.Draw("hist")
	hpostfitMHT.SetTitle('MHT: Post-Fit Backgrounds; Missing H_{T}; yield')
	hpostfitMHT.GetYaxis().SetTitleOffset(0.7);
	hpostfitMHT.SetMinimum(10);
	hpostfitHT.Draw("hist")
	hpostfitHT.SetTitle('HT: Post-Fit Backgrounds;H_{T}; yield')
	hpostfitHT.GetYaxis().SetTitleOffset(0.7);
	hpostfitHT.SetMinimum(800);

	NJetsPreFit.SetMarkerStyle(24);
	NJetsPreFit.SetMarkerSize(2);
	NJetsPreFit.SetMarkerColor(2);
	NJetsPreFit.SetLineColor(2);
        NBtagsPreFit.SetMarkerStyle(24);
        NBtagsPreFit.SetMarkerSize(2);
        NBtagsPreFit.SetMarkerColor(2);
        NBtagsPreFit.SetLineColor(2);
        MHTPreFit.SetMarkerStyle(24);
        MHTPreFit.SetMarkerSize(2);
        MHTPreFit.SetMarkerColor(2);
        MHTPreFit.SetLineColor(2);
        HTPreFit.SetMarkerStyle(24);
        HTPreFit.SetMarkerSize(2);
        HTPreFit.SetMarkerColor(2);
        HTPreFit.SetLineColor(2);
	MHTDataNew=TH1F('MHTData', ";MHT;Yields", 4,a_MHT)
	HTDataNew=TH1F('HTData', ";HT;Yields", 3,a_HT)
	NBtagsDataNew=TH1F('NBtagsData', ";NBtags;Yields", 4,a_btags)
	NJetsDataNew=TH1F('NJetsData', ";NJets;Yields", 5,a_jets)
	NJetsDataNew.SetBinErrorOption(ROOT.TH1F.kPoisson);
	NBtagsDataNew.SetBinErrorOption(ROOT.TH1F.kPoisson);
	HTDataNew.SetBinErrorOption(ROOT.TH1F.kPoisson);
	HTDataNew.SetBinErrorOption(ROOT.TH1F.kPoisson);
	for i in range(NJetsData.GetNbinsX()+1):NJetsDataNew.SetBinContent(i,  NJetsData.GetBinContent(i));
	for i in range(NBtagsData.GetNbinsX()+1):NBtagsDataNew.SetBinContent(i,  NBtagsData.GetBinContent(i));
	for i in range(HTData.GetNbinsX()+1):HTDataNew.SetBinContent(i,  HTData.GetBinContent(i));
	for i in range(MHTData.GetNbinsX()+1):MHTDataNew.SetBinContent(i,  MHTData.GetBinContent(i));
	p4 = TPad("p4","p1",0.0,0.3,1.0,0.97)
	p4.SetBottomMargin(0.05)
	p4.SetNumber(1)
	canPost1DProj.cd();
	p4.SetLogy()
	p4.Draw();
	p4.cd()
	
	hpostfitNJets.Draw("hist")
	NJetsDataNew.Draw("pesame");
	NJetsPreFit.Draw('phistsame');
	leg4 = TLegend(0.55,0.6,0.9,0.87);
	leg4.SetFillStyle(0);
	leg4.SetBorderSize(0);
	leg4.SetTextSize(0.04); 
	leg4.AddEntry(NJetsDataNew,"Data", "pe")
	leg4.AddEntry(NJetsPreFit,"Pre-fit Total", "p")
	leg4.AddEntry(NJetsQCDPostFit,"QCD", "f")
	leg4.AddEntry(NJetsZPostFit,"Z#rightarrow#nu#bar{#nu}", "f")
	leg4.AddEntry(NJetsHTauPostFit,"Hadronic #tau ", "f")
	leg4.AddEntry(NJetsLostLPostFit,"Lost lepton", "f")
	leg4.Draw()
	p3 = TPad("p3","p3",0.0,0.00,1.0,0.3)
	p3.SetNumber(2)
	p3.SetTopMargin(0.05)
	p3.SetBottomMargin(0.30)	
	canPost1DProj.cd();
	p3.Draw(); p3.cd();
		
	PreFitNjets=NJetsPreFit.Clone("PreFitNjets");
	PostFitNJets=hpostfitNJets.GetStack().Last().Clone("PostFitNJets");
	PostFitNJets.Divide(PreFitNjets)
	PostFitNJets.SetMarkerStyle(kFullCircle)

	PostFitNJets.SetTitle(";N_{Jets}; N_{post}/N_{pre}")
	PostFitNJets.GetXaxis().SetTitleSize(0.15);
	PostFitNJets.GetYaxis().SetTitleSize(0.15);
	PostFitNJets.GetXaxis().SetTitleOffset(0.7);
	PostFitNJets.GetYaxis().SetTitleOffset(0.3);
	PostFitNJets.GetXaxis().SetLabelSize(0.1);
	PostFitNJets.GetYaxis().SetLabelSize(0.1);
	PostFitNJets.GetYaxis().SetRangeUser(0.75,1.25)
	PostFitNJets.Draw("phist")
	canPost1DProj.SaveAs("plotstacks/1DProjectionNJets.pdf")
	canPost1DProj.cd()
	p4.Draw(); p4.cd();
	hpostfitNBtags.Draw("hist")
	NBtagsDataNew.Draw("pesames")	
	NBtagsPreFit.Draw("phistsame")
	leg4.Draw();
	canPost1DProj.cd()	
	p3.Draw(); p3.cd();
		
	PreFitNBTags=NBtagsPreFit.Clone("PreFitNBTags");
	PostFitNBTags=hpostfitNBtags.GetStack().Last().Clone("PostFitNBTags");
	PostFitNBTags.Divide(PreFitNBTags)
	PostFitNBTags.SetMarkerStyle(kFullCircle)

	PostFitNBTags.SetTitle(";N_{BTags}; N_{post}/N_{pre}")
	PostFitNBTags.GetXaxis().SetTitleSize(0.15);
	PostFitNBTags.GetYaxis().SetTitleSize(0.15);
	PostFitNBTags.GetXaxis().SetTitleOffset(0.7);
	PostFitNBTags.GetYaxis().SetTitleOffset(0.3);
	PostFitNBTags.GetXaxis().SetLabelSize(0.1);
	PostFitNBTags.GetYaxis().SetLabelSize(0.1);
	PostFitNBTags.GetYaxis().SetRangeUser(0.75,1.25)
	PostFitNBTags.Draw("phist")
	canPost1DProj.SaveAs("plotstacks/1DProjectionNBTags.pdf")	

	canPost1DProj.cd()
	p4.Draw(); p4.cd();
	hpostfitMHT.Draw("hist")
	MHTDataNew.Draw("pesames")	
	MHTPreFit.Draw("phistsame")
	leg4.Draw();
	canPost1DProj.cd()
	p3.Draw(); p3.cd();
		
	PreFitMHT=MHTPreFit.Clone("PreFitNjets");
	PostFitMHT=hpostfitMHT.GetStack().Last().Clone("PostFitMHT");
	PostFitMHT.Divide(PreFitMHT)
	PostFitMHT.SetMarkerStyle(kFullCircle)

	PostFitMHT.SetTitle(";Missing H_{T}; N_{post}/N_{pre}")
	PostFitMHT.GetXaxis().SetTitleSize(0.15);
	PostFitMHT.GetYaxis().SetTitleSize(0.15);
	PostFitMHT.GetXaxis().SetTitleOffset(0.7);
	PostFitMHT.GetYaxis().SetTitleOffset(0.3);
	PostFitMHT.GetXaxis().SetLabelSize(0.1);
	PostFitMHT.GetYaxis().SetLabelSize(0.1);
	PostFitMHT.GetYaxis().SetRangeUser(0.75,1.25)
	PostFitMHT.Draw("phist")
	canPost1DProj.SaveAs("plotstacks/1DProjectionMHT.pdf")	
	canPost1DProj.cd()
	p4.Draw(); p4.cd();
	hpostfitHT.Draw("hist")
	HTDataNew.Draw("pesames")	
	HTPreFit.Draw("phistsame")
	leg4.Draw();
	canPost1DProj.cd()	
	p3.Draw(); p3.cd();
		
	PreFitHT=HTPreFit.Clone("PreFitNjets");
	PostFitHT=hpostfitHT.GetStack().Last().Clone("PostFitHT");
	PostFitHT.Divide(PreFitHT)
	PostFitHT.SetMarkerStyle(kFullCircle)

	PostFitHT.SetTitle(";H_{T}; N_{post}/N_{pre}")
	PostFitHT.GetXaxis().SetTitleSize(0.15);
	PostFitHT.GetYaxis().SetTitleSize(0.15);
	PostFitHT.GetXaxis().SetTitleOffset(0.7);
	PostFitHT.GetYaxis().SetTitleOffset(0.3);
	PostFitHT.GetXaxis().SetLabelSize(0.1);
	PostFitHT.GetYaxis().SetLabelSize(0.1);
	PostFitHT.GetYaxis().SetRangeUser(0.75,1.25)
	PostFitHT.Draw("phist")
	canPost1DProj.SaveAs("plotstacks/1DProjectionHT.pdf")	

