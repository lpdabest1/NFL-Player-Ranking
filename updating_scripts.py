import pages.Receiving_Stats as Receiving_Stats
import pages.Rushing_Stats as Rushing_Stats
import pages.Passing_Stats_Modern_Era as Passing_Stats_Modern_Era
import pages.Passing_Stats_Past_Era as Passing_Stats_Past_Era

import os
import time

while True:
    os.system("Receiving_Stats.py")
    time.sleep(3600*24)   
    os.system("Rushing_Stats.py")
    time.sleep(3600*24)
    os.system("Passing_Stats_Modern_Era.py")
    time.sleep(3600*24)
    os.system("Passing_Stats_Past_Era.py")
    time.sleep(3600*24)
 