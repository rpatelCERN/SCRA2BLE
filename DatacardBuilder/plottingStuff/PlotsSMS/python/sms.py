from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()
        if modelname.find("T5qqqqVV") != -1: self.T5qqqqVV()
	if modelname.find("T2tt")!=-1:self.T2tt()
	if modelname.find("T2bb")!=-1:self.T2bb()
	if modelname.find("T2qq")!=-1:self.T2qq()

    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 2000
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
    def T5qqqqVV(self):
        # model name
        self.modelname = "T5qqqqVV"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} V #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 1800
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow t #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 200
        self.Xmax = 1000
        self.Ymin = 0
        self.Ymax = 600
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 175
	#mW2= 160
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        #self.diagY2=array('d',[-mW2, 20000-mW2])
    def T2bb(self):
        # model name
        self.modelname = "T2bb"
        # decay chain
        self.label= "pp #rightarrow #tilde{b} #tilde{b}, #tilde{b} #rightarrow b #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 300
        self.Xmax = 1200
        self.Ymin = 0
        self.Ymax = 800

        # produce sparticle
        self.sParticle = "m_{#tilde{b}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 175
	#mW2= 160
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        #self.diagY2=array('d',[-mW2, 20000-mW2])
        
    def T2qq(self):
        # model name
        self.modelname = "T2qq"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow q #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 200
        self.Xmax = 1000
        self.Ymin = 0
        self.Ymax = 600
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 175
	#mW2= 160
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        #self.diagY2=array('d',[-mW2, 20000-mW2])

    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 1800
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0
	#mW2= 160
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        #self.diagY2=array('d',[-mW2, 20000-mW2])
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2100
        self.Ymin = 0
        self.Ymax = 1800
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
	mW = 0
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])
