#!/usr/bin/python
## stores properties of bin, including links to possibly-correlated bins
from __future__ import division

njets_cuts = ['2', '3-4', '5-6', '7-8', '9+']
nbjets_cuts = ['0', '1', '2', '3+']
mht_cuts = ['300-350', '350-500', '500-750', '750+']
ht_cuts = ['300-500', '500-1000', '1000+', '350-500', '500-1000', '1000+', '500-1000', '1000+', '750-1500', '1500+']

class SearchBin:

    def __init__(self, binnum):
        self.set_vars(binnum)
        
    def set_vars(self, binnum):
        self.num = binnum
        self.inj = self.GetINJ()
        self.inb = self.GetINB()
        self.ihtmht = self.GetIHTMHT()
        self.imht = self.GetIMHT()
        self.iht = self.GetIHT()
        self.nj_s = njets_cuts[self.inj]
        self.nb_s = njets_cuts[self.inb]
        self.mht_s = mht_cuts[self.imht]
        self.ht_s = ht_cuts[self.ihtmht]
        
    def GetINJ(self):
        if self.num > 141:
            return 4
        elif self.num > 109:
            return 3
        elif self.num > 69:
            return 2
        elif self.num > 29:
            return 1
        else:
            return 0

    def GetINB(self):
        INJ = self.GetINJ()
        if INJ==0:
            return self.num // 10
        elif INJ < 3:
            return (self.num - 30 - 40*(INJ-1)) // 10
        else:
            return (self.num - 110-32*(INJ-3)) // 8
    ## note: at high njets, where we drop HTMHT bins 0 and 3, the other HTMHT bins will keep the same HTMHT indices
    def GetIHTMHT(self):
        INJ = self.GetINJ()
        INB = self.GetINB()
        if INJ < 3:
            return self.num % 10
        else:
            offset = (self.num - 30 - 40*(INJ-1)) % 8
            if offset<2:
                return offset+1
            else:
                return offset+2
    
    def GetIMHT(self):
        IHTMHT = self.GetIHTMHT()
        if IHTMHT < 3:
            return 0
        elif IHTMHT < 6:
            return 1
        elif IHTMHT < 8:
            return 2
        else:
            return 3
    
    def GetIHT(self):
        IHTMHT = self.GetIHTMHT()
        if IHTMHT == 0 or IHTMHT == 3: # 300 < HT < 500
            return 0
        elif IHTMHT == 1 or IHTMHT == 4 or IHTMHT == 6 or IHTMHT == 8: # 500 < HT < 1000 (750-1500)
            return 1
        else: # > 1000 (1500)
            return 2
            ## note: we're putting HTMHT Box 9 (MHT>750, 750<HT<1500) in the same HT range as the bins with 500 < HT < 1000
            ## we're also putting HTMHT Box 10 (MHT>750, HT>1500) in the same HT range as the bins with HT > 1000      
        

    def Print(self):
        print("Search bin %d: INJ/INB/IMHT/IHT = %d / %d / %d / %d" % (self.num+1, self.inj, self.inb, self.imht, self.iht) )
    
