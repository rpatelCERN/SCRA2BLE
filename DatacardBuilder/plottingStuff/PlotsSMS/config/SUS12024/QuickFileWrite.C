void QuickFileWrite(){
TFile*f1=new TFile("MassScanT1ttttSmooth.root");
TFile*f2=new TFile("MassScanT1bbbbSmooth.root");
TFile*f3=new TFile("MassScanT1qqqqSmooth.root");
TFile*f4=new TFile("MassScanT5qqqqVVSmooth.root");

TFile*f1_2=new TFile("../../../MassScanT1tttt.root");
TFile*f2_2=new TFile("../../../MassScanT1bbbb.root");
TFile*f3_2=new TFile("../../../MassScanT1qqqq.root");
TFile*f4_2=new TFile("../../../MassScanT5qqqqVV.root");

TFile*f5=new TFile("GluinoGluinoProdLimits.root", "RECREATE");
TGraph*ExpLim_T1tttt=(TGraph*)f1->Get("ExpLim");
TGraph*ObsLim_T1tttt=(TGraph*)f1->Get("ObsLim");
TGraph*ExpLimPlus_T1tttt=(TGraph*)f1->Get("ExpLimSdn");
TGraph*ObsLimPlus_T1tttt=(TGraph*)f1->Get("ObsLimSdn");
TGraph*ExpLimMinus_T1tttt=(TGraph*)f1->Get("ExpLimSup");
TGraph*ObsLimMinus_T1tttt=(TGraph*)f1->Get("ObsLimSup");
TH2D*T1tttt_MassScan2DObs=(TH2D*)f1_2->Get("MassScan2DObs");
TH2D*T1tttt_MassScan2DExp=(TH2D*)f1_2->Get("MassScan2DExp");

TGraph*ExpLim_T1bbbb=(TGraph*)f2->Get("ExpLim");
TGraph*ObsLim_T1bbbb=(TGraph*)f2->Get("ObsLim");
TGraph*ExpLimPlus_T1bbbb=(TGraph*)f2->Get("ExpLimSdn");
TGraph*ObsLimPlus_T1bbbb=(TGraph*)f2->Get("ObsLimSdn");
TGraph*ExpLimMinus_T1bbbb=(TGraph*)f2->Get("ExpLimSup");
TGraph*ObsLimMinus_T1bbbb=(TGraph*)f2->Get("ObsLimSup");
TH2D*T1bbbb_MassScan2DObs=(TH2D*)f2_2->Get("MassScan2DObs");
TH2D*T1bbbb_MassScan2DExp=(TH2D*)f2_2->Get("MassScan2DExp");

TGraph*ExpLim_T1qqqq=(TGraph*)f3->Get("ExpLim");
TGraph*ObsLim_T1qqqq=(TGraph*)f3->Get("ObsLim");
TGraph*ExpLimPlus_T1qqqq=(TGraph*)f3->Get("ExpLimSdn");
TGraph*ObsLimPlus_T1qqqq=(TGraph*)f3->Get("ObsLimSdn");
TGraph*ExpLimMinus_T1qqqq=(TGraph*)f3->Get("ExpLimSup");
TGraph*ObsLimMinus_T1qqqq=(TGraph*)f3->Get("ObsLimSup");
TH2D*T1qqqq_MassScan2DObs=(TH2D*)f3_2->Get("MassScan2DObs");
TH2D*T1qqqq_MassScan2DExp=(TH2D*)f3_2->Get("MassScan2DExp");

TGraph*ExpLim_T5qqqqVV=(TGraph*)f4->Get("ExpLim");
TGraph*ObsLim_T5qqqqVV=(TGraph*)f4->Get("ObsLim");
TGraph*ExpLimPlus_T5qqqqVV=(TGraph*)f4->Get("ExpLimSdn");
TGraph*ObsLimPlus_T5qqqqVV=(TGraph*)f4->Get("ObsLimSdn");
TGraph*ExpLimMinus_T5qqqqVV=(TGraph*)f4->Get("ExpLimSup");
TGraph*ObsLimMinus_T5qqqqVV=(TGraph*)f4->Get("ObsLimSup");
TH2D*T5qqqqVV_MassScan2DObs=(TH2D*)f4_2->Get("MassScan2DObs");
TH2D*T5qqqqVV_MassScan2DExp=(TH2D*)f4_2->Get("MassScan2DExp");



f5->cd();
ExpLim_T1tttt->Write("ExpLim_T1tttt");
ObsLim_T1tttt->Write("ObsLim_T1tttt");
ExpLimPlus_T1tttt->Write("ExpLimPlus_T1tttt");
ObsLimPlus_T1tttt->Write("ObsLimPlus_T1tttt");
ExpLimMinus_T1tttt->Write("ExpLimMinus_T1tttt");
ObsLimMinus_T1tttt->Write("ObsLimMinus_T1tttt");
T1tttt_MassScan2DObs->Write("T1tttt_MassScan2DObs");
T1tttt_MassScan2DExp->Write("T1tttt_MassScan2DExp");

ExpLim_T1bbbb->Write("ExpLim_T1bbbb");
ObsLim_T1bbbb->Write("ObsLim_T1bbbb");
ExpLimPlus_T1bbbb->Write("ExpLimPlus_T1bbbb");
ObsLimPlus_T1bbbb->Write("ObsLimPlus_T1bbbb");
ExpLimMinus_T1bbbb->Write("ExpLimMinus_T1bbbb");
ObsLimMinus_T1bbbb->Write("ObsLimMinus_T1bbbb");
T1bbbb_MassScan2DObs->Write("T1bbbb_MassScan2DObs");
T1bbbb_MassScan2DExp->Write("T1bbbb_MassScan2DExp");

ExpLim_T1qqqq->Write("ExpLim_T1qqqq");
ObsLim_T1qqqq->Write("ObsLim_T1qqqq");
ExpLimPlus_T1qqqq->Write("ExpLimPlus_T1qqqq");
ObsLimPlus_T1qqqq->Write("ObsLimPlus_T1qqqq");
ExpLimMinus_T1qqqq->Write("ExpLimMinus_T1qqqq");
ObsLimMinus_T1qqqq->Write("ObsLimMinus_T1qqqq");
T1qqqq_MassScan2DObs->Write("T1qqqq_MassScan2DObs");
T1qqqq_MassScan2DExp->Write("T1qqqq_MassScan2DExp");

ExpLim_T5qqqqVV->Write("ExpLim_T5qqqqVV");
ObsLim_T5qqqqVV->Write("ObsLim_T5qqqqVV");
ExpLimPlus_T5qqqqVV->Write("ExpLimPlus_T5qqqqVV");
ObsLimPlus_T5qqqqVV->Write("ObsLimPlus_T5qqqqVV");
ExpLimMinus_T5qqqqVV->Write("ExpLimMinus_T5qqqqVV");
ObsLimMinus_T5qqqqVV->Write("ObsLimMinus_T5qqqqVV");
T5qqqqVV_MassScan2DObs->Write("T5qqqqVV_MassScan2DObs");
T5qqqqVV_MassScan2DExp->Write("T5qqqqVV_MassScan2DExp");

f5->Close();
}
