import nmap
import argparse
import os
import subprocess
import pyfiglet


def folder_creater(foldername):

    folder_name = foldername
    CHECK_FOLDER = os.path.isdir(folder_name)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(folder_name)
        print("(+) Created Folder : ", folder_name)

    else:
        print("(-) "+folder_name+" Already Exists.")

def banner():

    ascii_banner = pyfiglet.figlet_format("Network Scanner 2.0!!")
    print("---------------------------------------")
    print(ascii_banner)
    print("---------------------------------------")
    print("(+) Program intialized \n")

    print("Now with subprocess(Work in Progress)")

#File Reader
def file_reader():

    print("(+) Opening file")

    #Open file and append to list
    file=open(args.input,'r')

    for line in file:

        fields = line.split()
        # print(fields)

        IP_list.append(fields[0])
        IP_location.append(fields[1])

    file.close()

    print("(+)", len(IP_list),"IP Locations have been read")
    print("(+) Closing file \n")


    try:
        # Change the current working Directory
        os.chdir(args.output)
        print("(+) Directory changed")
    except OSError:
        print("(-) Error : Can't change the Current Working Directory")

### NMAP Ping Mode ###
def nmap_ping_scanner():

    print("(+) Starting nmap")
    nm = nmap.PortScanner()
    print("(+) Scanning list ")


    folder_creater("Ping_List")

    # print(IP_list)

    for i in range(len(IP_list)):
        print("\n Scanning "+str(i+1)+" of "+str(len(IP_list)))
        nm.scan(IP_list[i], arguments='-n -sn ')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        # print(i)

        print("(+) Creating IP list with hosts up")
        ping_list_file = IP_location[i]+"_Ping_List.txt"
        f = open("Ping_List/"+ping_list_file, "w")

        # Write the IPs that are up to file
        for host, status in hosts_list:

            f.write(host+"\n")

            # Check output
            # print(host + ' ' + status)

        f.close()
        print("(+) Closing file "+ping_list_file+"\n")


#####  MASSCAN
def masscanner():


    ## Need to iterate through Ping List

    print("(+) Scanning for ports using Masscan \n")
    ports = "7000"

    for i in range(len(IP_list)):

        ping_list = "Ping_List/"+IP_location[i]+"_Ping_List.txt"
        print("i = ",i," of",len(IP_list)-1 )

        # m1_cmd ="sudo masscan "+
        #     "--top-ports "+ports+
        #     " -iL "+ ping_list+
        #     " --rate 10000 -oG Godzilla.txt"


        masscan_command = os.system(
            "sudo masscan "+
            "--top-ports "+ports+
            " -iL "+ ping_list+
            " --rate 10000 -oG Godzilla.txt")
        print("\n(+) Process Complete. Results saved to File")

        print("")
        if(i==1):
            os.system("grep -oP '(?<=Ports: )[0-9]+' Godzilla.txt | sort -u >  abc.txt")
        else:
            os.system("grep -oP '(?<=Ports: )[0-9]+' Godzilla.txt | sort -u >>  abc.txt")

    print("Running Grep Ports")
    list =os.system("grep -oP '[0-9]+' abc.txt | sort -u >  Ports.txt ")

# Vuln Scan via Nmap
def nmap_vuln_scanner():

    #Open Ports file and read ports to a list
    Ports_Text_reader = open("Ports.txt", "r")
    content = Ports_Text_reader.read()
    Ports_list = content.split("\n")
    Ports_Text_reader.close()

    #Convert List to string and replace space with commas
    Ports_String = ' '.join(map(str,Ports_list))
    Ports_String = Ports_String.replace(" ",",")

    #Just a check
    print(Ports_String)

    # Check and create folder if not exists
    folder_creater("XML")
    folder_creater("HTML")


    print("\n\t [1] Run Nmap Scan")
    print("\t [2] Run Nmap Vuln Scan\n")



    choice_nmap = int(input('Your choice : '))


    for i in range(len(IP_list)):

        file_name = "Ping_List/"+IP_location[i]+"_Ping_List.txt"
        print(file_name)

        XML_file_name = IP_location[i]+".xml"

        if (choice_nmap==1):

            cmd = "nmap -A -T4 -vv -sC -sV -iL "+file_name+" -p "+Ports_String+" -oX XML/"+ XML_file_name
            print (cmd)
            os.system(cmd)

        elif(choice_nmap==2):

            cmd = "sudo nmap -A -T4 -vv --script vulners -iL "+file_name+" -p "+Ports_String+" -oX XML/"+ XML_file_name
            print (cmd)
            os.system(cmd)

        else:
            break

        #Convert XML file to HTML
        os.system("xsltproc XML/"+XML_file_name+" -o HTML/"+IP_location[i]+".html")

def menu():

    menu_banner = pyfiglet.figlet_format("\t\tM e n u",font="emboss")
    print(menu_banner)

    print("\t [1] Run Ping Scan")
    print("\t [2] Run Port Scan")
    print("\t [3] Run Nmap Vuln Scan")
    print("\t [4] Run All\n")

    user_choice = int(input('Your choice : '))


    if(user_choice==1):
        print("(#) Nmap Ping Scan Starting \n")
        nmap_ping_scanner()

    elif(user_choice==2):
        masscanner()

    elif(user_choice==3):
        nmap_vuln_scanner()

    elif(user_choice==4):
        nmap_ping_scanner()
        masscanner()
        nmap_vuln_scanner()

    else:
        print("Wrong choice. Bye")


banner()

#Intialize empty list
IP_list=[]
IP_location=[]


print("(+) Parsing Arguments \n")

#Collect arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type=str)
parser.add_argument("--output", "-o", type=str, required=False)
args = parser.parse_args()


file_reader()
menu()









#e=subprocess.Popen(" nmap -sn -n -vvv "+IP_list[4],
#shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#e.communicate()[0]

# e  = os.popen("nmap -sn -n -vvv "+IP_list[4]).read()
# print (e)


# print("(+) Scanning list ")


# ge=subprocess.Popen("sudo masscan  --top-ports 80 --rate 10000 -oG OLE.txt"+IP_list[3],
#     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# ge.communicate()[0]



# ge=subprocess.Popen("sudo nmap -sn -n -vvv "+IP_list[4],
#shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#e.communicate()[0]

# e  = os.popen("nmap -sn -n -vvv "+IP_list[4]).read()
# print (e)
