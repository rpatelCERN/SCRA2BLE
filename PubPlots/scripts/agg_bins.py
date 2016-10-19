## defines all aggregate signal regions, stores sets of them in a dictionary
from search_bin import SearchBin
from ROOT import TH1D
from math import sqrt

## here define aggregate regions as lists of the bin indices  
asr1 = [i for i in range(1,161) if SearchBin(i).inb == 0 and SearchBin(i).imht > 1]
asr2 = [i for i in range(1,161) if SearchBin(i).inb == 0 and SearchBin(i).ihtmht == 9]
asr3 = [i for i in range(1,161) if SearchBin(i).inb == 0 and SearchBin(i).imht > 1 and SearchBin(i).inj > 0]
asr4 = [i for i in range(1,161) if SearchBin(i).inb == 0 and SearchBin(i).ihtmht == 9 and SearchBin(i).inj > 0]
asr5 = [130]
asr6 = [i for i in range(1,161) if SearchBin(i).inb >= 2 and SearchBin(i).imht > 1]
asr7 = [i for i in range(1,161) if SearchBin(i).inb >= 1 and SearchBin(i).imht > 2]
asr8 = [i for i in range(1,161) if SearchBin(i).inb == 3 and SearchBin(i).imht > 1 and SearchBin(i).inj >= 1]
asr9 = [i for i in range(1,161) if SearchBin(i).inb >= 2 and SearchBin(i).ihtmht == 9 and SearchBin(i).inj >= 1]
asr10 = [159, 160]
asr11 = [i for i in range(1,161) if SearchBin(i).inb >= 1 and SearchBin(i).inj >= 2]
asr12 = [i for i in range(1,161) if SearchBin(i).inb >= 1 and SearchBin(i).imht > 2 and SearchBin(i).inj >= 1]


## Each histogram of aggregrate bins shouls be added to this dictionary with a name (e.g. 'ASR' for the 12 standard aggregate regions) and a tuple of the aggregate regions defined above. This will be turned into a histogram with one bin per aggregate region, in the order specified in the tuple. You should also specify the x-axis title and visual binning
asr_sets = {'ASR': (asr1, asr2, asr3, asr4, asr5, asr6, asr7, asr8, asr9, asr10, asr11, asr12), \
            'NJ': ([i for i in range(1,41)], [i for i in range(41,81)], [i for i in range(81,121)], [i for i in range(121,161)]), \
            'NB': ([i for i in range(1,161) if SearchBin(i).inb==0], [i for i in range(1,161) if SearchBin(i).inb==1], [i for i in range(1,161) if SearchBin(i).inb==2], [i for i in range(1,161) if SearchBin(i).inb==3]), \
            'MHT': ([i for i in range(1,161) if SearchBin(i).imht==0], [i for i in range(1,161) if SearchBin(i).imht==1], [i for i in range(1,161) if SearchBin(i).imht==2], [i for i in range(1,161) if SearchBin(i).imht==3]), \
            'T1tttt': ([i for i in range(26,31)]+[i for i in range(36,41)], [i for i in range(66,71)]+[i for i in range(76,81)], [i for i in range(106,111)]+[i for i in range(116,121)], [i for i in range(146,151)]+[i for i in range(156,161)]), \
            'T1bbbb': ([48, 50, 88, 90, 128, 130], [58, 60, 98, 100, 138, 140], [68, 70, 108, 110, 148, 150], [78, 80, 118, 120, 158, 160]), \
            'T1qqqq' : ([43, 83, 123], [46, 86, 126], [48, 88, 128], [50, 90, 130]), \
            'T2tt' : ([47, 48, 49, 50, 87, 88, 89, 90], [57, 58, 59, 60, 97, 98, 99, 100], [67, 68, 69, 70, 107, 108, 109, 110], [77, 78, 79, 80, 117, 118, 119, 120]), \
            'T2bb' : ([22, 23], [25, 26], [27, 28], [29, 30]), \
            'T2qq': ([3, 43], [6, 46], [8, 48], [10, 50])
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
            'NJ': [2.5, 4.5, 6.5, 8.5, 12.5], \
            'NB': [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'MHT': [300., 350., 500., 750., 1050.], \
            'T1tttt': [2.5, 4.5, 6.5, 8.5, 12.5], \
            'T1bbbb': [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'T1qqqq' : [300., 350., 500., 750., 1050.], \
            'T2tt' : [-0.499, 0.5, 1.5, 2.5, 3.499], \
            'T2bb' : [300., 350., 500., 750., 1050.], \
            'T2qq' : [2.5, 4.5, 6.5, 8.5, 12.5]}

def AddHistsInQuadrature(name, hists):
    hout = TH1D(name, "", hists[0].GetNbinsX(), hists[0].GetXaxis().GetXbins().GetArray())
    for ibin in range(hout.GetNbinsX()):
        total = 0.
        for ihist in hists:
            total += ihist.GetBinContent(ibin+1)**2
        hout.SetBinContent(ibin+1, sqrt(total))
    return hout
