## defines all aggregate signal regions, stores sets of them in a dictionary
from search_bin import SearchBin
from ROOT import TH1D
from math import sqrt
from bin_navigation import *

## here define aggregate regions as lists of the bin indices  
asr1 = [i for i in range(160) if SearchBin(i).inb == 0 and SearchBin(i).imht > 1]
asr2 = [i for i in range(160) if SearchBin(i).inb == 0 and SearchBin(i).ihtmht == 9]
asr3 = [i for i in range(160) if SearchBin(i).inb == 0 and SearchBin(i).imht > 1 and SearchBin(i).inj > 1]
asr4 = [i for i in range(160) if SearchBin(i).inb == 0 and SearchBin(i).ihtmht == 9 and SearchBin(i).inj > 1]
asr5 = [149]
asr6 = [i for i in range(160) if SearchBin(i).inb >= 2 and SearchBin(i).imht > 1]
asr7 = [i for i in range(160) if SearchBin(i).inb >= 1 and SearchBin(i).imht > 2]
asr8 = [i for i in range(160) if SearchBin(i).inb == 3 and SearchBin(i).imht > 1 and SearchBin(i).inj >= 2]
asr9 = [i for i in range(160) if SearchBin(i).inb >= 2 and SearchBin(i).ihtmht == 9 and SearchBin(i).inj >= 2]
asr10 = [172, 173]
asr11 = [i for i in range(160) if SearchBin(i).inb >= 1 and SearchBin(i).inj >= 3]
asr12 = [i for i in range(160) if SearchBin(i).inb >= 1 and SearchBin(i).imht > 2 and SearchBin(i).inj >= 2]


## Each histogram of aggregrate bins shouls be added to this dictionary with a name (e.g. 'ASR' for the 12 standard aggregate regions) and a tuple of the aggregate regions defined above. This will be turned into a histogram with one bin per aggregate region, in the order specified in the tuple. You should also specify the x-axis title and visual binning
asr_sets = {'ASR': [asr1, asr2, asr3, asr4, asr5, asr6, asr7, asr8, asr9, asr10, asr11, asr12], \
            'NJ': GetNJetsBins(), \
            'NB': GetNBJetsBins(), \
            'MHT': GetMHTBins(), \
            'T1tttt': GetNJetsBins(minNB=2, minMHT=2, minHT=1), \
            'T1bbbb': GetNBJetsBins(minNJ=2, minMHT=2, minHT=2), \
            'T1qqqq' : GetMHTBins(minNJ=3, minNB=0, maxNB=0, minHT=2), \
            'T2tt' : GetNBJetsBins(minNJ=2, maxNJ=3, minMHT=2, minHT=1), \
            'T2bb' : GetMHTBins(minNJ=1, maxNJ=1, minNB=2, maxNB=2, minHT=1), \
            'T2qq': GetNJetsBins(minNB=0, maxNB=0, minMHT=3, minHT=2)
            }
    
asr_xtitle = {'ASR': 'Aggregate search region binning', \
            'NJ': 'N_{jet} (p_{T} > 30 GeV)', \
            'NB': 'N_{b-jet} (p_{T} > 30 GeV)', \
            'MHT': 'H_{T}^{miss} [GeV]', \
            'T1tttt': 'N_{jet} (p_{T} > 30 GeV)', \
            'T1bbbb': 'N_{b-jet} (p_{T} > 30 GeV)', \
            'T1qqqq' : 'H_{T}^{miss} [GeV]', \
            'T2tt' : 'N_{b-jet} (p_{T} > 30 GeV)', \
            'T2bb' : 'H_{T}^{miss} [GeV]', \
            'T2qq' : 'N_{jet} (p_{T} > 30 GeV)'}

asr_xbins = {'ASR': [i+0.5 for i in range(13)], \
            'NJ': [1.5, 2.5, 4.5, 6.5, 8.5, 12.5], \
            'NB': [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'MHT': [300., 350., 500., 750., 1050.], \
            'T1tttt': [1.5, 2.5, 4.5, 6.5, 8.5, 12.5], \
            'T1bbbb': [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'T1qqqq' : [300., 350., 500., 750., 1050.], \
            'T2tt' : [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'T2bb' : [300., 350., 500., 750., 1050.], \
            'T2qq' : [1.5, 2.5, 4.5, 6.5, 8.5, 12.5]}

def AddHistsInQuadrature(name, hists):
    hout = TH1D(name, "", hists[0].GetNbinsX(), hists[0].GetXaxis().GetXbins().GetArray())
    for ibin in range(hout.GetNbinsX()):
        total = 0.
        for ihist in hists:
            total += ihist.GetBinContent(ibin+1)**2
        hout.SetBinContent(ibin+1, sqrt(total))
    return hout
