import sys
import subprocess

#Checking IP reachability
def ip_reach(list):

    for ip in list:
        ip = ip.rstrip("\n")

        # Sending only 2 ICMP packets with "-n 2"
        # Redirecting stdout and stderr to DEVNULL to supress all output from ping as we are only
        #   interested in the return value being 0 if succesfull or !=0 if failed
        ping_reply = subprocess.call('ping %s -c 2' % (ip,), stdout=subprocess.DEVNULL, \
                                     stderr=subprocess.DEVNULL, shell=True)
        
        if ping_reply == 0:
            print("\n* {} is reachable :)\n".format(ip))

            # If ping is successful then continue to next IP in list skipping rest of code in for loop block
            continue
        
        else:
            print('\n* {} not reachable :( Check connectivity and try again.'.format(ip))
            sys.exit()