import sys
import ROOT as rt
rt.gROOT.SetBatch(True)    

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return " ".join(tmpLINE[1:])

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            x = rootFileIn.Get(tmpLINE[2])
            x.SetDirectory(0)
            return {'histogram': x}
            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {
		    'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'minus': rootFileIn.Get(tmpLINE[4]),
                    'plus2sigma': rootFileIn.Get(tmpLINE[5]),
                    'minus2sigma': rootFileIn.Get(tmpLINE[6]),
		    'nominal2': rootFileIn.Get(tmpLINE[7]),
                    'plus2': rootFileIn.Get(tmpLINE[8]),
                    'minus2': rootFileIn.Get(tmpLINE[9]),
                    'plus2sigma2': rootFileIn.Get(tmpLINE[10]),
                    'minus2sigma2': rootFileIn.Get(tmpLINE[11]),
                    'colorLine': tmpLINE[12],
                    'colorArea': tmpLINE[13]}

    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {
		    'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'minus': rootFileIn.Get(tmpLINE[4]),
		    'nominal2': rootFileIn.Get(tmpLINE[5]),
                    'plus2': rootFileIn.Get(tmpLINE[6]),
                    'minus2': rootFileIn.Get(tmpLINE[7]),
                    'colorLine': tmpLINE[8],
                    'colorArea': tmpLINE[9]}

