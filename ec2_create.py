import logging
import boto3
import paramiko
from botocore.exceptions import ClientError
import time 

image_id = 'ami-02df9ea15c1778c9c'
instance_type = 't2.micro'
keypair_name = 'awstest'
security_groups = 'SSH-HTTP-ONLY'
tag_name = {"Key": "ResourseName", "Value": "AlexPalazchenko"}
region = 'eu-west-1'
pathKey = '/home/user/aws_script/awstest.pem'
pathScript = '/home/user/aws_script/script.sh'

ec2 = boto3.resource('ec2', region_name= region)
ec2_client = boto3.client('ec2', region_name= region)



def create_security_group(security_groups):
    check = False
    
    for rds_security_group in ec2_client.describe_security_groups()['SecurityGroups']:
        if rds_security_group['GroupName'] == security_groups: 
            check = True
    if check == False:
        try:
                securitygroup = ec2.create_security_group( GroupName=security_groups, 
                                                           Description='only allow SSH and HTTP traffic')
                securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
                securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
                
        except ClientError as e:
                logging.error(e)


def create_ec2_instance(image_id, instance_type, keypair_name, security_groups):
    
    try:
        response = ec2.create_instances( ImageId=image_id,
                                         InstanceType=instance_type,
                                         KeyName= keypair_name,
                                         MaxCount=1,
                                         MinCount=1,
                                         SecurityGroups=[
                                         security_groups,
                                         ],
                                         TagSpecifications=[{'ResourceType': 'instance',
                                                             'Tags': [tag_name]}])
        return response[0]
                                            
    except ClientError as e:
        logging.error(e)


def create_ebs():
    response = ec2_client.create_volume( AvailabilityZone='eu-west-1a',
                                         Encrypted=False,
                                         Size=1,
                                         VolumeType='standard',
                                         TagSpecifications=[
                                             {'ResourceType': 'volume',
                                              'Tags' : [tag_name],
                                             }])     
    return response['VolumeId'] 


def create_connection_to_instance(publicIp):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=publicIp, username='ubuntu', key_filename=pathKey)

    bash_script = open(pathScript).read()
    stdin, stdout, stderr = ssh.exec_command(bash_script)

    for line in stdout.read().splitlines():
        print(line)

    ssh.close()


def main():
        
    create_security_group(security_groups)
    created_instance = create_ec2_instance(image_id, instance_type, keypair_name, security_groups)
    volume_id = create_ebs()
    created_instance.wait_until_running()
    created_instance.attach_volume(VolumeId=volume_id, Device='/dev/sdy')
    publicIp = created_instance.public_dns_name
    print(publicIp)
    time.sleep(55) #bad way ))
    create_connection_to_instance(publicIp)          
    
    
    




if __name__ == '__main__':
    main()
