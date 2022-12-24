# import the python modules
import subprocess as sp , sys
import requests
from datetime import datetime

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
    create_timestamp=sp.getoutput(f'az vm list --query [].timeCreated -o tsv')
    # print(vm_list, rg_list,create_timestamp)
    vm_list=vm_list.split()
    rg_list=rg_list.split()
    create_timestamp=create_timestamp.split()
    current_time=datetime.now()
    right_format=[current_time-(datetime.strptime(x[:19],'%Y-%m-%dT%H:%M:%S')) for x in create_timestamp]
    demo_ind=vm_list.index('demo-new')
    vm_list.pop(demo_ind)
    rg_list.pop(demo_ind)
    right_format.pop(demo_ind)
    preview_ind=vm_list.index('preview-cluster')
    vm_list.pop(preview_ind)
    rg_list.pop(preview_ind)
    right_format.pop(preview_ind)
    bastion_ind=vm_list.index('bastion')
    vm_list.pop(bastion_ind)
    rg_list.pop(bastion_ind)
    right_format.pop(bastion_ind)
    
    # time_object=[datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in right_format]
    # diff_time=[x - current_time for x in create_timestamp]
    # print(vm_list, rg_list, right_format)
    return vm_list,rg_list,right_format

list_vm_rgs()
authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    vm_list,rg_list,right_format=list_vm_rgs()
    main_output=('Azure machines list\n\n')
    main_output+=(f"VM Name \t Resource Group \t Age \n")
    main_output+=("-------------------------------------------------------\n")
    for i in range(len(vm_list)):
        main_output+=(f'{vm_list[i]} : \t {rg_list[i]} : \t {right_format[i]}\n\n')
    print(main_output)
    resp = requests.post(
                webhooks_url,
                data={
                    'content':"```\n"+main_output+"\n```",
                },
            )
else:
    print("Authentication failed",authout[1])
