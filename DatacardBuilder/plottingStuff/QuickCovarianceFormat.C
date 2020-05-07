void QuickCovarianceFormat(){
TFile*fin=new TFile("fitDiagnosticstestCards-Moriond-T2tt_1000_550-137.4-mu0.0.root", "READ");
TH2D*CombineCovariance=(TH2D*)fin->Get("shapes_prefit/overall_total_covar");
    TH2D*OrderedCovariance=(TH2D*)CombineCovariance->Clone("OrderedCovariance");
    TH2D*Correlation=(TH2D*)CombineCovariance->Clone("Correlation");

    for(int i=1; i<=174; ++i){
        for(int j=1; j<=174; ++j){
            int ArrayI=i;
            int ArrayJ=j;
             ArrayI=CombineCovariance->GetXaxis()->FindBin(TString::Format("ch%d_0", i).Data());
             ArrayJ=CombineCovariance->GetYaxis()->FindBin(TString::Format("ch%d_0",j).Data());
          //  std::cout<<"Bin i, j "<<ArrayI<<", "<<ArrayJ<<std::endl;
            //OrderedCovariance->SetBinContent(i,j, CombineCovariance->GetBinContent(ArrayI, ArrayJ));
            OrderedCovariance->GetXaxis()->SetBinLabel(i,TString::Format("ch%d", i).Data());
            OrderedCovariance->GetYaxis()->SetBinLabel(j,TString::Format("ch%d",j).Data());
            Correlation->GetXaxis()->SetBinLabel(i,TString::Format("ch%d", i).Data());
            Correlation->GetYaxis()->SetBinLabel(j,TString::Format("ch%d",j).Data());
            OrderedCovariance->SetBinContent(i,j, CombineCovariance->GetBinContent(ArrayI, ArrayJ));
            float covij=CombineCovariance->GetBinContent(ArrayI, ArrayJ);
            float covii=CombineCovariance->GetBinContent(ArrayI,ArrayI);
            float covjj=CombineCovariance->GetBinContent(ArrayJ,ArrayJ);
            
            //if(covii>0 && covjj>0)std::cout<<"Bin "<<i<<", "<<j<<" "<<covij/sqrt(covii*covjj)<<std::endl;;
            if(covii>0 && covjj>0)Correlation->SetBinContent(i, j, covij/sqrt(covii*covjj) );
            else Correlation->SetBinContent(i, j, 0);
	   
        }
    }
/*
   TH2D*OrderedCovarianceReorder=OrderedCovariance->Clone("OrderedCovarianceReorder");
	OrderedCovarianceReorder->Reset();
 */
    TFile*finCrossCheck=new TFile("PrefitUnc.root", "READ");
    
    TH1D*PrefitUnc=(TH1D*)finCrossCheck->Get("PrefitUnc");
    for(int i=1; i<=174; ++i){
        for(int j=1; j<=174; ++j){
            if(i!=j)continue;
		std::cout<<"X Label "<<OrderedCovariance->GetXaxis()->GetBinLabel(i)<<std::endl;
            std::cout<<"Prefit Unc Cov Matrix "<<sqrt(OrderedCovariance->GetBinContent(i,j))<< " Cross Check "<<PrefitUnc->GetBinContent(i)<<std::endl;
                std::cout<<"Prefit Unc Cov Matrix Ratio with Truth "<<sqrt(OrderedCovariance->GetBinContent(i,j))/PrefitUnc->GetBinContent(i)<<std::endl;
            //std::cout<<"Y Label "<<OrderedCovarianceReorder->GetYaxis()->GetBinLabel(j)<<std::endl;;
            OrderedCovariance->GetXaxis()->SetBinLabel(i,"");
            OrderedCovariance->GetYaxis()->SetBinLabel(j,"");
            Correlation->GetXaxis()->SetBinLabel(i,"");
            Correlation->GetYaxis()->SetBinLabel(j,"");
            if(i==1)OrderedCovariance->GetXaxis()->SetBinLabel(i,"N_{Jets} [2,3]");
            if(j==1)OrderedCovariance->GetYaxis()->SetBinLabel(i,"N_{Jets} [2,3]");
            
            if(i==31)OrderedCovariance->GetXaxis()->SetBinLabel(i,"N_{Jets} [4,5]");
            if(j==31)OrderedCovariance->GetYaxis()->SetBinLabel(i,"N_{Jets} [4,5]");
            
            if(i==71)OrderedCovariance->GetXaxis()->SetBinLabel(i,"N_{Jets} [6,7]");
            if(j==71)OrderedCovariance->GetYaxis()->SetBinLabel(i,"N_{Jets} [6,7]");
            
            if(i==111)OrderedCovariance->GetXaxis()->SetBinLabel(i,"N_{Jets} [8,9]");
            if(j==111)OrderedCovariance->GetYaxis()->SetBinLabel(i,"N_{Jets} [8,9]");
            
            if(i==143)OrderedCovariance->GetXaxis()->SetBinLabel(i,"N_{Jets} [10+]");
            if(j==143)OrderedCovariance->GetYaxis()->SetBinLabel(i,"N_{Jets} [10+]");
            
            if(i==1)Correlation->GetXaxis()->SetBinLabel(i,"N_{Jets} [2,3]");
            if(j==1)Correlation->GetYaxis()->SetBinLabel(i,"N_{Jets} [2,3]");
            
            if(i==31)Correlation->GetXaxis()->SetBinLabel(i,"N_{Jets} [4,5]");
            if(j==31)Correlation->GetYaxis()->SetBinLabel(i,"N_{Jets} [4,5]");
            
            if(i==71)Correlation->GetXaxis()->SetBinLabel(i,"N_{Jets} [6,7]");
            if(j==71)Correlation->GetYaxis()->SetBinLabel(i,"N_{Jets} [6,7]");
            
            if(i==111)Correlation->GetXaxis()->SetBinLabel(i,"N_{Jets} [8,9]");
            if(j==111)Correlation->GetYaxis()->SetBinLabel(i,"N_{Jets} [8,9]");
            
            if(i==143)Correlation->GetXaxis()->SetBinLabel(i,"N_{Jets} [10+]");
            if(j==143)Correlation->GetYaxis()->SetBinLabel(i,"N_{Jets} [10+]");

	}
    }
    
   // return;
    Correlation->Draw("colz");
    TFile*fout=new TFile("RA2CorrelationMatrixFinal.root", "RECREATE");
    OrderedCovariance->Write("RA2BinCovariance");
    Correlation->Write("RA2BinCorrelation");

    return;

}

