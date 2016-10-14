## defines all aggregate signal regions, stores sets of them in a dictionary
from search_bin import SearchBin
from ROOT import TH1D
from math import sqrt

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

asr_sets = {'ASR': (asr1, asr2, asr3, asr4, asr5, asr6, asr7, asr8, asr9, asr10, asr11, asr12), \
            'NJ': ([i for i in range(1,41)], [i for i in range(41,81)], [i for i in range(81,121)], [i for i in range(121,161)]), \
            'NB': ([i for i in range(1,161) if SearchBin(i).inb==0], [i for i in range(1,161) if SearchBin(i).inb==1], [i for i in range(1,161) if SearchBin(i).inb==2], [i for i in range(1,161) if SearchBin(i).inb==3]), \
            'MHT': ([i for i in range(1,161) if SearchBin(i).imht==0], [i for i in range(1,161) if SearchBin(i).imht==1], [i for i in range(1,161) if SearchBin(i).imht==2], [i for i in range(1,161) if SearchBin(i).imht==3]) \
            }     

def AddHistsInQuadrature(name, hists):
    hout = TH1D(name, "", hists[0].GetNbinsX(), 0.5, hists[0].GetNbinsX() + 0.5)
    for ibin in range(hout.GetNbinsX()):
        total = 0.
        for ihist in hists:
            total += ihist.GetBinContent(ibin+1)**2
        hout.SetBinContent(ibin+1, sqrt(total))
    return hout
