import logging
import boto3
from botocore.exceptions import ClientError


check = False
ec2 = boto3.resource('ec2', region_name='eu-west-1')
ec2c = boto3.client('ec2', region_name='eu-west-1')
for rds_security_group in ec2c.describe_security_groups()['SecurityGroups']:
    if rds_security_group['GroupName'] == 'SSH-HTTP-ONLY': 
        check = check | True
    else:
        check = check | False
if check == False:
    try:
        securitygroup = ec2.create_security_group(GroupName='SSH-HTTP-ONLY', Description='only allow SSH and HTTP traffic')
        securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
        securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
    except ClientError as e:
        logging.error(e)
