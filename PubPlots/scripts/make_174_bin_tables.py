from __future__ import print_function
import os
import errno
from bg_est import BGEst
from data_obs import DataObs
from results_table import ResultsTable
from ROOT import TFile

def make_174_bin_tables(output_file, lostlep, hadtau, znn, qcd, data_obs): #, 

    with open("/".join(["output", output_file+".tex"]), 'w') as fout:
        ## copy preamble already saved in output directory
        with open('output/reference/preamble.tex', 'r') as fpre:
            preamble = fpre.read()

        fout.write(preamble)
        ## now write Table 1 (2 jets)
        table0 = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, 1, 30, \
                              "Observed number of events and pre-fit background predictions in the $\\njets=2$ search bins.", "tab:pre-fit-results-nj0")
        fout.write(table0.full+"\n")
        ## and the other tables ...
        table1 = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, 31, 70, \
                              "Observed number of events and pre-fit background predictions in the $3\\leq\\njets\\leq4$ search bins.", "tab:pre-fit-results-nj1")
        fout.write(table1.full+"\n")
        table2 = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, 71, 110, \
                              "Observed number of events and pre-fit background predictions in the $5\\leq\\njets\\leq6$ search bins.", "tab:pre-fit-results-nj2")
        fout.write(table2.full+"\n")
        table3 = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, 111, 142, \
                              "Observed number of events and pre-fit background predictions in the $7\\leq\\njets\\leq8$ search bins.", "tab:pre-fit-results-nj3")
        fout.write(table3.full+"\n")
        table4 = ResultsTable(data_obs, lostlep, hadtau, znn, qcd, 143, 174, \
                              "Observed number of events and pre-fit background predictions in the $\\njets\\geq9$ search bins.", "tab:pre-fit-results-nj4")
        fout.write(table4.full+"\n")

        fout.write("\\end{document}\n")
        
if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    output_file = sys.argv[1]
    f_lostlep = TFile.Open(sys.argv[2])
    lostlep = BGEst(f_lostlep.Get("hCV"), f_lostlep.Get("hStatUp"), f_lostlep.Get("hStatDown"), f_lostlep.Get("hSystUp"), f_lostlep.Get("hSystDown"))
    f_hadtau = TFile.Open(sys.argv[3])
    hadtau = BGEst(f_hadtau.Get("hCV"), f_hadtau.Get("hStatUp"), f_hadtau.Get("hStatDown"), f_hadtau.Get("hSystUp"), f_hadtau.Get("hSystDown"))
    f_znn = TFile.Open(sys.argv[4])
    znn = BGEst(f_znn.Get("hCV"), f_znn.Get("hStatUp"), f_znn.Get("hStatDown"), f_znn.Get("hSystUp"), f_znn.Get("hSystDown"))
    f_qcd = TFile.Open(sys.argv[5])
    qcd = BGEst(f_qcd.Get("hCV"), f_qcd.Get("hStatUp"), f_qcd.Get("hStatDown"), f_qcd.Get("hSystUp"), f_qcd.Get("hSystDown"))
    f_data_obs = TFile.Open(sys.argv[6])
    data_obs = DataObs(f_data_obs.Get("data"))

    make_160_bin_tables(output_file, lostlep, hadtau, znn, qcd, data_obs) # , sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]  
