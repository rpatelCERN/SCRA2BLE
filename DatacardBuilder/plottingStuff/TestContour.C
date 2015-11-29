void TestContour(TString Model){
TFile*f0=new TFile(TString::Format("test%s.root",Model.Data()), "READ");
TCanvas* c = new TCanvas("c","Contour List",0,0,600,600);
//Make Level Contours to find limit:
TH2F*histExp=f0->Get("h2_MassScan");
TH2F*histExpSup=f0->Get("h2_MassScanSup");
TH2F*histExpSdn=f0->Get("h2_MassScanSdn");
TH2F*histObs=f0->Get("h2_MassScanObs");
TH2F*histObsSup=f0->Get("h2_MassScanObsSup");
TH2F*histObsSdn=f0->Get("h2_MassScanObsSdn");
TH2F*h2_MassScanXsec=f0->Get("h2_MassScanXsec");
Double_t contours[2]={0.0,1.0};
histExp->SetContour(2, contours);
histExpSup->SetContour(2, contours);
histExpSdn->SetContour(2, contours);
histObs->SetContour(2, contours);
histObsSup->SetContour(2, contours);
histObsSdn->SetContour(2, contours);

histExp->Draw("CONT Z  List");
c->Update();
 
TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   TList* contLevel = conts->At(0);
   TGraph* curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   Double_t*mLSP=curv->GetY();
   Double_t*mGo=curv->GetX();
   TGraph* ExpLim=new TGraph(curv->GetN());

  int fill=1;


   for(i=0; i<curv->GetN(); ++i){
	std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1100)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ExpLim->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ExpLim->Set(fill-1);
	ExpLim->Draw("ACP");
histExpSup->Draw("CONT Z  List");
c->Update();
 
   conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   contLevel = (TList*)conts->At(0);
   curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   mLSP=curv->GetY();
   mGo=curv->GetX();
   TGraph*ExpLimSup=new TGraph(curv->GetN());
   fill=1;
   for(i=0; i<curv->GetN(); ++i){
	//std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1100)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ExpLimSup->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ExpLimSup->Set(fill-1);
	ExpLimSup->Draw("ACP");
histExpSdn->Draw("CONT Z  List");
c->Update();
 
   conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   contLevel = (TList*)conts->At(0);
   curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   mLSP=curv->GetY();
   mGo=curv->GetX();
   TGraph*ExpLimSdn=new TGraph(curv->GetN());
   fill=1;
   for(i=0; i<curv->GetN(); ++i){
	//std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1200)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ExpLimSdn->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ExpLimSdn->Set(fill-1);
	ExpLimSdn->Draw("ACP");


histObs->Draw("CONT Z  List");
c->Update();
 
   conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   contLevel = (TList*)conts->At(0);
   curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   mLSP=curv->GetY();
   mGo=curv->GetX();
   TGraph*ObsLim=new TGraph(curv->GetN());
   fill=1;
   for(i=0; i<curv->GetN(); ++i){
	//std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1100)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ObsLim->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ObsLim->Set(fill-1);
	ObsLim->Draw("ACP");

histObsSup->Draw("CONT Z  List");
c->Update();
 
   conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   contLevel = (TList*)conts->At(0);
   curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   mLSP=curv->GetY();
   mGo=curv->GetX();
   TGraph*ObsLimSup=new TGraph(curv->GetN());
   fill=1;
   for(i=0; i<curv->GetN(); ++i){
	//std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1100)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ObsLimSup->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ObsLimSup->Set(fill-1);
	ObsLimSup->Draw("ACP");

histObsSdn->Draw("CONT Z  List");
c->Update();
 
   conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   contLevel = (TList*)conts->At(0);
   curv     = (TGraph*)contLevel->First();;
//Clean out the contour due to white space
   mLSP=curv->GetY();
   mGo=curv->GetX();
   TGraph*ObsLimSdn=new TGraph(curv->GetN());
   fill=1;
   for(i=0; i<curv->GetN(); ++i){
	//std::cout<<mLSP[i]<<", "<<mGo[i]<<", "<<mGo[i]-mLSP[i]<<std::endl;
	if(mLSP[i]>1100)continue;
	if(mGo[i]-mLSP[i]<=25)continue;
	ObsLimSdn->SetPoint(i, mGo[i], mLSP[i]);
	++fill;
   }
	ObsLimSdn->Set(fill-1);
	ObsLimSdn->Draw("ACP");
TFile*f1=new TFile(TString::Format("MassScan%s.root",Model.Data()), "RECREATE");
ExpLim->SetName("ExpLim");
ExpLimSup->SetName("ExpLimSup");
ExpLimSdn->SetName("ExpLimSdn");
ObsLim->SetName("ObsLim");
ObsLimSup->SetName("ObsLimSup");
ObsLimSdn->SetName("ObsLimSdn");

ExpLim->Write();
ExpLimSup->Write();
ExpLimSdn->Write();
ObsLim->Write();
ObsLimSup->Write();
ObsLimSdn->Write();
h2_MassScanXsec->Write();
}
