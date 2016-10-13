#!/usr/bin/python
## stores properties of bin, including links to possibly-correlated bins
from __future__ import division


class SearchBin:

    def __init__(self, binnum):
        self.set_vars(binnum)
        
    def set_vars(cls, binnum):
        cls.num = binnum
        cls.inj = cls.GetINJ()
        cls.inb = cls.GetINB()
        cls.ihtmht = cls.GetIHTMHT()
        cls.imht = cls.GetIMHT()
        cls.iht = cls.GetIHT()
        ## these you can call as needed
        ## cls.same_njets = cls.GetBinsWithSameNJets()
        ## cls.same_nbjets = cls.GetBinsWithSameNBJets()
        ## cls.same_htmht = cls.GetBinsWithSameHTMHT()
        ## cls.same_mht = cls.GetBinsWithSameMHT()
        ## cls.same_ht = cls.GetBinsWithSameHT()
        
    def GetINJ(cls):
        INJ = (cls.num-1) // 40
        return INJ

    def GetINB(cls):
        INB = ((cls.num-1) % 40) // 10
        return INB

    def GetIHTMHT(cls):
        IHTMHT = ((cls.num-1) % 40) % 10
        return IHTMHT
    
    def GetIMHT(cls):
        if cls.ihtmht < 0:
            return -1
        elif cls.ihtmht < 3:
            return 0
        elif cls.ihtmht < 6:
            return 1
        elif cls.ihtmht < 8:
            return 2
        else:
            return 3
    
    def GetIHT(cls):
        if cls.ihtmht < 0:
            return -1
        elif cls.ihtmht == 0 or cls.ihtmht == 3: # 300 < HT < 500
            return 0
        elif cls.ihtmht == 1 or cls.ihtmht == 4 or cls.ihtmht == 6: # 500 < HT < 1000
            return 1
        else: 
            return 2 # note: we're putting HTMHT Box 9 (MHT>750, 750<HT<1500) in the same HT range as the bins with HT > 1000
                     # we're also pytting HTMHT Box 10 (MHT>750, HT>1500) in the same HT range as the bins with HT > 1000
    
    def GetBinsWithSameNJets(cls):
        same_njets = [bin for bin in range(1,161) if (bin-1) // 40 == cls.inj]
        return same_njets

    def GetBinsWithSameNBJets(cls):
        same_nbjets = [bin for bin in range(1,161) if ((bin-1) % 40) // 10 == cls.inb]
        return same_nbjets

    def GetBinsWithSameHTMHT(cls):
        same_htmht = [bin for bin in range(1,161) if ((bin-1) % 40) % 10 == cls.ihtmht]
        return same_htmht

    def GetBinsWithSameMHT(cls):
        same_mht = [bin for bin in range(1,161) if SearchBin(bin).imht == cls.imht]
        return same_mht

    def GetBinsWithSameHT(cls):
        same_ht = [bin for bin in range(1,161) if SearchBin(bin).iht == cls.iht]
        return same_ht

    @classmethod
    def GetBin(cls, mht, ht, njets, nbjets): # get event bin number from kinematic observables
        if mht < 300 or ht < 300 or njets < 3:
            return -1 ## not in any analysis bin

        # which interval in NJets ?
        # [3, 4]; [5,6]; [7,8] [9,inf)
        inj = 0
        if njets >= 5 and njets<=6:
            inj = 1
        elif njets >= 7 and njets<=8:
            inj = 2
        elif (njets>=9):
            inj = 3

        # which interval in mht?
        # [300, 350]; (350,500]; (500,750] (750,inf)
        imht = 0
        if mht > 350 and mht <= 500:
            imht = 1
        elif mht > 500 and mht <= 750:
            imht = 2
        elif mht > 750:
            imht = 3

        # which interval in htmht?
        ihtmht = 0
        if imht == 0:
            if ht > 300 and ht <= 500:
                ihtmht = 0
            elif ht > 500 and ht <= 1000:
                ihtmht = 1
            elif ht > 1000:
                ihtmht = 2
        elif imht == 1:
            if ht > 350 and ht <= 500:
                ihtmht = 3
            elif ht > 500 and ht <= 1000:
                ihtmht = 4
            elif ht > 1000:
                ihtmht = 5
            else:
                return -1 # throw away event if ht < mht
        elif imht == 2:
            if ht > 500 and ht <= 1000:
                ihtmht = 6
            elif ht > 1000:
                ihtmht = 7
            else:
                return -1 # throw away event if ht < mht
        elif imht == 3:
            if ht > 750 and ht <= 1500:
                ihtmht = 8
            elif ht > 1500:
                ihtmht = 9
            else:
                return -1 # throw away event if ht < mht
        else:
            return -1

        return cls(inj*40 + nbjets*10 + ihtmht + 1)
