#! /usr/bin/env python
import os
import glob
import math
from array import array
import sys
import time

#import ROOT
from ROOT import *
############################################
#            Job steering                  #
############################################
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='use fastsim signal (default = %default)')
parser.add_option('--keeptar', action='store_true', dest='keeptar', default=False, help='keep old tarball for condor jobs (default = %default)')
parser.add_option("--outDir", dest="outDir", default = "/store/user/rgp230/SUSY/statInterp/scanOutput/Cards2016/FullSim",help="EOS output directory  (default = %default)", metavar="outDir")
(options, args) = parser.parse_args()

# -----------------------------------------------------------------
#Create CACHEDIR.TAG files on the fly to exclude output directories from condor tarball
# -----------------------------------------------------------------
def cachedir(DIR):
    if len(DIR)==0:
        return
        
    tagfile = DIR+"/CACHEDIR.TAG"
    if not os.path.isfile(tagfile):
        tag = open(tagfile,'w')
        tag.write("Signature: 8a477f597d28d172789f06886806bc55\n")
        tag.write("# This file is a cache directory tag.\n")
        tag.write("# For information about cache directory tags, see:\n")
        tag.write("#       http://www.brynosaurus.com/cachedir/")
        tag.close()

def condorize(command,tag,odir,CMSSWVER):

    print "--------------------"
    print "Launching phase space point:",tag

    #change to a tmp dir
#    os.chdir("tmp");
    #startdir = os.getcwd();
    f1n = "tmp_%s.sh" %(tag);
    f1=open(f1n, 'w')
    f1.write("#!/bin/sh \n");

    # setup environment
    #f1.write("cd ${_CONDOR_SCRATCH_DIR} \n");
    #f1.write("tar -xzf %s.tar.gz \n" % (CMSSWVER));
    #f1.write("scram b ProjectRename \n");
    #f1.write("source /cvmfs/cms.cern.ch/cmsset_default.sh \n");
    f1.write("#SBATCH -J CombineCLT_%s\n" %(tag))
    f1.write("#SBATCH -p background-4g\n")
    f1.write("#SBATCH --time=03:30:00\n")
    f1.write("#SBATCH --mem-per-cpu=8000 \n")
    f1.write("#SBATCH -o CombineCLT_%s.out \n" %(tag))
    f1.write("#SBATCH -e CombineCLT_%s.err \n" %(tag))
    #f1.write("set SCRAM_ARCH=slc6_amd64_gcc481\n"
    #f1.write("cd ${_CONDOR_SCRATCH_DIR} \n")
    f1.write("cd /fdata/hepx/store/user/rish/CombineCards/gitPushApproval/%s \n" % (CMSSWVER));
    f1.write("cd src/SCRA2BLE/DatacardBuilder/ \n");
    f1.write("eval `scramv1 runtime -sh`\n")

    f1.write("ls \n");
    f1.write(command+" \n") 
    #for mu in range(0,6):
    #	f1.write("xrdcp -f results_%s_mu%1.1f.root root://cmseos.fnal.gov/%s/results_%s_mu%1.1f.root 2>&1 \n" % (tag,float(mu),odir,tag,float(mu)));
    #f1.write("rm -r *.py input* *.root *.tar.gz \n")
    f1.close();
    '''
    f2n = "tmp_%s.condor" % (tag);
    outtag = "out_%s_$(Cluster)" % (tag)
     
    f2=open(f2n, 'w')
    f2.write("universe = vanilla \n");
    f2.write("Executable = %s \n" % (f1n) );
    f2.write("Requirements = OpSys == \"LINUX\"&& (Arch != \"DUMMY\" ) \n");
    f2.write("request_disk = 10000000 \n");
    f2.write("request_memory = 21000 \n");
    f2.write("Should_Transfer_Files = YES \n");
    f2.write("WhenToTransferOutput  = ON_EXIT \n");
    f2.write("Transfer_Input_Files = %s, %s.tar.gz \n" % (f1n,CMSSWVER));
    f2.write("Output = "+outtag+".stdout \n");
    f2.write("Error = "+outtag+".stderr \n");
    f2.write("Log = "+outtag+".log \n");
    f2.write("Notification    = Error \n");
    f2.write("x509userproxy = $ENV(X509_USER_PROXY) \n")
    f2.write("Queue 1 \n");
    f2.close();
    '''
    #os.system("condor_submit %s" % (f2n));
    #os.system("sbatch %s " %f1n)
 #   os.chdir("../.");



if __name__ == '__main__':
    outDir = options.outDir
    eosDir = "root://cmseos.fnal.gov/"+options.outDir
    
    # get some info from the OS
    CMSSWVER = os.getenv("CMSSW_VERSION")
    CMSSWBASE = os.getenv("CMSSW_BASE")
    # tar it up for usage
    '''

    if not os.path.exists('tmp'):
        os.makedirs('tmp')
        cachedir('tmp')

    #if not options.keeptar:
    os.system("tar --exclude-caches-all -zcf tmp/"+CMSSWVER+".tar.gz -C "+CMSSWBASE+"/.. "+CMSSWVER)
    f = TFile.Open("inputHistograms/fastsimSignalT2qq/RA2bin_signal.root");
    names = [k.GetName() for k in f.GetListOfKeys()]
    models = []
    mGos=[]
    mLSPs=[]
    #print names
    for n in names:
        parse=n.split('_')
        #if parse[1] =="T1qqqq" or parse[1] =="T5qqqqVV":
        models.append(parse[1])
        mGos.append(int(parse[2]))
        mLSPs.append(int(parse[3]))
    '''

	    	#print parse
    #models=["T5qqqqVV"]
    #mGos  = [975];
    #mLSPs = [775];

    if not options.fastsim:
        #models = ['T1bbbb','T1bbbb','T1tttt','T1tttt','T1qqqq','T1qqqq','T2tt','T2tt','T2tt'];
        #mGos = [1500,1000,1500,1200,1400,1000,425,500,850];
        #mLSPs = [100,800,100,800,100,900,325,325,100];
	models=['T5HH','T5HH','T5HH','T5HH','T5HH']
	mGos = [1300,1400,1500,1600, 1700]
	mLSPs=[1250,1350,1450,1550,1650]
    # for signal in signals:
    for m in range(len(mGos)):
        #    for mLSP in mLSPs:
        command = "python analysisBuilderCondor.py ";
        command += "--signal %s " % models[m];
        command += "--mGo %i " % mGos[m];
        command += "--mLSP %i " % mLSPs[m];
        if options.fastsim: command += " --fastsim";
        command += " --realData";
        command += " --tag allBkgs";
        #command += " --eos %s" % (eosDir);

        tag = "%s_%i_%i" % (models[m],mGos[m],mLSPs[m]);
	os.system(command)
	#print command
        #condorize( command, tag, outDir, CMSSWVER );
        #time.sleep(0.05);


    # else:

    #     os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1500 --mLSP 100 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1000 --mLSP 100 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1500 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1200 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1400 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1000 --mLSP 800 --realData --tag allBkgs');





