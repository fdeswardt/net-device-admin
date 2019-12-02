import sys

#Checking octets
def ip_addr_valid(list):

    for ip in list:
        # remove the trailing \n produced by the readlines() function
        ip = ip.rstrip("\n")

        # split the IP address into a list of 4 octets
        octet_list = ip.split('.')

        # check that IP is not in reserved ranges
        # See https://en.wikipedia.org/wiki/Reserved_IP_addresses for details
        #
        # check IP is not: - multicast: 224.0.0.0/4 -or- reserved for future use: 240.0.0.0/4
        # check IP is not Link-Local 169.254.0.0/16
        # check IP is not loopback 127.0.0.0/8
        # check IP is not broadcast of 255.255.255.255
        if (len(octet_list) == 4) \
                and (1 <= int(octet_list[0]) <= 223) \
                and (int(octet_list[0]) != 169 \
                     or int(octet_list[1]) != 254) \
                and (int(octet_list[0]) != 127) \
                and (0 <= int(octet_list[1]) <= 255 \
                     and 0 <= int(octet_list[2]) <= 255 \
                     and 0 <= int(octet_list[3]) <= 255):

            # If octet is valid then continue for-loop to next IP in list
            continue

        else:
            # If octet is not valid then exit with message
            print('\n* There was an invalid IP address in the file: {} :(\n'.format(ip))
            sys.exit()
