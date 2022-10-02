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


# VM deallocated
# az vm show -d  --name anugrah1  --resource-group anugrah1-RG  --query powerState  -o json
# az vm get-instance-view --name manish-microk8s --resource-group MANISH-MICROK8S-RG --query instanceView.statuses  -o json

# az vm show -d  --name manish-microk8s  --resource-group manish-microk8s-RG  --query "powerState"  -o tsv 

# az login --service-principal -u faa31a16-d9fe-4e9d-9fc9-56cddde425bd -p FH48Q~1yqXQ81oF.abHHazekZaQscIfXwU2Q.awM --tenant aee9b2ed-7ecc-4cb2-bfed-6d0d71c0e957 