import paramiko
import os.path
import time
import sys
import re

#Checking username/password file
#Prompting user for input - USERNAME/PASSWORD FILE
user_file = input("\n# Enter user file path and name (e.g. ~/login-info.txt): ")

#Verifying the validity of the USERNAME/PASSWORD file
if os.path.isfile(user_file) == True:
    print("\n* Username/password file is valid :)\n")

else:
    print(f"\n* File {user_file} does not exist :( Please check and try again.\n")
    sys.exit()
        
#Checking commands file
#Prompting user for input - COMMANDS FILE
cmd_file = input("\n# Enter commands file path and name (e.g. ~/command-file.txt): ")

#Verifying the validity of the COMMANDS FILE
if os.path.isfile(cmd_file) == True:
    print("\n* Command file is valid :)\n")

else:
    print(f"\n* File {cmd_file} does not exist :( Please check and try again.\n")
    sys.exit()
    
#Open SSHv2 connection to the device
def ssh_connection(ip):
    
    # import the global variables into the local function space
    #   there variable values were obtained outside this function by
    #   prompting the user for these
    global user_file
    global cmd_file
    
    # Creating SSH CONNECTION
    try:
        # Define SSH parameters
        selected_user_file = open(user_file, 'r')
        
        # Starting from the beginning of the file
        selected_user_file.seek(0)
        
        # Reading the username from the file in first field
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")
        
        # Starting from the beginning of the file
        selected_user_file.seek(0)
        
        # Reading the password from the file in the second field
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        # Logging into device
        session = paramiko.SSHClient()
        
        # For testing purposes, this allows auto-accepting unknown host keys
        # Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the device using username and password
        session.connect(ip.rstrip("\n"), username = username, password = password)
        
        # Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        # Setting terminal length for entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        # Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        # Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        # Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        # Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        # Closing the user file
        selected_user_file.close()
        
        # Closing the command file
        selected_cmd_file.close()
        
        # Checking command output for NetDevice OS syntax errors
        router_output = connection.recv(65535)
        
        if re.search(b"% Invalid input", router_output):
            print(f"* There was at least one NetDevice OS syntax error on device {ip} :(")
            
        else:
            print(f"\nDONE for device {ip} :)\n")
            
        # Test for reading command output
        # this dumps all output - useful for debug: print(str(router_output) + "\n")
        # find all IPs in output using "[0-9]{1,3}\." regex
        print(f"IPs for device with IP {ip}: ", \
              re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",str(router_output)))
        
        # Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print("* Invalid username or password :( \n* Please check the username/password file or the device configuration.")
        print("* Closing program... Bye!")