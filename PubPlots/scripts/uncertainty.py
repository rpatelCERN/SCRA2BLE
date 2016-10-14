#!/usr/bin/python
## stores properties of bin, including links to possibly-correlated bins
from __future__ import division
from search_bin import SearchBin
from ROOT import TH1D
from math import sqrt

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

    def AggregateBins(self, agg_bins): # creates the new histogram with aggregated bins
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
                    if 'all' in self.corrs \
                      or 'njets' in self.corrs and 'nbjets' not in self.corrs and jbin.inj == ibin.inj \
                      or 'nbjets' in self.corrs  and 'njets' not in self.corrs and jbin.inb == ibin.inb \
                      or 'njets' in self.corrs and 'nbjets' in self.corrs and jbin.inj == ibin.inj and jbin.inb == ibin.inb \
                      or 'htmht' in self.corrs and jbin.ihtmht == ibin.ihtmht:
                      #print("\t and adding jbin %d: %f" % (jbin.num, self.hist.GetBinContent(jbin.num)))
                      corr_part += self.hist.GetBinContent(jbin.num)
                      done[jsub] = True
                      # end jsub loop
                err += corr_part**2
                # isub loop
            hagg.SetBinContent(iasr+1, sqrt(err))

        return Uncertainty(hagg)
