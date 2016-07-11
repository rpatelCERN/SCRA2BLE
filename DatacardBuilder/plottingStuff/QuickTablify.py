#from ROOT import *
import ROOT
import sys
def ExtractFile(iname):
	f = ROOT.TFile(iname);
	t = f.Get("limit");
	Lim=[]
	
	t.GetEntry(2);
	Lim.append(t.limit)
	t.GetEntry(5);
	Lim.append(t.limit)
	return Lim

if __name__ == '__main__':
	idir="./"
	models=["SMSbbbb1500","SMSbbbb1000","SMStttt1500","SMStttt1200","SMSqqqq1400","SMSqqqq1000","SMStt850", "SMStt500","SMStt425" ]
	printModels=["T1bbbb(1500, 100)", "T1bbbb(1000, 800)", "T1tttt(1500, 100)", "T1tttt(1200, 800)", " T1qqqq(1400, 100)",  "T1qqqq(1000, 900)", "T2tt(850,100)", "T2tt(500,325)","T2tt(425,325)"]
	i=0
	mode=sys.argv[1]
	for m in models:
		ExpUL=ExtractFile(idir+"higgsCombinetestCards-%s-%s-2.6-mu0.0.Asymptotic.mH120.root" %(mode,m))[0]	
		ObsUL=ExtractFile(idir+"higgsCombinetestCards-%s-%s-2.6-mu0.0.Asymptotic.mH120.root" %(mode,m))[1]
		print "%s & %1.2f & %1.2f \\\\" %(printModels[i], ExpUL,ObsUL)
		i=i+1
