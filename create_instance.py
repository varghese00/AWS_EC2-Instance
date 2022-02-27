# uncomment  the create create_kePair() method, created_instance variable and create_securityGroup()method if you want to create everything new and vice-versa


import os  ## helps to run terminal commands,example changing permissions
import boto3
image_id='ami-033b95fb8079dc481'
instance_type='t2.nano'
key_name='ec2-keyPair'
#region_name="us-east-1"  
ec2= boto3.resource('ec2')



##Creating the key-pair .pem file
def create_keyPair():
    try:
        print("Creating new key-pair") 
        ##create a file to store key locally
        outfile=open('ec2-keyPair.pem','w')
        ##call  boto3 function to create a key pair
        key_pair=ec2.create_key_pair(KeyName=key_name)
        ##capture the key and store it in a file
        KeyPairOut=str(key_pair.key_material)
        print(KeyPairOut)
        outfile.write(KeyPairOut)
        return KeyPairOut
    except Exception as e:
        print(e)
create_keyPair() #comment out for not to create a new keyPair.pem file and if created chmod 400 the file

os.system("chmod 400 ./ec2-keyPair.pem") ## changes the permission of the file created

## Creating a new ec2 instance
def create_newInstance():    
    try:
        instances = ec2.create_instances(
            ImageId=image_id ,#declared globally
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type, 
            UserData="""#!/bin/bash   
             yum update -y
             yum install httpd -y
             systemctl enable httpd
             systemctl start httpd 
             """, 
            KeyName=key_name,
            TagSpecifications=[
                 {
                     'ResourceType':'instance',
                     'Tags':[
                         {
                             'Key': 'Name',
                             'Value':'my_ipAddress_excercise',
                         },
                     ]
                 },
            ],
             
            )         
        return instances           
    except Exception as e:
        print(e) 

################Comment out the entire block to create and vice-versa ##################

created_instance=create_newInstance()
for instance in created_instance: 
   print(f'A new EC2 instance is just launched with id: " {instance.id}"')
   instance.wait_until_running()
   print(f'The ec2 instance with id "{instance.id}" just launched is now started running')




def get_InstanceId():
    all_instances=[]
    instances=ec2.instances.all()  ## instances.all() is a aws api built in method
    for instance in instances:
        all_instances.append(instance)
        last_instance_id=all_instances[-1].id
        print(f'The first instance in ec2 has the id "{last_instance_id}"')  ## f strings must be used to access a variable value
        return last_instance_id
instance_id_response=get_InstanceId()     ## calling the above method  

def create_securityGroup():

    security_group=ec2.create_security_group(
        Description='Allows SSH and HTTP access',
        GroupName='HTTP-SSH-CreatedBy-PythonProgram',
        TagSpecifications=[
        {
            'ResourceType':'security-group',
            'Tags':[
                {
                    'Key': 'Name',
                    'Value':'for-ssh-Access',
                }
            ]
        },
    ],
    
)
    security_group.authorize_ingress(
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'TCP',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'For ssh',
                    },
                ],
                'ToPort': 22,
                
            },
            {
                'FromPort': 80,
                'IpProtocol': 'TCP',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'For http',
                    },
                ],
                'ToPort': 80,
                
            },
        ],
    )
    return security_group.id

security_groupID=create_securityGroup()
print(f'Security group with id: "{security_groupID}" is just created')
    
def attach_SecGroupToEc2_Instance(ec2_instance_id):
    sec_group_list=[]
    sec_groups=ec2.security_groups.all()
    for sec_group in sec_groups:
        sec_group_list.append(sec_group)
        last_sec_group=sec_group_list[0].id  ## for some reason the new security code is being added to the 0 index in the list in aws security groups
    ec2_instance=ec2.Instance(ec2_instance_id)
    ec2_instance.modify_attribute(
        Groups=[
            last_sec_group
        ]
    )
    print(f'Instance id: "{ec2_instance_id}" and security-group: "{last_sec_group}" are succesfully attached to each other')    

attach_SecGroupToEc2_Instance(instance_id_response) ## instance_id_response is assigned instance_id_response=get_InstanceId() above





def newInstance_IP(instance_id):
    try:
        instance=ec2.Instance(instance_id)
        public_ip=instance.public_ip_address
        print(f'This  public ip-address of instance Id:  "{instance.id}" is "{instance.public_ip_address}"')
        return public_ip
    except Exception as e:
        print(e)
new_instance_ip=newInstance_IP(instance_id_response) ## accessing the ip address as a variable value for ssh below
print(new_instance_ip)
ip_ssh=os.system(f'ssh -i ec2-keyPair.pem ec2-user@{new_instance_ip}') ## f string must be used to access the variable values in python strings



