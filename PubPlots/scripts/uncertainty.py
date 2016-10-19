#!/usr/bin/python
## stores properties of bin, including links to possibly-correlated bins
## input is histogram of the uncertainty in all search bins (e.g. 160), string describing correlation structure
from __future__ import division
from search_bin import SearchBin
from ROOT import TH1D
from math import sqrt
from array import array

class Uncertainty:

    def __init__(self, hist, corrs=""):
        self.set_vars(hist, corrs)
        
    def set_vars(self, hist, corrs):
        self.hist = hist
        self.corrs = []
        self.AddCorrelations(corrs)
        
    def AddCorrelations(self, corr_in): ## string-based for now, can list multiple correlations, separated by :
        corr_list = corr_in.split(":")
        for corr in corr_list:
            self.corrs.append(corr)

    def AggregateBins(self, agg_bins, xaxis_title=None, xaxis_binning=None): # creates the new histogram with aggregated bins
        ## can define the x-axis here if you want
        if xaxis_title != None and xaxis_binning!=None:
            hagg = TH1D(self.hist.GetName(), ";"+xaxis_title, len(xaxis_binning)-1, array('d', xaxis_binning))
        else:
            hagg = TH1D(self.hist.GetName(), self.hist.GetTitle(), len(agg_bins), 0.5, float(len(agg_bins))+0.5)
        for iasr in range(len(agg_bins)):
            done = [False] * len(agg_bins[iasr]) # this will check to see if we've already added an uncertainty
            err = 0.
            for isub in range(len(agg_bins[iasr])):
                if done[isub]: # if we've already counted this one, skip it
                    continue
                if self.hist.GetBinContent(agg_bins[iasr][isub]) < 0.:  # no uncertainty, skip it
                    done[isub] = True
                    continue
                ibin = SearchBin(agg_bins[iasr][isub])
                corr_part = self.hist.GetBinContent(ibin.num) # we'll separately sum groups of uncertainties that are correlated, then add them in quadrature with the uncorrelated ones
                #print("Adding ibin %d: %f" % (ibin.num, corr_part))
                done[isub] = True
                for jsub in range(len(agg_bins[iasr])):
                    if isub == jsub or done[jsub]:
                        continue
                    if self.hist.GetBinContent(agg_bins[iasr][jsub]) < 0.:  # no uncertainty, skip it
                        done[jsub] = True
                        continue
                    jbin = SearchBin(agg_bins[iasr][jsub])
                    # now we'll linearly add an uncertainty from jbin if it should be correlated with the uncertainty from ibin
                    # here's where you define a correlation model -- give it a name and an condition to satisfy between bins i and j
                    # ex 1: 'all' -- this means all bins are correlated, so all systematics should be added linearly
                    # ex 2: 'DYsysPur' -- the purity of the dilepton sample has one value for nbjets = 1 and another for nbjets > 1 -- so
                    # uncertainties between two bins with the same nbjets (or both with >= 2) will be correlated, added linearly 
                    if 'all' in self.corrs \
                      or ('njets' in self.corrs and 'nbjets' not in self.corrs and jbin.inb == ibin.inb and jbin.ihtmht == ibin.ihtmht) \
                      or ('nbjets' in self.corrs  and 'njets' not in self.corrs and jbin.inj == ibin.inj and jbin.ihtmht == ibin.ihtmht) \
                      or ('njets' in self.corrs and 'nbjets' in self.corrs and jbin.ihtmht == ibin.ihtmht) \
                      or ('htmht' in self.corrs and 'nbjets' not in self.corrs and jbin.inb == ibin.inb and jbin.inj == ibin.inj) \
                      or ('htmht' in self.corrs and 'nbjets' in self.corrs and jbin.inj == ibin.inj) \
                      or ('DYsysPur' in self.corrs and ((ibin.inb == 1 and jbin.inb == 1) or (ibin.inb > 1 and jbin.inb > 1))) \
                      or ('LLAcc' in self.corrs and ibin.ihtmht == jbin.ihtmht and ibin.inj == jbin.inj and \
                          (ibin.inb + ibin.inj >=2) and (ibin.inb >= 2 or ibin.inj >= 2)):
                      #print("\t and adding correlated jbin %d: %f" % (jbin.num, self.hist.GetBinContent(jbin.num)))
                      corr_part += self.hist.GetBinContent(jbin.num)
                      done[jsub] = True
                      # end jsub loop
                err += corr_part**2
                # isub loop
            hagg.SetBinContent(iasr+1, sqrt(err))

        return Uncertainty(hagg)
