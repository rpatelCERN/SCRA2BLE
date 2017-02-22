void QuickTreeCopy(){
TFile*fin=new TFile("/eos/uscms/store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV11/tree_signalUnblind/tree_JetHT_2016G.root", "READ");
TTree*originalTree=(TTree*)fin->Get("tree");
TFile*fout=new TFile("OutputDataEvents.root","RECREATE");
TTree*CopyTree=originalTree->CopyTree("MHT>300 && HT>300 && globalTightHalo2016Filter==1 && HBHENoiseFilter==1 && HBHEIsoNoiseFilter==1 && eeBadScFilter==1 && EcalDeadCellTriggerPrimitiveFilter==1 && BadChargedCandidateFilter && BadPFMuonFilter && NVtx > 0 && (TriggerPass[42]==1||TriggerPass[43]==1||TriggerPass[44]==1||TriggerPass[46]==1||TriggerPass[47]==1||TriggerPass[48]==1)");
fout->cd();
CopyTree->Write("tree");

}
