import boto3
import botocore


image_id = 
instance_type = 't2.micro'
keypair_name = 'awstest'
security_groups = 'SSH-HTTP-ONLY'

tag_name = {"Key": "ResourseName", "Value": "AlexPalazchenko"}
region = 'eu-west-1'

ec2 = boto3.resource('ec2', region_name= region)
ec2_client = boto3.client('ec2', region_name= region)

def create_ec2_instance():
    
    try:
        response = ec2.create_instances( ImageId='ami-02df9ea15c1778c9c',
                                         InstanceType=instance_type,
                                         KeyName= keypair_name,
                                         MaxCount=1,
                                         MinCount=1,
                                         SecurityGroups=[
                                         'SSH-HTTP-ONLY',
                                         ],
                                         TagSpecifications=[{'ResourceType': 'instance',
                                                             'Tags': [tag_name]}])
        return response[0]




created_instance = create_ec2_instance(image_id, instance_type, keypair_name)
created_instance.wait_until_running()
classic_address = ec2.ClassicAddress('public_ip')
print(classic_address)