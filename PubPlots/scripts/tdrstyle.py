from ROOT import TStyle, TColor

qcd_uscb_gold = TColor(2001, 255/255.,200/255.,47/255)
znn_penn_red = TColor(2002, 255/255.,0/255.,43/255.)
lost_lep_dusk_blue = TColor(2006, 105/255.,166/255., 202/255.)
had_tau_grayed_jade = TColor(2007, 133/255.,189/255., 164/255.)

pull_blue = TColor(2029, 20/255., 125/255., 97/255.)

signal_pinkle = TColor(2072, 205/255., 102/255., 255/255.) 

def tdrGrid( gridOn):
  tdrStyle.SetPadGridX(gridOn)
  tdrStyle.SetPadGridY(gridOn)

#fixOverlay: Redraws the axis
def fixOverlay():
    gPad.RedrawAxis()

def setTDRStyle():
  tdrStyle =  TStyle("tdrStyle","Style for P-TDR")

   #for the canvas:
  tdrStyle.SetCanvasBorderMode(0)
  tdrStyle.SetCanvasColor(0)
  tdrStyle.SetCanvasDefH(600) #Height of canvas
  tdrStyle.SetCanvasDefW(600) #Width of canvas
  tdrStyle.SetCanvasDefX(0)   #POsition on screen
  tdrStyle.SetCanvasDefY(0)


  tdrStyle.SetPadBorderMode(0)
  #tdrStyle.SetPadBorderSize(Width_t size = 1)
  tdrStyle.SetPadColor(0)
  tdrStyle.SetPadGridX(False)
  tdrStyle.SetPadGridY(False)
  tdrStyle.SetGridColor(0)
  tdrStyle.SetGridStyle(3)
  tdrStyle.SetGridWidth(1)

#For the frame:
  tdrStyle.SetFrameBorderMode(0)
  tdrStyle.SetFrameBorderSize(1)
  tdrStyle.SetFrameFillColor(0)
  tdrStyle.SetFrameFillStyle(0)
  tdrStyle.SetFrameLineColor(1)
  tdrStyle.SetFrameLineStyle(1)
  tdrStyle.SetFrameLineWidth(1)
  
#For the histo:
  #tdrStyle.SetHistFillColor(1)
  #tdrStyle.SetHistFillStyle(0)
  tdrStyle.SetHistLineColor(1)
#  tdrStyle.SetHistLineStyle(0)
  tdrStyle.SetHistLineWidth(2)
  #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
  #tdrStyle.SetNumberContours(Int_t number = 20)

  tdrStyle.SetEndErrorSize(2)
  #tdrStyle.SetErrorMarker(20)
  #tdrStyle.SetErrorX(0.)
  
  tdrStyle.SetMarkerStyle(20)
  
#For the fit/function:
  tdrStyle.SetOptFit(1)
  tdrStyle.SetFitFormat("5.4g")
  tdrStyle.SetFuncColor(2)
  tdrStyle.SetFuncStyle(1)
  tdrStyle.SetFuncWidth(1)

#For the date:
  tdrStyle.SetOptDate(0)
  # tdrStyle.SetDateX(Float_t x = 0.01)
  # tdrStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
  tdrStyle.SetOptFile(0)
  tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
  tdrStyle.SetStatColor(0)
  tdrStyle.SetStatFont(42)
  tdrStyle.SetStatFontSize(0.025)
  tdrStyle.SetStatTextColor(1)
  tdrStyle.SetStatFormat("6.4g")
  tdrStyle.SetStatBorderSize(1)
  tdrStyle.SetStatH(0.1)
  tdrStyle.SetStatW(0.15)
  # tdrStyle.SetStatStyle(Style_t style = 1001)
  # tdrStyle.SetStatX(Float_t x = 0)
  # tdrStyle.SetStatY(Float_t y = 0)

# Margins:
  tdrStyle.SetPadTopMargin(0.05)
  tdrStyle.SetPadBottomMargin(0.13)
  tdrStyle.SetPadLeftMargin(0.16)
  tdrStyle.SetPadRightMargin(0.02)

# For the Global title:

  tdrStyle.SetOptTitle(0)
  tdrStyle.SetTitleFont(42)
  tdrStyle.SetTitleColor(1)
  tdrStyle.SetTitleTextColor(1)
  tdrStyle.SetTitleFillColor(10)
  tdrStyle.SetTitleFontSize(0.05)
  # tdrStyle.SetTitleH(0) # Set the height of the title box
  # tdrStyle.SetTitleW(0) # Set the width of the title box
  # tdrStyle.SetTitleX(0) # Set the position of the title box
  # tdrStyle.SetTitleY(0.985) # Set the position of the title box
  # tdrStyle.SetTitleStyle(Style_t style = 1001)
  # tdrStyle.SetTitleBorderSize(2)

# For the axis titles:

  tdrStyle.SetTitleColor(1, "XYZ")
  tdrStyle.SetTitleFont(42, "XYZ")
  tdrStyle.SetTitleSize(0.06, "XYZ")
  # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
  # tdrStyle.SetTitleYSize(Float_t size = 0.02)
  tdrStyle.SetTitleXOffset(0.9)
  tdrStyle.SetTitleYOffset(1.25)
  # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

# For the axis labels:

  tdrStyle.SetLabelColor(1, "XYZ")
  tdrStyle.SetLabelFont(42, "XYZ")
  tdrStyle.SetLabelOffset(0.007, "XYZ")
  tdrStyle.SetLabelSize(0.05, "XYZ")

# For the axis:

  tdrStyle.SetAxisColor(1, "XYZ")
  tdrStyle.SetStripDecimals(True)
  tdrStyle.SetTickLength(0.03, "XYZ")
  tdrStyle.SetNdivisions(510, "XYZ")
  tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
  tdrStyle.SetPadTickY(1)

# Change for log plots:
  tdrStyle.SetOptLogx(0)
  tdrStyle.SetOptLogy(0)
  tdrStyle.SetOptLogz(0)

# Postscript options:
  tdrStyle.SetPaperSize(20.,20.)
  # tdrStyle.SetLineScalePS(Float_t scale = 3)
  # tdrStyle.SetLineStyleString(Int_t i, const char* text)
  # tdrStyle.SetHeaderPS(const char* header)
  # tdrStyle.SetTitlePS(const char* pstitle)

  # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
  # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
  # tdrStyle.SetPaintTextFormat(const char* format = "g")
  # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
  # tdrStyle.SetTimeOffset(Double_t toffset)
  # tdrStyle.SetHistMinimumZero(kTRUE)

  tdrStyle.SetHatchesLineWidth(1)
  tdrStyle.SetHatchesSpacing(1)

  ## legends
  tdrStyle.SetLegendFillColor(0)
  tdrStyle.SetLegendFont(62)
  tdrStyle.SetLegendBorderSize(0)

  ## JACK custom
  tdrStyle.SetEndErrorSize(0)
  
  tdrStyle.cd()
