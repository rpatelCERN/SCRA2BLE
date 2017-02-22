from ROOT import *

f=TFile("OutputDataEvents.root", "READ");
EventTree=f.Get("tree")
evList=open("eventsRunG.txt", 'w')
for event in EventTree:
	print event.RunNum 
	evList.write("%d:%d:%d\n" %(event.RunNum,event.LumiBlockNum ,event.EvtNum))
