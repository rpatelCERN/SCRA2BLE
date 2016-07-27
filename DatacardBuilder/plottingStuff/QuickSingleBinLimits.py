from ROOT import *
import sys
import os
model=sys.argv[1]
Mgo=int(sys.argv[2])
Mlsp=int(sys.argv[3])

iDir="testCards-allBkgs-%s_%d_%d-7.7-mu0.0/" %(model,Mgo,Mlsp)
i=int(sys.argv[4])
#for i in range(0,160):
TotalCards=" "
TotalCards=TotalCards+" %s/card_signal%d.txt  %s/card_SLControl%d.txt %s/card_Lowdphi%d.txt" %(iDir,i,iDir,i,iDir,i)
photonbin=-1
if i<40:#Njets0 
	photonbin=i%10
if i>=40 and i<80:
	photonbin=10+(i-40)%10
if i>=80 and i<120:
	photonbin=20+(i-80)%10
if i>=120 and i<160:
	photonbin=30+(i-120)%10

TotalCards=TotalCards+" %s/card_sphoton%d.txt" %(iDir,photonbin)
os.system(" combineCards.py %s >%s/SingleBin%dExclusion.txt " %(TotalCards,iDir,i) )
os.chdir("%s" %iDir)
#for i in range(0,160):
os.system("combine -M Asymptotic SingleBin%dExclusion.txt -n Bin%d -m %d " %( i,i,i))
