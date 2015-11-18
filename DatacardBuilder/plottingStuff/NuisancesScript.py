import re
import os
import sys


os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMSbbbb1500-1.3-mu0.0.root -o NUIS_SMSbbbb1500.txt');
os.system('python QuickNuisPlot.py NUIS_SMSbbbb1500 -b');

os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMSbbbb1000-1.3-mu0.0.root -o NUIS_SMSbbbb1000.txt');
os.system('python QuickNuisPlot.py NUIS_SMSbbbb1000 -b');

os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMStttt1500-1.3-mu0.0.root -o NUIS_SMStttt1500.txt');
os.system('python QuickNuisPlot.py NUIS_SMStttt1500 -b');

os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMStttt1200-1.3-mu0.0.root -o NUIS_SMStttt1200.txt');
os.system('python QuickNuisPlot.py NUIS_SMStttt1200 -b');

os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMSqqqq1400-1.3-mu0.0.root -o NUIS_SMSqqqq1400.txt');
os.system('python QuickNuisPlot.py NUIS_SMSqqqq1400 -b');

os.system('python diffNuisances.py ../mlfittestCards-allBkgs-SMSqqqq1000-1.3-mu0.0.root -o NUIS_SMSqqqq1000.txt');
os.system('python QuickNuisPlot.py NUIS_SMSqqqq1000 -b');