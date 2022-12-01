# import the python modules
import subprocess as sp , sys
import requests

# Get the all arguments
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
webhooks_url=sys.argv[4]


# define the auth function
def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

def list_vm_rgs():
    vm_list = sp.getoutput(f'az vm list --query [].name -o tsv')
    rg_list = sp.getoutput(f'az vm list --query [].resourceGroup  -o tsv')
    vm_list=vm_list.split()
    rg_list=rg_list.split()
    return vm_list,rg_list


authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    vm_list,rg_list=list_vm_rgs()
    main_output=('Azure machines list\n\n')
    main_output+=(f"VM Name \t\t Resource Group \n")
    main_output+=("--------------------------------\n")
    for i in range(len(vm_list)):
        main_output+=(f'{vm_list[i]} : \t\t {rg_list[i]}\n')
    print(main_output)
    resp = requests.post(
                webhooks_url,
                data={
                    'content':"```\n"+main_output+"\n```",
                },
            )
else:
    print("Authentication failed",authout[1])
