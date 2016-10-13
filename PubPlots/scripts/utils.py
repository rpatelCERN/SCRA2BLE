
import math
from bg_est import BGEst

## round number to N digits -- helpful for printing
def round_to_digits(value, ndigits):
    if (value == 0.): ## otherwise it will return 'nan' due to the log10() of zero
        return value
    factor = math.pow(10.0, ndigits - math.ceil(math.log10(math.fabs(value))))
    return round(value * factor) / factor   


## returns a string of a BG prediction with the rounding and significant figures
def GetPred(bg_est, bin_number): # note: this is the root bin number -- index starts from 1!
    cv = bg_est.hCV.GetBinContent(bin_number)
    p_statup = round_to_digits(bg_est.hStatUp.GetBinContent(bin_number), 2)
    p_statdown = round_to_digits(bg_est.hStatDown.GetBinContent(bin_number), 2)
    p_systup = round_to_digits(bg_est.hSystUp.GetBinContent(bin_number), 2)
    p_systdown = round_to_digits(bg_est.hSystDown.GetBinContent(bin_number), 2)
   
    ## all uncertainties and CV must match the precision of the least precise uncertainty/CV
    if cv == 0. and p_statup == 0.: ## special case: all are 0 to  2-decimal precision, can't take logs
        return ("$0.00^{+0.00+0.00}_{-0.00-0.00}$")
    
    ndig = math.floor(math.log10(p_statup)) # now this one should never be 0
    if p_systup>0. and math.floor(math.log10(p_systup))>ndig:
        ndig = math.floor(math.log10(p_systup))
    if p_statdown>0. and math.floor(math.log10(p_statdown))>ndig:
        ndig = math.floor(math.log10(p_statdown))
    if p_systdown>0. and math.floor(math.log10(p_systdown))>ndig:
        ndig = math.floor(math.log10(p_systdown))

    # print the CV and uncertainties to a consistent number of significant figures
    if ndig>0: ## at least one uncertainty is > 10, print no decimals anywhere
        return ("$%2.0f^{+%2.0f+%2.0f}_{-%2.0f-%2.0f}$" % (cv, p_statup, p_systup, p_statdown, p_systdown))
    elif ndig==0: ## largest is 1.0-9.9, print 1 decimal point
        return("$%3.1f^{+%3.1f+%3.1f}_{-%3.1f-%3.1f}$" % (cv, p_statup, p_systup, p_statdown, p_systdown))
    else: ## largest is < 1, can print to 2 decimal points
        return("$%3.2f^{+%3.2f+%3.2f}_{-%3.2f-%3.2f}$" % (cv, p_statup, p_systup, p_statdown, p_systdown))
  
  
