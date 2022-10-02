# import the python modules
import subprocess as sp , sys

# Get the all arguments
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
vmname=sys.argv[4]
rgname=sys.argv[5]

# define the auth function
def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

def checkvmstatus():
    vmstatus=sp.getoutput("az vm show -d  --name {}  --resource-group {}  --query powerState -o tsv".format(vmname,rgname))
    return vmstatus

# define the auto start azure vm function
def autostart():
    vmstatus=checkvmstatus()
    print(vmstatus)
    if vmstatus=="VM running":
        print("Machine is running")
    elif vmstatus=="VM deallocated" or vmstatus=="VM deallocating":
        print("VM has deallocated")
        sp.getoutput("az vm start -n {} -g {}".format(vmname,rgname))
        print("Waiting to start")
        sp.getoutput("sleep 15")
        verifystatus=checkvmstatus()
        print("Current status is :",verifystatus)
    else:
        print("Something wrong")

authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    autostart()
else:
    print("Authentication failed",authout[1])
