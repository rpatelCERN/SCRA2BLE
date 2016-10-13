## creates an list of lines of latex that will produce a table with all BG predictions and observed data yields
## inputs also include lists of labels of cuts on each of the four search variables and (optional) a range of bins from which to extract results

from __future__ import print_function
import os
import errno
from ROOT import TH1D
from bg_est import BGEst
from data_obs import DataObs
from utils import GetPred

class ResultsTable:

    def __init__(self, data_obs, lostlep, hadtau, znn, qcd, mht_cuts, ht_cuts, njets_cuts, nbjets_cuts, first_bin=0, last_bin=None, caption=None, label=None):
        self.set_vars(data_obs, lostlep, hadtau, znn, qcd, mht_cuts, ht_cuts, njets_cuts, nbjets_cuts, first_bin, last_bin, caption, label)
        
    def set_vars(cls, data_obs, lostlep, hadtau, znn, qcd, mht_cuts, ht_cuts, njets_cuts, nbjets_cuts, first_bin, last_bin, caption, label):
        cls.caption = caption
        cls.label = label
        cls.data_obs = data_obs
        cls.lostlep = lostlep
        cls.hadtau = hadtau
        cls.znn = znn
        cls.qcd = qcd
        cls.header = cls.GetHeader()
        cls.trailer = cls.GetTrailer()
        cls.mht_cuts = mht_cuts
        cls.ht_cuts = ht_cuts
        cls.njets_cuts = njets_cuts
        cls.nbjets_cuts = nbjets_cuts
        cls.first_bin = first_bin
        if last_bin == None:
            cls.last_bin = cls.data_obs.hist.GetNbinsX()
        else:
            cls.last_bin = last_bin
        cls.last_bin = last_bin
        cls.contents = cls.GetContents()
        cls.full = cls.GetFormattedTable()
        #print("Bins: (%d, %d)" % (cls.first_bin, cls.last_bin))
        
    def GetHeader(cls):
        header = []
        header.append("\\begin{table}")
        header.append("\\renewcommand{\\arraystretch}{1.25}")
        header.append("\\centering")
        if cls.caption != None:
            header.append("\\caption{%s}" % cls.caption)
        if cls.label != None:
            header.append("\\label{%s}" % cls.label)
        header.append("\\resizebox{\\textwidth}{!}{")
        header.append("\\begin{tabular}{ |c|c|c|c|c||c|c|c|c||c|c| }")
        header.append("\\hline")
        header.append("Bin & $\\MHT$ [GeV] & $\\HT$ [GeV] & $\\njets$ & $\\nbjets$ & Lost-$e/\\mu$ & $\\tau\\rightarrow\\mathrm{had}$ & $Z\\rightarrow\\nu\\bar{\\nu}$ & QCD & Total Pred. & Obs. \\\\ \\hline")
        return header

    def GetTrailer(cls):
        trailer = []
        trailer.append("\\end{tabular}}")
        trailer.append("\\end{table}\n")
        return trailer

    def GetContents(cls):
        rows = []
        sumBG = BGEst.sumBG(cls.lostlep, cls.hadtau, cls.znn, cls.qcd)
        ilabel = 0 ## gets it's own index in case we're taking a subset of input histogram bins
        for ibin in range(cls.first_bin-1, cls.last_bin):
            line = []
            line.append(str(ibin+1))
            line.append(cls.mht_cuts[ilabel])
            line.append(cls.ht_cuts[ilabel])
            line.append(cls.njets_cuts[ilabel])
            line.append(cls.nbjets_cuts[ilabel])
            line.append(GetPred(cls.lostlep, ibin+1))
            line.append(GetPred(cls.hadtau, ibin+1))
            line.append(GetPred(cls.znn, ibin+1))
            line.append(GetPred(cls.qcd, ibin+1))
            line.append(GetPred(sumBG, ibin+1))
            line.append("%d \\\\ \\hline" % cls.data_obs.hist.GetBinContent(ibin+1))        
            rows.append(" & ".join(line))
            ilabel += 1

        return rows
        
    def GetFormattedTable(cls):
        return "\n".join(cls.header) + "\n" + "\n".join(cls.contents) + "\n" + "\n".join(cls.trailer)
