
#include <iostream>
#include <vector>
#include <math.h> 
#include "TROOT.h"
#include "TFile.h"
#include "TSystem.h"
#include "TChain.h"
#include "TTree.h"
#include "TCut.h"
#include "THStack.h"
#include "TLine.h"
#include "TH1.h"
#include "TH2.h"
#include "TFileCollection.h"
#include "TLorentzVector.h"
#include "TPaveText.h"
#include "TText.h"
#include "TGraphAsymmErrors.h"
// #include "Math/QuantFuncMathCore.h"
// #include "inc/jack_style.h"
// #include "inc/CMS_lumi.C"
// #include "asrs.h"

using namespace std;

double lumi = 35862.351;

void PrintSignalTables() {

  TH1::SetDefaultSumw2(1);
  //gROOT->SetBatch(1);


  TFile* fin = TFile::Open("signal_hists.root");

  TH1D* htttt_nc = (TH1D*) fin->Get("ASR/RA2bin_T1tttt_1500_100_fast_nominal");
  htttt_nc->Scale(lumi);
  TH1D* htttt_c = (TH1D*) fin->Get("ASR/RA2bin_T1tttt_1200_800_fast_nominal");
  htttt_c->Scale(lumi);
  TH1D* hbbbb_nc = (TH1D*) fin->Get("ASR/RA2bin_T1bbbb_1500_100_fast_nominal");
  hbbbb_nc->Scale(lumi);
  TH1D* hbbbb_c = (TH1D*) fin->Get("ASR/RA2bin_T1bbbb_1000_900_fast_nominal");
  hbbbb_c->Scale(lumi);
  TH1D* hqqqq_nc = (TH1D*) fin->Get("ASR/RA2bin_T1qqqq_1400_100_fast_nominal");
  hqqqq_nc->Scale(lumi);
  TH1D* hqqqq_c = (TH1D*) fin->Get("ASR/RA2bin_T1qqqq_1000_800_fast_nominal");
  hqqqq_c->Scale(lumi);

  TH1D* hqqqqVV_nc = (TH1D*) fin->Get("ASR/RA2bin_T5qqqqVV_1400_100_fast_nominal");
  hqqqqVV_nc->Scale(lumi);
  TH1D* hqqqqVV_c = (TH1D*) fin->Get("ASR/RA2bin_T5qqqqVV_1000_800_fast_nominal");
  hqqqqVV_c->Scale(lumi);
  TH1D* htbtb_nc = (TH1D*) fin->Get("ASR/RA2bin_T1tbtb_1500_100_fast_nominal");
  htbtb_nc->Scale(lumi);
  TH1D* htbtb_c = (TH1D*) fin->Get("ASR/RA2bin_T1tbtb_1100_700_fast_nominal");
  htbtb_c->Scale(lumi);

  TH1D* htt_nc = (TH1D*) fin->Get("ASR/RA2bin_T2tt_700_50_fast_nominal");
  htt_nc->Scale(lumi);
  TH1D* htt_c = (TH1D*) fin->Get("ASR/RA2bin_T2tt_300_200_fast_nominal");
  htt_c->Scale(lumi);
  TH1D* hbb_nc = (TH1D*) fin->Get("ASR/RA2bin_T2bb_650_1_fast_nominal");
  hbb_nc->Scale(lumi);
  TH1D* hbb_c = (TH1D*) fin->Get("ASR/RA2bin_T2bb_500_300_fast_nominal");
  hbb_c->Scale(lumi);
  TH1D* hqq_nc = (TH1D*) fin->Get("ASR/RA2bin_T2qq_1000_100_fast_nominal");
  hqq_nc->Scale(0.8*lumi);
  TH1D* hqq_c = (TH1D*) fin->Get("ASR/RA2bin_T2qq_700_400_fast_nominal");
  hqq_c->Scale(0.8*lumi);
  
  for (unsigned int bin(0); bin<12; bin++) {
    printf("& $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$  \\\\ \\hline\n", 
	   hbbbb_nc->GetBinContent(bin+1), hbbbb_nc->GetBinError(bin+1),
	   htttt_nc->GetBinContent(bin+1), htttt_nc->GetBinError(bin+1),
	   hqqqq_nc->GetBinContent(bin+1), hqqqq_nc->GetBinError(bin+1)
	   );
  }

  cout << endl << "***********" << endl << endl;
  for (unsigned int bin(0); bin<12; bin++) {
    printf("& $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$  \\\\ \\hline\n", 
	   hbbbb_c->GetBinContent(bin+1), hbbbb_c->GetBinError(bin+1),
	   htttt_c->GetBinContent(bin+1), htttt_c->GetBinError(bin+1),
	   hqqqq_c->GetBinContent(bin+1), hqqqq_c->GetBinError(bin+1)
	   );
  }

  cout << endl << "***********" << endl << endl;
  for (unsigned int bin(0); bin<12; bin++) {
    printf("& $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$  \\\\ \\hline\n", 
	   htbtb_nc->GetBinContent(bin+1), htbtb_nc->GetBinError(bin+1),
	   hqqqqVV_nc->GetBinContent(bin+1), hqqqqVV_nc->GetBinError(bin+1),
	   htbtb_c->GetBinContent(bin+1), htbtb_c->GetBinError(bin+1),
	   hqqqqVV_c->GetBinContent(bin+1), hqqqqVV_c->GetBinError(bin+1)
	   );
  }
  
  cout << endl << "***********" << endl << endl;
  for (unsigned int bin(0); bin<12; bin++) {
    printf("& $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ \\\\ \\hline\n", 
	   hbb_nc->GetBinContent(bin+1), hbb_nc->GetBinError(bin+1),
	   htt_nc->GetBinContent(bin+1), htt_nc->GetBinError(bin+1),
	   hqq_nc->GetBinContent(bin+1), hqq_nc->GetBinError(bin+1)
	   );
  }

  cout << endl << "***********" << endl << endl;
  for (unsigned int bin(0); bin<12; bin++) {
    printf("& $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ & $%3.2f \\pm %3.2f$ \\\\ \\hline\n", 
	   hbb_c->GetBinContent(bin+1), hbb_c->GetBinError(bin+1),
	   htt_c->GetBinContent(bin+1), htt_c->GetBinError(bin+1),
	   hqq_c->GetBinContent(bin+1), hqq_c->GetBinError(bin+1)
	   );
  }

  return;
  
}

