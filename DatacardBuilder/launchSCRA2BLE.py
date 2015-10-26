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
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')

(options, args) = parser.parse_args()

def condorize(command,tag,odir):

	print "--------------------"
	print "Launching phase space point:",tag

	startdir = os.getcwd();
	#change to a tmp dir
	if not os.path.exists('tmp'): os.makedirs('tmp');
	os.chdir("tmp");
	curdir = os.getcwd();

	f1n = "tmp_%s.sh" %(tag);
	f1=open(f1n, 'w')
	f1.write("#!/bin/sh \n");

	# setup environment
	f1.write("source /cvmfs/cms.cern.ch/cmsset_default.sh \n");
	f1.write("set SCRAM_ARCH=slc6_amd64_gcc481\n")
	f1.write("cd %s \n" % (startdir) );
	f1.write("eval `scramv1 runtime -sh`\n")
	# f1.write("tar -cvzf package.tar.gz *.py input* \n")
	# copy over all stuff and run 
	f1.write("cd - \n");
	f1.write("cp %s/package.tar.gz . \n" % (startdir));
	f1.write("tar -xvzf package.tar.gz \n" );
	f1.write("ls \n");
	f1.write(command+" \n")
	f1.write("xrdcp -f results_%s.root root://cmseos.fnal.gov/%s/results_%s.root \n" % (tag,odir,tag));
	f1.write("rm -r *.py input* *.root *.tar.gz")
	f1.close();

	f2n = "tmp_%s.condor" % (tag);
	outtag = "out_%s_$(Cluster)" % (tag)
	f2=open(f2n, 'w')
	f2.write("universe = vanilla \n");
	f2.write("Executable = %s \n" % (f1n) );
	f2.write("Requirements = OpSys == \"LINUX\"&& (Arch != \"DUMMY\" ) \n");
	f2.write("Should_Transfer_Files = YES \n");
	f2.write("WhenToTransferOutput  = ON_EXIT_OR_EVICT \n");
	f2.write("Output = "+outtag+".stdout \n");
	f2.write("Error = "+outtag+".stderr \n");
	f2.write("Log = "+outtag+".log \n");
	f2.write("Notification    = Error \n");
	f2.write("x509userproxy = $ENV(X509_USER_PROXY) \n")

	f2.write("Queue 1 \n");
	f2.close();

	os.system("condor_submit %s" % (f2n));

	os.chdir("../.");



if __name__ == '__main__':

	# outDir = "/store/user/rgp230/SUSY/statInterp/scanOutput"

	# # tar it up for usage
	# os.system('tar -cvzf package.tar.gz *.py input*');


	# signals = ['T1bbbb'];
	# f = TFile("inputHistograms/histograms_1p3fb/fastsimSignalScan/RA2bin_signal.root");
	# names = [k.GetName() for k in f.GetListOfKeys()]
	# mGos=[]
	# mLSPs=[]
	# for n in names:
 #        	parse=n.split('_')
 #       		mGos.append(int(parse[2]))
	#         mLSPs.append(int(parse[3]))

	# #mGos  = [1200];
	# #mLSPs = [1150];


	# for signal in signals:
	# 	for m in range(len(mGos)):
	# 		#for mLSP in mLSPs:
	# 			command = "python analysisBuilderCondor.py -b ";
	# 			command += "--signal %s " % signal;
	# 			command += "--mGo %i " % mGos[m];
	# 			command += "--mLSP %i " % mLSPs[m];
	# 			command += "--fastsim";
	# 			print command;
	# 			# os.system( command );
	# 			tag = "%s_%i_%i" % (signal,mGos[m],mLSPs[m]);
	# 			condorize( command, tag, outDir );
	# 			time.sleep(0.1);
	
	# time.sleep(0.1);
	# os.system('rm package.tar.gz');

	# os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1500 --mLSP 800');
	os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1000 --mLSP 100');
	# os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1500 --mLSP 800');
	# os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1200 --mLSP 800');
	# os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1400 --mLSP 800');
	# os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1000 --mLSP 800');





