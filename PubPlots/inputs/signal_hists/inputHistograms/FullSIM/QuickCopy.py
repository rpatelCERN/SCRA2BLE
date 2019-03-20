from ROOT import *
import sys
fin=TFile("../fastsimSignal%s/RA2bin_proc_%s_%s_%s_fast.root" %(sys.argv[1],sys.argv[1], sys.argv[2], sys.argv[3]));
fout=TFile("RA2bin_proc_%s_%s_%s_MC2017.root" %(sys.argv[1], sys.argv[2], sys.argv[3]), "RECREATE");
RA2binCopy=fin.Get("RA2bin_%s_%s_%s_fast_nominal"%(sys.argv[1], sys.argv[2], sys.argv[3]));
RA2binCopy.SetName("RA2bin_%s_%s_%s_MC2017_nominal" %(sys.argv[1], sys.argv[2], sys.argv[3]))
RA2binCopy.Write("RA2bin_%s_%s_%s_MC2017_nominal"%(sys.argv[1], sys.argv[2], sys.argv[3]));

