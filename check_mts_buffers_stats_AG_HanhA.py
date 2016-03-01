#!/usr/bin/env python
import pexpect
import re
import sys, time
#import logger
import logging
#import login
import logging.handlers


def main():

    ssh_newkey = "yes/no"
    response = r'.*\(yes/no\):' 
    prompt= r'(\$|%|#|>)'
    prompt1 = r'\(local-mgmt\)#'
    prompt2 = r'\S*\(nxos\)#'
    pattern = r'\d.*ag'
    sleeptime=10
    x =1
    count = 0

    p=pexpect.spawn('ssh admin@10.193.222.63')
    #p.logfile=sys.stdout
    i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
    if i == 0:
        print "I say yes"
        p.sendline('yes')
        i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
    if i == 1:
        print "I give password\n",
        p.sendline("Nbv12345\r")
        p.expect('#')
        p.sendline ("connect nxos a")
        p.expect (prompt2)

        while x==1:
            print "count %d ######################" %count
            '''p=pexpect.spawn('ssh admin@10.193.222.106')
            p.logfile=sys.stdout
            i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
            if i == 0:
                print "I say yes"
                p.sendline('yes')
                i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
            if i == 1:
                print "I give password\n",
                p.sendline("Nbv12345\r")
                p.expect('#')
                #p.interact()'''
            #print p.before
            p.sendline ("show system internal mts sup apps | grep sw-stats-ag")
            p.expect(prompt2)
            output=p.before
            print output
            line= output.splitlines()
            print line
            line2 = line[2]
            print line2
            list1=line2.split()
            print list1
            sapno=list1[0]
            print sapno
            str = "show system internal mts buffers sap %s" %sapno
            p.sendline (str)
            p.expect(prompt2)
            output1=p.before
            print output1
            mts_lines = output1.splitlines()
            print mts_lines
            mts_line1=mts_lines[0]
            mts_line2=mts_lines[1]
            mts_line3=mts_lines[2]
            mts_line4=mts_lines[3]

            if mts_line4:
                print mts_line4
                mts_buffers = mts_line4.split()
                print mts_buffers

                mts_buffers.remove(mts_buffers[0])
                print mts_buffers

                mts_buffers.remove(mts_buffers[0])
                print mts_buffers

                mts_buffers_int = []
                for n in mts_buffers:
                    mts_buffers_int.append(int(n))
                mts_buffers = mts_buffers_int

                print mts_buffers

                mts_buffers = [int(i) for i in mts_buffers]

                for q in mts_buffers:
                    print q
                    if q < 5:
                        print "################No stats_AG q leak###################"

                    if q > 10:
                        print "mts q vlaue more than 10########################"
                        log_file = "*mts_buffer_%d" %count
                        logger.setup_logger('mylog', log_file)
                        mylog = logging.getLogger('mylog')
                        mylog.info(output1)
                    if q > 100:
                        print "Danger! mts q leak seen #######################"
                        log_file = "***leak_mts_buffer_%d" %count
                        logger.setup_logger('mylog', log_file)
                        mylog = logging.getLogger('mylog')
                        mylog.info(output1)
                        break
            time.sleep(sleeptime)
            count = count+1
        
if '__main__' == __name__:
    main()

