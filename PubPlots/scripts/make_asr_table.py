## make a compilable latex table with yields in 12 aggregate search regions

from __future__ import print_function
import os
import errno
from bg_est import BGEst
from data_obs import DataObs
from results_table import ResultsTable
from ROOT import TFile

def make_asr_table(output_file, lostlep, hadtau, znn, qcd, data_obs): #, 

    # define common cut labels
    njets_cuts = ['3+', '3+', '5+', '5+', '9+']*2 + ['7+', '5+']
    nbjets_cuts = ['0']*5 + ['2+', '1+', '3+', '2+', '3+', '1+', '1+']
    ht_cuts = ['500+', '1500+', '500+', '1500+', '1500+', '500+', '750+', '500+', '1500+', '750+', '300+', '750+']
    mht_cuts = ['500+', '750+', '500+', '750+', '750+', '500+', '750+', '500+', '750+', '750+', '300+', '750+']

            
    with open("/".join(["output", output_file+".tex"]), 'w') as fout:
        ## copy preamble already saved in output directory
        with open('output/reference/preamble.tex', 'r') as fpre:
            preamble = fpre.read()

        fout.write(preamble)
        ## get table and write it
        table = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, mht_cuts, ht_cuts, njets_cuts, nbjets_cuts, 1, 12, \
                              "Observed number of events and pre-fit background predictions in the aggregate search regions.", "tab:pre-fit-results-asrs")
        fout.write(table.full+"\n")

        fout.write("\\end{document}\n")
        
if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    output_file = sys.argv[1]
    f_lostlep = TFile.Open(sys.argv[2])
    lostlep = BGEst(f_lostlep.Get("ASR/hCV"), f_lostlep.Get("ASR/hStatUp"), f_lostlep.Get("ASR/hStatDown"), f_lostlep.Get("ASR/hSystUp"), f_lostlep.Get("ASR/hSystDown"))
    f_hadtau = TFile.Open(sys.argv[3])
    hadtau = BGEst(f_hadtau.Get("ASR/hCV"), f_hadtau.Get("ASR/hStatUp"), f_hadtau.Get("ASR/hStatDown"), f_hadtau.Get("ASR/hSystUp"), f_hadtau.Get("ASR/hSystDown"))
    f_znn = TFile.Open(sys.argv[4])
    znn = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"))
    f_qcd = TFile.Open(sys.argv[5])
    qcd = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"))
    f_data_obs = TFile.Open(sys.argv[6])
    data_obs = DataObs(f_data_obs.Get("ASR/hCV"))

    make_asr_table(output_file, lostlep, hadtau, znn, qcd, data_obs) # , sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]  
