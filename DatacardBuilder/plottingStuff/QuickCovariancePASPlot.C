//
//  QuickPasPlot.c
//  
//
//  Created by Rishi Patel on 2/18/19.
//
//

#include <stdio.h>
#include "CMS_lumi.C");
void QuickPasPlot(){
    gStyle->SetOptStat(0);
    gStyle->SetOptTitle(0);
    TCanvas*c1=new TCanvas("c1","", 1200, 800);

    
    c1->Update();
			 
    TFile*fin=new TFile("RA2CorrelationMatrixFinal.root","READ");
    TH2D*Covariance=(TH2D*)fin->Get("RA2BinCovariance");
    Covariance->GetYaxis()->SetLabelSize(0.045);
    Covariance->GetYaxis()->SetLabelOffset(0.005);
    Covariance->GetXaxis()->SetLabelOffset(0.01);

    Covariance->GetXaxis()->SetLabelSize(0.045);

   // Covariance->GetYaxis()->SetTitleFont(42);
    Covariance->GetZaxis()->SetTitle("#sigma_{xy}");
    Covariance->GetZaxis()->SetTitleOffset(0.75);
    Covariance->GetZaxis()->SetTitleSize(0.05);
    Covariance->SetMinimum(0.001);
    Covariance->GetXaxis()->SetTitle("");
    Covariance->GetYaxis()->SetTitle("");

    Covariance->Draw("colz");
    c1->SetLogz();

    writeExtraText = true;       // if extra text
    
    extraText  = "Supplementary   arXiv:1908.04722";
    lumi_sqrtS = "137 fb^{-1} (13 TeV)";
    
    CMS_lumi( c1, 0, 1 );
    c1->Update();
    return;

    

    c1->Print("SupplementaryMaterialCovariancePlot.pdf");
    
   // TFile*fin=new TFile("FormattedCovarianceMatrices.root","READ");
    TH2D*Correlation=(TH2D*)fin->Get("RA2BinCorrelation");
    Correlation->GetYaxis()->SetLabelSize(0.045);
    Correlation->GetYaxis()->SetLabelOffset(0.005);
    Correlation->GetXaxis()->SetLabelOffset(0.01);
    
    Correlation->GetXaxis()->SetLabelSize(0.045);
    
    // Correlation->GetYaxis()->SetTitleFont(42);
    Correlation->GetZaxis()->SetTitle("#rho_{Correl}");
    Correlation->GetZaxis()->SetTitleOffset(0.75);
    Correlation->GetZaxis()->SetTitleSize(0.05);
    Correlation->GetXaxis()->SetTitle("");
    Correlation->GetYaxis()->SetTitle("");
    c1->SetLogz(0);

    Correlation->Draw("colz");
    writeExtraText = true;       // if extra text
    
    extraText  = "Supplementary arXiv:1908.04722";
    lumi_sqrtS = "137 fb^{-1} (13 TeV)";
    
    CMS_lumi( c1, 0, 1 );
    c1->Update();
    return;
 
    
    
    c1->Print("SupplementaryMaterialCorrelationPlot.pdf");
    
    //c1->Print("SupplementaryMaterialCorrelationPlot.pdf");

}
