import sys
import subprocess

# Import name from os to check OS type for correct usage of ping
from os import name


#Checking IP reachability
def ip_reach(list):

    for ip in list:
        ip = ip.rstrip("\n")

        # Sending only 2 ICMP packets with "-n 2"
        # Redirecting stdout and stderr to DEVNULL to supress all output from ping as we are only
        #   interested in the return value being 0 if succesfull or !=0 if failed

        # for windows
        # use "-n 2" parameter
        if name == 'nt':
            ping_reply = subprocess.run('ping %s -n 2' % (ip), stdout=subprocess.DEVNULL, \
                                         stderr=subprocess.DEVNULL)

        # for mac and linux
        # use "-c 2" parameter
        elif name == 'posix':
            ping_reply = subprocess.run('ping %s -c 2' % (ip), stdout=subprocess.DEVNULL, \
                                         stderr=subprocess.DEVNULL, shell=True)

        # unknown OS
        else:
            print(f"Unknown OS \'{name}\', and not able to correctly ping targets, please run on supported OS")
            sys.exit()

        if ping_reply == 0:
            print("\n* {} is reachable :)\n".format(ip))

            # If ping is successful then continue to next IP in list skipping rest of code in for loop block
            continue
        
        else:
            print('\n* {} not reachable :( Check connectivity and try again.'.format(ip))
            sys.exit()